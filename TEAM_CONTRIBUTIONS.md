# Team Contributions & Hours Log
## Opportunity Hub - TSA Webmaster 2025-26

---

## Begli Pirmuhammedov (Team Leader)
**Total Hours: ~200 hours**
**Role: Full Stack Developer, Project Architect**

### Backend Development (~100 hours)
- **API Architecture & Setup** (15 hours)
  - Designed and implemented FastAPI application structure
  - Set up SQLAlchemy ORM with async PostgreSQL database
  - Configured authentication system with JWT tokens
  - Implemented dependency injection for database sessions and user authentication

- **User Authentication System** (12 hours)
  - Built user registration with email validation and password hashing (bcrypt)
  - Implemented JWT token-based login system
  - Created token refresh and expiration logic
  - Added rate limiting to prevent abuse

- **Opportunity Management System** (20 hours)
  - Created CRUD endpoints for posting, editing, and deleting opportunities
  - Implemented search and filtering (by type, location, tags, keywords)
  - Built duplicate detection system using content hashing
  - Added deadline tracking and auto-closing functionality
  - Created saved opportunities/bookmarking system

- **Application System** (15 hours)
  - Built application submission endpoint with validation
  - Created application inbox for opportunity creators
  - Implemented application approval/rejection workflow
  - Added application status tracking and decision reasons

- **Moderation System** (18 hours)
  - Integrated OpenAI API for AI-powered content moderation
  - Built appeal system for flagged posts
  - Created moderator dashboard with appeals, reports, and external URL review
  - Implemented report system with duplicate prevention
  - Added external URL moderation workflow

- **Email Integration** (8 hours)
  - Integrated Resend API for contact form emails
  - Configured email templates with user information
  - Set up environment-based domain configuration

- **Database Design & Migrations** (10 hours)
  - Designed database schema for users, opportunities, applications, reports
  - Created relationships and foreign keys
  - Migrated from SQLite to PostgreSQL for production
  - Added indexes for performance optimization

- **Deployment & DevOps** (12 hours)
  - Configured Render backend deployment
  - Set up environment variables and secrets management
  - Fixed CORS configuration for production
  - Debugged and resolved deployment issues

### Frontend Development (~85 hours)
- **Vue.js Application Setup** (8 hours)
  - Configured Vite build system
  - Set up Vue Router with protected routes
  - Created authentication store with Pinia/Composition API
  - Implemented API client with Axios interceptors

- **Authentication Pages** (10 hours)
  - Built login page with form validation
  - Created signup page with email validation
  - Implemented error handling and user feedback
  - Added token management and auto-logout on expiration

- **Dashboard & Navigation** (15 hours)
  - Designed and built main dashboard with opportunity cards
  - Implemented search and filter functionality
  - Created responsive navigation with mobile hamburger menu
  - Built user profile dropdown and logout functionality

- **Opportunity Management UI** (18 hours)
  - Created "My Posts" page with edit/delete functionality
  - Built opportunity creation form with all fields
  - Implemented tag system and deadline picker
  - Added external URL input with moderation status indicators
  - Created appeal interface for flagged posts

- **Application System UI** (12 hours)
  - Built application submission form
  - Created application inbox for post creators
  - Implemented application approval/rejection interface
  - Added application status tracking and filtering

- **Moderation Dashboard** (15 hours)
  - Created comprehensive moderator interface
  - Built tabs for appeals, reports, and external URLs
  - Implemented decision modals with response fields
  - Added real-time data refresh functionality

- **Landing & Information Pages** (12 hours)
  - Designed and built Prelogin landing page with hero section
  - Created About Us page with mission, vision, and features
  - Built References page with technology stack documentation
  - Implemented responsive design for all pages

- **Styling & UI/UX** (15 hours)
  - Created cohesive design system with CSS variables
  - Implemented gradient themes and modern card designs
  - Built responsive layouts for mobile, tablet, and desktop
  - Added animations, transitions, and hover effects
  - Ensured accessibility with semantic HTML and ARIA labels

### Testing & Debugging (~15 hours)
- Tested all user flows (registration, login, posting, applying)
- Debugged timezone issues in date displays
- Fixed CORS and deployment issues
- Resolved mobile responsiveness problems
- Tested moderation workflows and edge cases

---

## Jabari Myers
**Total Hours: ~18 hours**
**Role: Frontend Developer**

### Frontend Development (18 hours)
- **Component Development** (8 hours)
  - Assisted with styling and layout of dashboard components
  - Helped implement responsive card designs for opportunity listings
  - Contributed to mobile navigation menu styling
  - Worked on form input styling and validation feedback

- **UI Refinement** (6 hours)
  - Refined color schemes and spacing in various components
  - Improved button styles and hover effects
  - Enhanced visual consistency across pages
  - Adjusted typography and text hierarchy

- **Responsive Design** (4 hours)
  - Tested and fixed mobile viewport issues
  - Adjusted breakpoints for tablet and mobile layouts
  - Ensured proper display on various screen sizes
  - Fixed navbar collapse behavior on mobile devices

---

## Benjamin Popma
**Total Hours: ~17 hours**
**Role: Frontend Developer**

### Frontend Development (17 hours)
- **Component Development** (7 hours)
  - Assisted with building reusable Vue components
  - Helped implement modal dialogs for forms and confirmations
  - Contributed to footer component design and functionality
  - Worked on loading states and error message displays

- **User Interface Design** (6 hours)
  - Designed and implemented card layouts for opportunity displays
  - Created tag/pill components for categories and filters
  - Enhanced form layouts and input field designs
  - Improved visual feedback for user actions

- **Responsive Design & Testing** (4 hours)
  - Tested application across different browsers
  - Fixed cross-browser compatibility issues
  - Adjusted CSS for better mobile experience
  - Ensured consistent styling across all pages

---

## Kanishaka Madan
**Total Hours: ~16 hours**
**Role: Backend Developer**

### Backend Development (16 hours)
- **API Endpoint Development** (8 hours)
  - Assisted with implementing GET endpoints for opportunity listings
  - Helped create user profile endpoint (`/users/me`)
  - Contributed to saved opportunities endpoint
  - Worked on basic CRUD operations for opportunities

- **Database Integration** (5 hours)
  - Assisted with SQLAlchemy model definitions
  - Helped set up database relationships
  - Contributed to query optimization
  - Tested database operations and migrations

- **Testing & Documentation** (3 hours)
  - Tested API endpoints using Postman
  - Documented endpoint parameters and responses
  - Verified data validation and error handling
  - Tested authentication flow

---

## Nicolai Nunez
**Total Hours: ~16 hours**
**Role: Backend Developer**

### Backend Development (16 hours)
- **API Endpoint Development** (7 hours)
  - Assisted with POST endpoints for opportunity creation
  - Helped implement application submission endpoint
  - Contributed to update/delete endpoints
  - Worked on search and filter query parameters

- **Data Validation** (6 hours)
  - Assisted with Pydantic schema definitions
  - Helped implement input validation for forms
  - Contributed to error message formatting
  - Worked on data sanitization and security checks

- **Testing & Debugging** (3 hours)
  - Tested API endpoints for edge cases
  - Verified error handling and status codes
  - Tested rate limiting functionality
  - Debugged database connection issues

---

## Total Project Hours: ~267 hours

### Technology Stack Summary
- **Frontend:** Vue.js 3, Vue Router, Axios, Vite, HTML5, CSS3, JavaScript (ES6+)
- **Backend:** FastAPI, Python 3, SQLAlchemy, PostgreSQL, Pydantic, JWT, bcrypt
- **APIs & Services:** OpenAI (moderation), Resend (email)
- **Deployment:** Vercel (frontend), Render (backend), PostgreSQL (database)
- **Tools:** Git, VS Code/Cursor, Postman, Chrome DevTools

### Key Features Implemented
1. User authentication and authorization
2. Opportunity posting and management
3. Search and filtering system
4. Application submission and tracking
5. AI-powered content moderation
6. Appeal system for flagged content
7. Report system for inappropriate content
8. External URL moderation
9. Email contact system
10. Responsive design for all devices
11. Moderator dashboard
12. Saved opportunities/bookmarking

---

*This document represents the collaborative effort of Team 5792 for the TSA Webmaster 2025-26 competition.*
