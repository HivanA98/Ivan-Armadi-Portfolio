from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# Experience Model
class ExperienceBase(BaseModel):
    title: str
    company: str
    location: str
    period: str
    type: str
    description: str
    projects: List[str]
    technologies: List[str]
    achievements: Optional[List[str]] = []
    order: int = 0

class ExperienceCreate(ExperienceBase):
    pass

class ExperienceUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    period: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    projects: Optional[List[str]] = None
    technologies: Optional[List[str]] = None
    achievements: Optional[List[str]] = None
    order: Optional[int] = None

class Experience(ExperienceBase):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# Education Model
class EducationBase(BaseModel):
    degree: str
    institution: str
    location: str
    period: str
    status: str
    description: str
    order: int = 0

class EducationCreate(EducationBase):
    pass

class EducationUpdate(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    location: Optional[str] = None
    period: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None

class Education(EducationBase):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# Project Model
class ProjectBase(BaseModel):
    title: str
    category: str
    description: str
    image: str
    technologies: List[str]
    highlights: List[str]
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    order: int = 0

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    technologies: Optional[List[str]] = None
    highlights: Optional[List[str]] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    order: Optional[int] = None

class Project(ProjectBase):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# Certification Model
class CertificationBase(BaseModel):
    title: str
    issuer: str
    date: str
    image: str
    credential_url: str
    description: str
    order: int = 0

class CertificationCreate(CertificationBase):
    pass

class CertificationUpdate(BaseModel):
    title: Optional[str] = None
    issuer: Optional[str] = None
    date: Optional[str] = None
    image: Optional[str] = None
    credential_url: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None

class Certification(CertificationBase):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# Skill Model
class SkillBase(BaseModel):
    category: str
    icon: str
    items: List[str]
    order: int = 0

class SkillCreate(SkillBase):
    pass

class SkillUpdate(BaseModel):
    category: Optional[str] = None
    icon: Optional[str] = None
    items: Optional[List[str]] = None
    order: Optional[int] = None

class Skill(SkillBase):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# Contact Message Model
class ContactMessageBase(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

class ContactMessageCreate(ContactMessageBase):
    pass

class ContactMessage(ContactMessageBase):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    status: str = "new"  # new, read, replied
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# Admin Model
class AdminBase(BaseModel):
    username: str
    email: EmailStr

class AdminCreate(AdminBase):
    password: str

class Admin(AdminBase):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None