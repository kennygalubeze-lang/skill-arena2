# SkillArena - Deployment-ready Package (lightweight)

This package is deployment-ready for Render (auto-detects `render.yaml`) and for local Docker Compose testing.

## Quick start (Render)
1. Push this repository to GitHub.
2. On Render.com, create a new service and connect your GitHub repo. Render will read `render.yaml` and deploy backend + frontend.
3. Backend (FastAPI) will auto-seed an admin user:
   - email: admin@skillarena.com
   - password: SkillArena@2025
4. For production use replace `DATABASE_URL` with a managed Postgres and set a strong `JWT_SECRET`.

## Local testing (Docker)
```
docker compose -f docker-compose.prod.yml up --build
```
Frontend: http://localhost:3000 (nginx), Backend: http://localhost:8000

Support:
- WhatsApp: +2347011695248
- Call: +2347053070533
- Email: kennygalubeze@gmail.com
