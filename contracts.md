# Ivan Armadi Portfolio - Backend Integration Contracts

## Overview
This document outlines the API contracts and integration plan between the frontend and backend for the portfolio CMS system.

## Current Mock Data Location
- `/app/frontend/src/mock.js` contains all mock data for:
  - Personal Information
  - Skills (4 categories)
  - Work Experience (6 positions)
  - Education (2 entries)
  - Projects (8 projects)
  - Certifications (3 certifications)
  - Testimonials (2 testimonials)

## Database Models

### 1. Experience
```javascript
{
  _id: ObjectId,
  title: String,
  company: String,
  location: String,
  period: String,
  type: String,
  description: String,
  projects: [String],
  technologies: [String],
  achievements: [String],
  order: Number,
  createdAt: Date,
  updatedAt: Date
}
```

### 2. Education
```javascript
{
  _id: ObjectId,
  degree: String,
  institution: String,
  location: String,
  period: String,
  status: String,
  description: String,
  order: Number,
  createdAt: Date,
  updatedAt: Date
}
```

### 3. Project
```javascript
{
  _id: ObjectId,
  title: String,
  category: String,
  description: String,
  image: String,
  technologies: [String],
  highlights: [String],
  githubUrl: String (optional),
  liveUrl: String (optional),
  order: Number,
  createdAt: Date,
  updatedAt: Date
}
```

### 4. Certification
```javascript
{
  _id: ObjectId,
  title: String,
  issuer: String,
  date: String,
  image: String,
  credentialUrl: String,
  description: String,
  order: Number,
  createdAt: Date,
  updatedAt: Date
}
```

### 5. Skill
```javascript
{
  _id: ObjectId,
  category: String,
  icon: String,
  items: [String],
  order: Number,
  createdAt: Date,
  updatedAt: Date
}
```

### 6. ContactMessage
```javascript
{
  _id: ObjectId,
  name: String,
  email: String,
  subject: String,
  message: String,
  status: String (enum: ['new', 'read', 'replied']),
  createdAt: Date,
  updatedAt: Date
}
```

### 7. Admin
```javascript
{
  _id: ObjectId,
  username: String (unique),
  email: String (unique),
  password: String (hashed),
  createdAt: Date,
  updatedAt: Date
}
```

## API Endpoints

### Public Endpoints (No Auth Required)

#### Experience
- `GET /api/experience` - Get all experiences (sorted by order)
- `GET /api/experience/:id` - Get single experience

#### Education
- `GET /api/education` - Get all education entries (sorted by order)
- `GET /api/education/:id` - Get single education entry

#### Projects
- `GET /api/projects` - Get all projects (sorted by order)
- `GET /api/projects/:id` - Get single project
- `GET /api/projects/category/:category` - Get projects by category

#### Certifications
- `GET /api/certifications` - Get all certifications (sorted by order)
- `GET /api/certifications/:id` - Get single certification

#### Skills
- `GET /api/skills` - Get all skills (sorted by order)
- `GET /api/skills/:id` - Get single skill

#### Contact
- `POST /api/contact` - Submit contact form
  Request Body:
  ```javascript
  {
    name: String,
    email: String,
    subject: String,
    message: String
  }
  ```

### Admin Endpoints (Auth Required)

#### Authentication
- `POST /api/admin/login` - Admin login
  Request Body:
  ```javascript
  {
    email: String,
    password: String
  }
  ```
  Response:
  ```javascript
  {
    token: String,
    admin: { id, username, email }
  }
  ```

- `POST /api/admin/register` - Register admin (first time only)
- `GET /api/admin/verify` - Verify JWT token

#### Experience Management
- `POST /api/admin/experience` - Create new experience
- `PUT /api/admin/experience/:id` - Update experience
- `DELETE /api/admin/experience/:id` - Delete experience

#### Education Management
- `POST /api/admin/education` - Create new education
- `PUT /api/admin/education/:id` - Update education
- `DELETE /api/admin/education/:id` - Delete education

#### Project Management
- `POST /api/admin/projects` - Create new project
- `PUT /api/admin/projects/:id` - Update project
- `DELETE /api/admin/projects/:id` - Delete project

#### Certification Management
- `POST /api/admin/certifications` - Create new certification
- `PUT /api/admin/certifications/:id` - Update certification
- `DELETE /api/admin/certifications/:id` - Delete certification

#### Skill Management
- `POST /api/admin/skills` - Create new skill
- `PUT /api/admin/skills/:id` - Update skill
- `DELETE /api/admin/skills/:id` - Delete skill

#### Contact Messages
- `GET /api/admin/contact` - Get all contact messages
- `GET /api/admin/contact/:id` - Get single message
- `PUT /api/admin/contact/:id` - Update message status
- `DELETE /api/admin/contact/:id` - Delete message

## Frontend Integration Plan

### Step 1: Create API Service Layer
Create `/app/frontend/src/services/api.js` with:
- Axios instance with base URL
- API methods for all endpoints
- Error handling
- JWT token management

### Step 2: Update Components
Replace mock data imports with API calls in:
- `Hero.jsx` - No API needed (static info)
- `Skills.jsx` - Fetch from `/api/skills`
- `Experience.jsx` - Fetch from `/api/experience`
- `Education.jsx` - Fetch from `/api/education`
- `Projects.jsx` - Fetch from `/api/projects`
- `Certifications.jsx` - Fetch from `/api/certifications`
- `Contact.jsx` - POST to `/api/contact`

### Step 3: Create Admin Panel
Create admin interface at `/admin` route with:
- Login page
- Dashboard with stats
- CRUD interfaces for each content type
- Contact messages viewer

### Step 4: State Management
Use React Context or keep component-level state for simplicity.

## Authentication Flow

1. Admin navigates to `/admin`
2. Login form submits to `/api/admin/login`
3. Backend validates credentials and returns JWT token
4. Frontend stores token in localStorage
5. All admin API calls include token in Authorization header
6. Backend middleware verifies token for protected routes

## Data Migration

Initial data from `mock.js` will be seeded into MongoDB when backend starts (if collections are empty).

## Error Handling

- Frontend displays user-friendly error messages
- Backend returns consistent error format:
  ```javascript
  {
    error: String,
    message: String,
    statusCode: Number
  }
  ```

## Testing Checklist

### Backend Tests
- [ ] All public endpoints return correct data
- [ ] Admin login works correctly
- [ ] JWT authentication works
- [ ] CRUD operations work for all models
- [ ] Contact form submission works
- [ ] Data validation works

### Frontend Integration Tests
- [ ] Data loads correctly from API
- [ ] Contact form submits successfully
- [ ] Admin login works
- [ ] Admin can create/update/delete content
- [ ] Changes reflect immediately on public site

### Mobile Responsive Tests
- [ ] All views work on mobile (375px)
- [ ] All views work on tablet (768px)
- [ ] All views work on desktop (1920px)
