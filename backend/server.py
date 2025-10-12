from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path
from bson import ObjectId
from datetime import datetime, timedelta
import os
import logging

# Import models and auth
from models import (
    Experience, ExperienceCreate, ExperienceUpdate,
    Education, EducationCreate, EducationUpdate,
    Project, ProjectCreate, ProjectUpdate,
    Certification, CertificationCreate, CertificationUpdate,
    Skill, SkillCreate, SkillUpdate,
    ContactMessage, ContactMessageCreate,
    Admin, AdminCreate, AdminLogin, Token
)
from auth import (
    get_password_hash, verify_password, create_access_token,
    get_current_admin, ACCESS_TOKEN_EXPIRE_MINUTES
)

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create FastAPI app
app = FastAPI(title="Ivan Armadi Portfolio API")

# Create API router
api_router = APIRouter(prefix="/api")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Helper function to convert ObjectId to string
def serialize_doc(doc):
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

# ===========================================
# PUBLIC ENDPOINTS
# ===========================================

@api_router.get("/")
async def root():
    return {"message": "Ivan Armadi Portfolio API", "version": "1.0"}

# Experience Endpoints
@api_router.get("/experience")
async def get_all_experience():
    experiences = await db.experience.find().sort("order", 1).to_list(100)
    return [serialize_doc(exp) for exp in experiences]

@api_router.get("/experience/{exp_id}")
async def get_experience(exp_id: str):
    if not ObjectId.is_valid(exp_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    exp = await db.experience.find_one({"_id": ObjectId(exp_id)})
    if not exp:
        raise HTTPException(status_code=404, detail="Experience not found")
    return serialize_doc(exp)

# Education Endpoints
@api_router.get("/education")
async def get_all_education():
    education = await db.education.find().sort("order", 1).to_list(100)
    return [serialize_doc(edu) for edu in education]

@api_router.get("/education/{edu_id}")
async def get_education(edu_id: str):
    if not ObjectId.is_valid(edu_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    edu = await db.education.find_one({"_id": ObjectId(edu_id)})
    if not edu:
        raise HTTPException(status_code=404, detail="Education not found")
    return serialize_doc(edu)

# Project Endpoints
@api_router.get("/projects")
async def get_all_projects():
    projects = await db.projects.find().sort("order", 1).to_list(100)
    return [serialize_doc(proj) for proj in projects]

@api_router.get("/projects/{proj_id}")
async def get_project(proj_id: str):
    if not ObjectId.is_valid(proj_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    proj = await db.projects.find_one({"_id": ObjectId(proj_id)})
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return serialize_doc(proj)

@api_router.get("/projects/category/{category}")
async def get_projects_by_category(category: str):
    projects = await db.projects.find({"category": category}).sort("order", 1).to_list(100)
    return [serialize_doc(proj) for proj in projects]

# Certification Endpoints
@api_router.get("/certifications")
async def get_all_certifications():
    certifications = await db.certifications.find().sort("order", 1).to_list(100)
    return [serialize_doc(cert) for cert in certifications]

@api_router.get("/certifications/{cert_id}")
async def get_certification(cert_id: str):
    if not ObjectId.is_valid(cert_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    cert = await db.certifications.find_one({"_id": ObjectId(cert_id)})
    if not cert:
        raise HTTPException(status_code=404, detail="Certification not found")
    return serialize_doc(cert)

# Skill Endpoints
@api_router.get("/skills")
async def get_all_skills():
    skills = await db.skills.find().sort("order", 1).to_list(100)
    return [serialize_doc(skill) for skill in skills]

@api_router.get("/skills/{skill_id}")
async def get_skill(skill_id: str):
    if not ObjectId.is_valid(skill_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    skill = await db.skills.find_one({"_id": ObjectId(skill_id)})
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return serialize_doc(skill)

# Contact Endpoint
@api_router.post("/contact")
async def submit_contact(contact: ContactMessageCreate):
    contact_dict = contact.model_dump()
    contact_dict["status"] = "new"
    contact_dict["created_at"] = datetime.utcnow()
    contact_dict["updated_at"] = datetime.utcnow()
    
    result = await db.contact_messages.insert_one(contact_dict)
    contact_dict["_id"] = str(result.inserted_id)
    
    logger.info(f"New contact message from {contact.email}")
    return {"message": "Message sent successfully", "id": str(result.inserted_id)}

# ===========================================
# ADMIN AUTHENTICATION ENDPOINTS
# ===========================================

@api_router.post("/admin/register", response_model=dict)
async def register_admin(admin: AdminCreate):
    # Check if admin already exists
    existing_admin = await db.admins.find_one({"email": admin.email})
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin with this email already exists"
        )
    
    # Hash password
    hashed_password = get_password_hash(admin.password)
    
    # Create admin
    admin_dict = {
        "username": admin.username,
        "email": admin.email,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db.admins.insert_one(admin_dict)
    logger.info(f"New admin registered: {admin.email}")
    
    return {"message": "Admin registered successfully", "id": str(result.inserted_id)}

@api_router.post("/admin/login", response_model=Token)
async def login_admin(admin: AdminLogin):
    # Find admin
    db_admin = await db.admins.find_one({"email": admin.email})
    if not db_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Verify password
    if not verify_password(admin.password, db_admin["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.email}, expires_delta=access_token_expires
    )
    
    logger.info(f"Admin logged in: {admin.email}")
    return {"access_token": access_token, "token_type": "bearer"}

@api_router.get("/admin/verify")
async def verify_token(current_admin: str = Depends(get_current_admin)):
    return {"email": current_admin, "authenticated": True}

# ===========================================
# ADMIN PROTECTED ENDPOINTS
# ===========================================

# Experience Management
@api_router.post("/admin/experience")
async def create_experience(
    experience: ExperienceCreate,
    current_admin: str = Depends(get_current_admin)
):
    exp_dict = experience.model_dump()
    exp_dict["created_at"] = datetime.utcnow()
    exp_dict["updated_at"] = datetime.utcnow()
    
    result = await db.experience.insert_one(exp_dict)
    exp_dict["_id"] = str(result.inserted_id)
    
    logger.info(f"Experience created by {current_admin}")
    return serialize_doc(exp_dict)

@api_router.put("/admin/experience/{exp_id}")
async def update_experience(
    exp_id: str,
    experience: ExperienceUpdate,
    current_admin: str = Depends(get_current_admin)
):
    if not ObjectId.is_valid(exp_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    update_data = {k: v for k, v in experience.model_dump(exclude_unset=True).items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db.experience.update_one(
        {"_id": ObjectId(exp_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Experience not found")
    
    updated_exp = await db.experience.find_one({"_id": ObjectId(exp_id)})
    logger.info(f"Experience {exp_id} updated by {current_admin}")
    return serialize_doc(updated_exp)

@api_router.delete("/admin/experience/{exp_id}")
async def delete_experience(
    exp_id: str,
    current_admin: str = Depends(get_current_admin)
):
    if not ObjectId.is_valid(exp_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    result = await db.experience.delete_one({"_id": ObjectId(exp_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Experience not found")
    
    logger.info(f"Experience {exp_id} deleted by {current_admin}")
    return {"message": "Experience deleted successfully"}

# Education Management
@api_router.post("/admin/education")
async def create_education(
    education: EducationCreate,
    current_admin: str = Depends(get_current_admin)
):
    edu_dict = education.model_dump()
    edu_dict["created_at"] = datetime.utcnow()
    edu_dict["updated_at"] = datetime.utcnow()
    
    result = await db.education.insert_one(edu_dict)
    edu_dict["_id"] = str(result.inserted_id)
    
    logger.info(f"Education created by {current_admin}")
    return serialize_doc(edu_dict)

@api_router.put("/admin/education/{edu_id}")
async def update_education(
    edu_id: str,
    education: EducationUpdate,
    current_admin: str = Depends(get_current_admin)
):
    if not ObjectId.is_valid(edu_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    update_data = {k: v for k, v in education.model_dump(exclude_unset=True).items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db.education.update_one(
        {"_id": ObjectId(edu_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Education not found")
    
    updated_edu = await db.education.find_one({"_id": ObjectId(edu_id)})
    logger.info(f"Education {edu_id} updated by {current_admin}")
    return serialize_doc(updated_edu)

@api_router.delete("/admin/education/{edu_id}")
async def delete_education(
    edu_id: str,
    current_admin: str = Depends(get_current_admin)
):
    if not ObjectId.is_valid(edu_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    result = await db.education.delete_one({"_id": ObjectId(edu_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Education not found")
    
    logger.info(f"Education {edu_id} deleted by {current_admin}")
    return {"message": "Education deleted successfully"}

# Project Management
@api_router.post("/admin/projects")
async def create_project(
    project: ProjectCreate,
    current_admin: str = Depends(get_current_admin)
):
    proj_dict = project.model_dump()
    proj_dict["created_at"] = datetime.utcnow()
    proj_dict["updated_at"] = datetime.utcnow()
    
    result = await db.projects.insert_one(proj_dict)
    proj_dict["_id"] = str(result.inserted_id)
    
    logger.info(f"Project created by {current_admin}")
    return serialize_doc(proj_dict)

@api_router.put("/admin/projects/{proj_id}")
async def update_project(
    proj_id: str,
    project: ProjectUpdate,
    current_admin: str = Depends(get_current_admin)
):
    if not ObjectId.is_valid(proj_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    update_data = {k: v for k, v in project.model_dump(exclude_unset=True).items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db.projects.update_one(
        {"_id": ObjectId(proj_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    
    updated_proj = await db.projects.find_one({"_id": ObjectId(proj_id)})
    logger.info(f"Project {proj_id} updated by {current_admin}")
    return serialize_doc(updated_proj)

@api_router.delete("/admin/projects/{proj_id}")
async def delete_project(
    proj_id: str,
    current_admin: str = Depends(get_current_admin)
):
    if not ObjectId.is_valid(proj_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    result = await db.projects.delete_one({"_id": ObjectId(proj_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    
    logger.info(f"Project {proj_id} deleted by {current_admin}")
    return {"message": "Project deleted successfully"}

# Certification Management
@api_router.post("/admin/certifications")
async def create_certification(
    certification: CertificationCreate,
    current_admin: str = Depends(get_current_admin)
):
    cert_dict = certification.model_dump()
    cert_dict["created_at"] = datetime.utcnow()
    cert_dict["updated_at"] = datetime.utcnow()
    
    result = await db.certifications.insert_one(cert_dict)
    cert_dict["_id"] = str(result.inserted_id)
    
    logger.info(f"Certification created by {current_admin}")
    return serialize_doc(cert_dict)

@api_router.put("/admin/certifications/{cert_id}")
async def update_certification(
    cert_id: str,
    certification: CertificationUpdate,
    current_admin: str = Depends(get_current_admin)
):
    if not ObjectId.is_valid(cert_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    update_data = {k: v for k, v in certification.model_dump(exclude_unset=True).items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db.certifications.update_one(
        {"_id": ObjectId(cert_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Certification not found")
    
    updated_cert = await db.certifications.find_one({"_id": ObjectId(cert_id)})
    logger.info(f"Certification {cert_id} updated by {current_admin}")
    return serialize_doc(updated_cert)

@api_router.delete("/admin/certifications/{cert_id}")
async def delete_certification(
    cert_id: str,
    current_admin: str = Depends(get_current_admin)
):
    if not ObjectId.is_valid(cert_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    result = await db.certifications.delete_one({"_id": ObjectId(cert_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Certification not found")
    
    logger.info(f"Certification {cert_id} deleted by {current_admin}")
    return {"message": "Certification deleted successfully"}

# Skill Management
@api_router.post("/admin/skills")
async def create_skill(
    skill: SkillCreate,
    current_admin: str = Depends(get_current_admin)
):
    skill_dict = skill.model_dump()
    skill_dict["created_at"] = datetime.utcnow()
    skill_dict["updated_at"] = datetime.utcnow()
    
    result = await db.skills.insert_one(skill_dict)
    skill_dict["_id"] = str(result.inserted_id)
    
    logger.info(f"Skill created by {current_admin}")
    return serialize_doc(skill_dict)

@api_router.put("/admin/skills/{skill_id}")
async def update_skill(
    skill_id: str,
    skill: SkillUpdate,
    current_admin: str = Depends(get_current_admin)
):
    if not ObjectId.is_valid(skill_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    update_data = {k: v for k, v in skill.model_dump(exclude_unset=True).items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db.skills.update_one(
        {"_id": ObjectId(skill_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    updated_skill = await db.skills.find_one({"_id": ObjectId(skill_id)})
    logger.info(f"Skill {skill_id} updated by {current_admin}")
    return serialize_doc(updated_skill)

@api_router.delete("/admin/skills/{skill_id}")
async def delete_skill(
    skill_id: str,
    current_admin: str = Depends(get_current_admin)
):
    if not ObjectId.is_valid(skill_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    result = await db.skills.delete_one({"_id": ObjectId(skill_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    logger.info(f"Skill {skill_id} deleted by {current_admin}")
    return {"message": "Skill deleted successfully"}

# Contact Messages Management
@api_router.get("/admin/contact")
async def get_all_messages(current_admin: str = Depends(get_current_admin)):
    messages = await db.contact_messages.find().sort("created_at", -1).to_list(100)
    return [serialize_doc(msg) for msg in messages]

@api_router.get("/admin/contact/{msg_id}")
async def get_message(
    msg_id: str,
    current_admin: str = Depends(get_current_admin)
):
    if not ObjectId.is_valid(msg_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    msg = await db.contact_messages.find_one({"_id": ObjectId(msg_id)})
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    
    # Mark as read
    await db.contact_messages.update_one(
        {"_id": ObjectId(msg_id)},
        {"$set": {"status": "read", "updated_at": datetime.utcnow()}}
    )
    
    return serialize_doc(msg)

@api_router.put("/admin/contact/{msg_id}")
async def update_message_status(
    msg_id: str,
    status: str,
    current_admin: str = Depends(get_current_admin)
):
    if not ObjectId.is_valid(msg_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    if status not in ["new", "read", "replied"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    result = await db.contact_messages.update_one(
        {"_id": ObjectId(msg_id)},
        {"$set": {"status": status, "updated_at": datetime.utcnow()}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Message not found")
    
    logger.info(f"Message {msg_id} status updated to {status} by {current_admin}")
    return {"message": "Status updated successfully"}

@api_router.delete("/admin/contact/{msg_id}")
async def delete_message(
    msg_id: str,
    current_admin: str = Depends(get_current_admin)
):
    if not ObjectId.is_valid(msg_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    result = await db.contact_messages.delete_one({"_id": ObjectId(msg_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Message not found")
    
    logger.info(f"Message {msg_id} deleted by {current_admin}")
    return {"message": "Message deleted successfully"}

# Include the router
app.include_router(api_router)

# Shutdown event
@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
