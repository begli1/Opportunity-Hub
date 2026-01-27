# Opportunity Hub

A platform for students to discover and apply to internships, clubs, volunteering opportunities, and tutoring positions.

## Project Structure

```
.
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── main.py   # Main API application
│   │   ├── models.py # Database models
│   │   └── schemas.py # Pydantic schemas
│   └── requirements.txt
└── frontend/         # Vue.js frontend
    ├── src/
    └── package.json
```

## Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Deployment

### Backend (Render)
- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Environment Variables:
  - `DATABASE_URL` (provided by Render PostgreSQL)
  - `SECRET_KEY`
  - `OPENAI_API_KEY`
  - `RESEND_API_KEY`
  - `CONTACT_EMAIL`

### Frontend (Vercel)
- Root Directory: `frontend`
- Build Command: `npm install && npm run build`
- Output Directory: `dist`
- Environment Variables:
  - `VITE_API_URL` (your Render backend URL, e.g., `https://your-backend.onrender.com`)

## Environment Variables

Create a `.env` file in the `backend` directory:
```
DATABASE_URL=postgresql+asyncpg://...
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
RESEND_API_KEY=your-resend-key
CONTACT_EMAIL=your-email@example.com
```
