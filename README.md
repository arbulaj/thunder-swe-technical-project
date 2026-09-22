# Oklahoma City Thunder — Lineup Analytics

**Full-stack basketball analytics dashboard | Python · Django REST Framework · PostgreSQL · Angular · TypeScript**

A full-stack application for exploring how different player combinations perform across offensive and defensive possessions. I built this project as part of an Oklahoma City Thunder software engineering technical assessment, extending a provided application skeleton into an analytics workflow with API-driven lineup statistics and an interactive frontend.

> **My contribution:** Implementing and testing lineup-analysis functionality, connecting the frontend to the API, adding ways to explore different lineup sizes, and working through deployment of the application. The original assignment and starter code were provided; the features described below are my project work.

## What I built

### Backend and data
- Worked with **Python, Django REST Framework, and PostgreSQL** to serve basketball lineup data through a REST API.
- Developed lineup-statistics functionality for **1–5-player combinations**, using possession-level offensive and defensive data.
- Added lineup performance measures, including **offensive rating, defensive rating, and net rating**.
- Implemented and tested API query behavior for different lineup sizes.

### Frontend
- Built an **Angular/TypeScript** interface for exploring lineup performance.
- Connected frontend components to the backend API and displayed lineup statistics in an interactive dashboard.
- Added data-exploration features including **search, sorting, and pagination**.

### Testing and deployment
- Tested API responses and query parameters while debugging backend/frontend integration.
- Worked with **Railway** to deploy the frontend, backend, and PostgreSQL services.

## Technology stack

| Area | Technologies |
| --- | --- |
| Backend | Python, Django, Django REST Framework |
| Frontend | Angular, TypeScript, HTML, SCSS |
| Database | PostgreSQL |
| API | REST, JSON |
| Deployment | Railway |
| Development | Git, GitHub, Windows, PowerShell |

## How the application works

```text
Possession-level data
        ↓
PostgreSQL / backend data processing
        ↓
Django REST API — /api/v1/lineups
        ↓
Angular dashboard
        ↓
Explore lineup sizes, compare ratings, search and sort results
```

The API aggregates statistics for player combinations; the frontend makes those results easier to inspect and compare. **Net rating** is the difference between offensive and defensive rating, offering a concise view of a lineup's performance in the sample data.

## Explore the project

- **Code:** This repository
- **Live application:** Add your verified deployed frontend URL here.
- **Demo video:** Add your screen-recording link here.
- **Screenshots:** Add dashboard screenshots here.

<!-- Once you have a screenshot committed to the repo, replace this comment with: ![Lineup analytics dashboard](path/to/screenshot.png) -->

## Run locally

The project contains separate `backend/` and `frontend/` directories. Set up PostgreSQL and the environment variables required by the backend before starting the services.

**Backend**
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Frontend**
```bash
cd frontend
npm install
npm start
```

Frontend: `http://localhost:4200/`  
API: `http://localhost:8000/api/v1/lineups`

Refer to the [original assessment instructions](ASSESSMENT_INSTRUCTIONS.md) for the provided data-ingestion and deployment setup. The original assignment requested backend engineering, frontend engineering, written basketball analysis, and a deployed demo; those instructions are retained for context rather than presented as work I independently designed.

## What I learned

This project gave me practical experience moving between a relational database, a Python API, and a TypeScript frontend. I worked through API query design, aggregation of structured data, integration debugging, and presenting technical output in a way that a non-developer can explore.

## Assessment and attribution

This repository began with a technical assessment and starter project supplied by the Oklahoma City Thunder. This README describes my implementation and learning, not authorship of the original assignment or starter code. The original instructions are preserved in [`ASSESSMENT_INSTRUCTIONS.md`](ASSESSMENT_INSTRUCTIONS.md). Any AI-assistance disclosure required by the assessment should remain in the existing `prompts/` directory.
