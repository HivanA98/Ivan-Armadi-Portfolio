"""
Data seeding script to populate MongoDB with initial portfolio data
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initial data based on mock.js
skills_data = [
    {
        "category": "QA Engineering",
        "icon": "ShieldCheck",
        "items": [
            "Manual Testing",
            "Automation Testing",
            "Katalon Studio",
            "Selenium",
            "API Testing (Postman)",
            "Performance Testing (JMeter)",
            "Test Case Design",
            "Bug Tracking (JIRA)",
            "ISTQB Certified",
            "Regression Testing",
            "UAT Coordination"
        ],
        "order": 1
    },
    {
        "category": "Web Development",
        "icon": "Code",
        "items": [
            "HTML5/CSS3",
            "JavaScript",
            "React.js",
            "Node.js",
            "Python (Django/Flask)",
            "RESTful APIs",
            "Git/GitHub",
            "Responsive Design",
            "Database (MySQL, MongoDB)"
        ],
        "order": 2
    },
    {
        "category": "Mobile Development",
        "icon": "Smartphone",
        "items": [
            "Android Development",
            "iOS Testing",
            "React Native",
            "Mobile UI/UX Testing",
            "App Performance Testing",
            "Cross-platform Testing"
        ],
        "order": 3
    },
    {
        "category": "Data Science",
        "icon": "BarChart3",
        "items": [
            "Python (Pandas, NumPy)",
            "Data Analysis",
            "Data Visualization",
            "SQL",
            "Test Data Management",
            "Statistical Analysis"
        ],
        "order": 4
    }
]

experience_data = [
    {
        "title": "QA Engineer (Founding Team)",
        "company": "Onkas",
        "location": "Jakarta",
        "period": "September 2025 - Present",
        "type": "Startup",
        "description": "Established the initial QA foundation for a new startup, setting up testing environment, configuring tools, and creating reusable test data.",
        "projects": [
            "Enabled consistent regression cycles and reduced setup time for future modules",
            "Set up complete testing infrastructure from scratch"
        ],
        "technologies": ["QA Foundation", "Test Environment Setup", "Test Data Management"],
        "achievements": [
            "Built QA foundation from ground up",
            "Reduced setup time for future testing"
        ],
        "order": 1
    },
    {
        "title": "QA Engineer (Freelance)",
        "company": "Bayerische Motoren Werke (BMW)",
        "location": "Jakarta",
        "period": "August 2025",
        "type": "Automotive",
        "description": "Executed end-to-end smoke and regression testing on web after system migration. Led defect triage for migration regressions and configuration gaps.",
        "projects": [
            "Built and maintained Confluence-based test documentation with end-to-end traceability",
            "Coordinated retests and verified fixes for system migration",
            "Provided go/no-go reports for release decision-making"
        ],
        "technologies": ["Confluence", "Web Testing", "Defect Triage", "Migration Testing"],
        "achievements": [
            "Discovered and logged 150+ defects",
            "Reduced post-release incidents",
            "Accelerated decision-making for safer releases"
        ],
        "order": 2
    },
    {
        "title": "UAT Tester",
        "company": "Wistkey",
        "location": "Hong Kong",
        "period": "February 2024 - March 2025",
        "type": "Software House",
        "description": "Led SIT and UAT for Green Hoop and Soso Mall applications. Developed automated test scripts and performed comprehensive manual testing across web and mobile platforms.",
        "projects": [
            "Green Hoop App: Analyzed 10+ business requirements, produced comprehensive SIT test plans, developed 150+ automated test scripts",
            "Soso Mall: Backend testing on Magento, designed 30+ test scenarios for Android & iOS, comprehensive web testing"
        ],
        "technologies": ["Katalon Studio", "Magento", "Android", "iOS", "API Testing", "Postman"],
        "achievements": [
            "Reduced manual testing time by 30%",
            "Uncovered 20+ critical bugs in Green Hoop",
            "Closed over 200 test tickets",
            "Improved product quality by 50%",
            "Detected 10+ critical issues in Soso Mall affecting payment and product synchronization",
            "Identified 100+ defects before deployment"
        ],
        "order": 3
    },
    {
        "title": "IT Quality Assurance",
        "company": "Nusatrip",
        "location": "Jakarta",
        "period": "August 2023 - December 2023",
        "type": "Travel Technology",
        "description": "Performed payment testing for B2B and B2C flight & hotel bookings. Executed API-based booking tests and validated data in database records using SQL.",
        "projects": [
            "Payment testing across multiple methods (bank transfer, credit card, deposit, vouchers)",
            "API-based booking tests with Postman",
            "Database validation using DBeaver and SQL",
            "System logs analysis using Linux environment and PuTTY"
        ],
        "technologies": ["Postman", "SQL", "DBeaver", "Linux", "PuTTY", "API Testing"],
        "achievements": [
            "Identified 50+ defects in Revamp project",
            "Ensured accurate third-party integrations",
            "Improved system stability and data integrity",
            "Reduced customer impact"
        ],
        "order": 4
    },
    {
        "title": "QA Tester",
        "company": "Bank Rakyat Indonesia",
        "location": "Jakarta",
        "period": "August 2022 - August 2023",
        "type": "Banking",
        "description": "Executed and documented SIT, BA UAT, BADT, and BAPT for retail and corporate banking journeys. Designed API tests and validated end-to-end data in core banking modules.",
        "projects": [
            "Created test cases and evidence, logged defects in Jira",
            "Designed and executed API tests in Postman for internal services and partner integrations",
            "Validated end-to-end data in core banking and back office modules",
            "Managed SIT and UAT datasets and environments"
        ],
        "technologies": ["Jira", "Postman", "Core Banking", "API Testing", "SQL"],
        "achievements": [
            "Achieved on-time sign off for six modules",
            "Reduced sanity regression time by 30%",
            "Prevented data errors from reaching production",
            "Increased stakeholder confidence"
        ],
        "order": 5
    },
    {
        "title": "QA Engineer Intern",
        "company": "Eduwork.id",
        "location": "Jakarta",
        "period": "May 2022 - August 2022",
        "type": "EdTech",
        "description": "Executed manual and automated mobile testing using Appium and Katalon Studio. Developed web UI automation using Katalon Studio and Cypress.",
        "projects": [
            "Mobile testing using Appium and Katalon Studio",
            "Web UI automation using Cypress",
            "Authored detailed test cases and execution reports"
        ],
        "technologies": ["Appium", "Katalon Studio", "Cypress", "Mobile Testing"],
        "achievements": [
            "Ensured functionality across diverse devices",
            "Improved test efficiency and repeatability",
            "Facilitated knowledge transfer"
        ],
        "order": 6
    }
]

education_data = [
    {
        "degree": "Bachelor of Science (B.Sc) - Biology",
        "institution": "Indonesia Open University",
        "location": "Jakarta, Indonesia",
        "period": "October 2023 - August 2026",
        "status": "Currently Enrolled",
        "description": "Transferred from Surya University. Completed literature review on therapeutic potential of bacteriophages against resistant Staphylococcus aureus.",
        "order": 1
    },
    {
        "degree": "Bachelor Degree - Biotechnology",
        "institution": "Surya University",
        "location": "Tangerang, Indonesia",
        "period": "August 2020 - May 2022",
        "status": "Transferred",
        "description": "Studied biotechnology before transferring to Indonesia Open University due to university closure.",
        "order": 2
    }
]

projects_data = [
    {
        "title": "Green Hoop App Testing",
        "category": "QA Engineering",
        "description": "Comprehensive SIT and UAT for mobile sustainability application at Wistkey. Developed 150+ automated test scripts for web and mobile platforms.",
        "image": "https://images.unsplash.com/photo-1551650975-87deedd944c3?w=800&q=80",
        "technologies": ["Katalon Studio", "Android", "iOS", "Web Testing"],
        "highlights": [
            "Analyzed 10+ business requirements and Figma designs",
            "Developed 150+ automated test scripts",
            "Reduced manual testing time by 30%",
            "Uncovered 20+ critical bugs",
            "Closed over 200 test tickets",
            "Improved product quality by 50%"
        ],
        "github_url": None,
        "live_url": None,
        "order": 1
    },
    {
        "title": "SoSomall E-commerce QA",
        "category": "QA Engineering",
        "description": "Backend testing on Magento and comprehensive mobile testing for Android & iOS e-commerce platform.",
        "image": "https://images.unsplash.com/photo-1557821552-17105176677c?w=800&q=80",
        "technologies": ["Magento", "Katalon Studio", "Android", "iOS"],
        "highlights": [
            "Designed 30+ test scenarios for mobile platforms",
            "Detected 10+ critical issues affecting payment",
            "Identified 100+ defects before deployment",
            "Ensured cross-platform functionality",
            "Mitigated potential revenue loss"
        ],
        "github_url": None,
        "live_url": None,
        "order": 2
    },
    {
        "title": "BMW System Migration Testing",
        "category": "QA Engineering",
        "description": "End-to-end smoke and regression testing for BMW web system after migration. Built comprehensive test documentation.",
        "image": "https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?w=800&q=80",
        "technologies": ["Confluence", "Web Testing", "Defect Triage"],
        "highlights": [
            "Discovered and logged 150+ defects",
            "Built Confluence-based test documentation",
            "Reduced post-release incidents",
            "Provided go/no-go reports for releases"
        ],
        "github_url": None,
        "live_url": None,
        "order": 3
    },
    {
        "title": "Nusatrip Payment Testing",
        "category": "QA Engineering",
        "description": "Comprehensive payment testing for B2B and B2C flight & hotel bookings with API and database validation.",
        "image": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=800&q=80",
        "technologies": ["Postman", "SQL", "DBeaver", "Linux"],
        "highlights": [
            "Tested multiple payment methods",
            "Identified 50+ defects in Revamp project",
            "Ensured third-party integration accuracy",
            "Improved system stability"
        ],
        "github_url": None,
        "live_url": None,
        "order": 4
    },
    {
        "title": "Cypress Automation Framework",
        "category": "Web Development",
        "description": "Developed end-to-end web automation tests for UI interactions and functional testing using Cypress.",
        "image": "https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?w=800&q=80",
        "technologies": ["Cypress", "JavaScript", "Mocha", "Chai"],
        "highlights": [
            "End-to-end UI testing automation",
            "Functional test coverage",
            "Reusable test framework"
        ],
        "github_url": "#",
        "live_url": None,
        "order": 5
    },
    {
        "title": "Katalon Studio Automation",
        "category": "QA Engineering",
        "description": "Automated Web UI, Mobile, and API testing using Katalon Studio with TestOps integration.",
        "image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&q=80",
        "technologies": ["Katalon Studio", "Selenium", "Katalon TestOps"],
        "highlights": [
            "Multi-platform automation",
            "TestOps integration",
            "Comprehensive test coverage"
        ],
        "github_url": "#",
        "live_url": None,
        "order": 6
    },
    {
        "title": "Data Science - ML & Visualization",
        "category": "Data Science",
        "description": "Built data cleaning and machine learning models with Flask API integration for deployment.",
        "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&q=80",
        "technologies": ["Python", "Pandas", "Flask", "Scikit-Learn", "MySQL"],
        "highlights": [
            "Machine learning model development",
            "Flask API integration",
            "Data visualization with Seaborn & Matplotlib",
            "MySQL database integration"
        ],
        "github_url": "#",
        "live_url": None,
        "order": 7
    },
    {
        "title": "Robot Framework Automation",
        "category": "Web Development",
        "description": "Developed Web UI automation test using Robot Framework and Selenium Library.",
        "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&q=80",
        "technologies": ["Robot Framework", "Selenium", "Python"],
        "highlights": [
            "Web UI automation",
            "Selenium Library integration",
            "Python-based test framework"
        ],
        "github_url": "#",
        "live_url": None,
        "order": 8
    }
]

certifications_data = [
    {
        "title": "Katalon Expert Level Certification",
        "issuer": "Katalon Academy",
        "date": "April 2023",
        "image": "https://hivana98.github.io/Ivan-Armadi-Portfolio/Data/Assets/Picture/badge-expert.png",
        "credential_url": "https://academy.katalon.com/mcertificate/64584df06b92e",
        "description": "Expert-level certification demonstrating advanced proficiency in Katalon Studio for test automation.",
        "order": 1
    },
    {
        "title": "ISTQB Certified Tester Foundation Level",
        "issuer": "ISTQB",
        "date": "March 2023",
        "image": "https://hivana98.github.io/Ivan-Armadi-Portfolio/Data/Assets/Picture/ISTQB.png",
        "credential_url": "#",
        "description": "Foundation Level certification in software testing principles and best practices.",
        "order": 2
    },
    {
        "title": "Data Science Bootcamp",
        "issuer": "Binar Academy",
        "date": "June 2024",
        "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&q=80",
        "credential_url": "#",
        "description": "Intensive bootcamp covering machine learning, data visualization, and data analysis techniques.",
        "order": 3
    }
]

async def seed_database():
    print("Starting database seeding...")
    
    # Check if data already exists
    skills_count = await db.skills.count_documents({})
    if skills_count > 0:
        print(f"Database already contains {skills_count} skills. Skipping seed.")
        return
    
    # Insert skills
    print("Seeding skills...")
    await db.skills.insert_many(skills_data)
    print(f"✅ Inserted {len(skills_data)} skills")
    
    # Insert experience
    print("Seeding experience...")
    await db.experience.insert_many(experience_data)
    print(f"✅ Inserted {len(experience_data)} experience entries")
    
    # Insert education
    print("Seeding education...")
    await db.education.insert_many(education_data)
    print(f"✅ Inserted {len(education_data)} education entries")
    
    # Insert projects
    print("Seeding projects...")
    await db.projects.insert_many(projects_data)
    print(f"✅ Inserted {len(projects_data)} projects")
    
    # Insert certifications
    print("Seeding certifications...")
    await db.certifications.insert_many(certifications_data)
    print(f"✅ Inserted {len(certifications_data)} certifications")
    
    print("\n✅ Database seeding completed successfully!")
    print("\nNext steps:")
    print("1. Register an admin user at: POST /api/admin/register")
    print("2. Login to get JWT token at: POST /api/admin/login")
    print("3. Use the token to manage content via admin endpoints")

if __name__ == "__main__":
    asyncio.run(seed_database())
    client.close()
