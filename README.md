# FastAPI Blog API

A production-ready REST API for a blogging platform built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL** — featuring JWT authentication, user management, and full CRUD operations for blog posts. Deployed live on Render.

[![Live API](https://img.shields.io/badge/Live%20API-Render-46E3B7?style=flat&logo=render)](https://fast-api-ra11.onrender.com/docs)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)

---

## Live Demo

> **Interactive API Docs:** [https://fast-api-ra11.onrender.com/docs](https://fast-api-ra11.onrender.com/docs)

Explore and test every endpoint directly from the browser using FastAPI's built-in Swagger UI.

---

## Features

- **JWT Authentication** — Secure login with bearer tokens via OAuth2 password flow
- **User Management** — Register and authenticate users with bcrypt-hashed passwords
- **Blog CRUD** — Create, read, update, and delete blog posts
- **Query Parameters** — Filter blog listings by publish status and limit results
- **Comments** — Fetch comments per blog post
- **PostgreSQL in production** — SQLAlchemy ORM with Alembic-ready setup
- **Auto-generated docs** — Swagger UI (`/docs`) and ReDoc (`/redoc`) out of the box
- **Render-ready** — Includes `render.yaml` blueprint for one-click deployment

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Server | Uvicorn |
| ORM | SQLAlchemy |
| Database (prod) | PostgreSQL (`psycopg2-binary`) |
| Authentication | JWT (`python-jose`), OAuth2 |
| Password hashing | `passlib[bcrypt]`, `bcrypt==4.0.1` |
| Form parsing | `python-multipart` |
| Deployment | Render |

---

## API Endpoints

### Blogs

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/blog` | List blogs (supports `?limit=` and `?published=` query params) | No |
| `GET` | `/blog/unpublished` | List all unpublished blogs | No |
| `GET` | `/blog/{id}` | Get a single blog by ID | No |
| `GET` | `/blog/{id}/comments` | Get comments for a blog post | No |
| `POST` | `/blog` | Create a new blog post | Yes |

### Authentication & Users

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/login` | Login with username & password → returns bearer token |
| `POST` | `/user` | Register a new user |

### Request / Response Example

**Create a blog post** (`POST /blog`):

```json
// Request body
{
  "title": "My First Post",
  "body": "Hello, FastAPI world!",
  "published": true
}

// Response
{
  "data": "blog is created with title: My First Post"
}
```

**Login** (`POST /login`):

```
Content-Type: application/x-www-form-urlencoded

username=you@example.com&password=yourpassword
```

Returns a bearer token. Use it as `Authorization: Bearer <token>` on protected routes.

---

## Getting Started Locally

### Prerequisites

- Python 3.10+
- pip

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/Suhas7842/Fast-API.git
cd Fast-API

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env
# Edit .env with your values (see Environment Variables below)

# 4. Start the development server
uvicorn blog.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Open `http://127.0.0.1:8000/docs` to explore the interactive docs.

> **Note:** The root-level `main.py` is a scratch file used during development and contains a `breakpoint()`. Do not use it as the application entrypoint — always use `blog.main:app`.

---

## Environment Variables

Copy `.env.example` to `.env` and fill in the values:

```env
SECRET_KEY=replace-with-a-long-random-secret
DATABASE_URL=sqlite:///./blog.db          # Use PostgreSQL URL in production
JWT_ALGORITHM=HS256                        # Optional, defaults to HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30             # Optional, defaults to 30
```

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | Yes | Long random string for JWT signing |
| `DATABASE_URL` | Yes | Database connection string |
| `JWT_ALGORITHM` | No | JWT algorithm (default: `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | Token lifetime in minutes (default: `30`) |

---

## Deploying to Render

This repo includes a `render.yaml` blueprint for automated deployment.

### Steps

1. Push this repository to GitHub.
2. In [Render](https://render.com), create a new **PostgreSQL** database.
3. Create a new **Web Service** from the GitHub repo with these settings:

```
Runtime:       Python
Build Command: pip install -r requirements.txt
Start Command: uvicorn blog.main:app --host 0.0.0.0 --port $PORT
```

4. Add the following environment variables in Render:

```
SECRET_KEY=<use Render's "Generate Value">
DATABASE_URL=<Render PostgreSQL internal connection string>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Deploy, then verify at `https://your-service.onrender.com/docs`.

### Post-deployment checklist

- [ ] `/docs` loads successfully
- [ ] Register a user via the user endpoint
- [ ] Login at `/login` with OAuth2 form data
- [ ] Use the returned bearer token to call protected `/blog` routes

For the full deployment guide, see [DEPLOYMENT.md](./DEPLOYMENT.md).

---

## Project Structure

```
Fast-API/
├── blog/               # Main application package
│   └── main.py         # App entry point (use this for deployment)
├── main.py             # Dev scratch file (DO NOT deploy)
├── requirements.txt    # Python dependencies
├── render.yaml         # Render deployment blueprint
├── .env.example        # Environment variable template
└── DEPLOYMENT.md       # Detailed deployment guide
```

---

## Security Notes

- Passwords are hashed with bcrypt before storage — never stored in plain text.
- JWTs are signed with your `SECRET_KEY`; keep it secret and rotate it if compromised.
- Never commit your `.env` file, local database files, or `__pycache__` to version control.
- For production, always use PostgreSQL — SQLite is not suitable for Render deployments.
- Add CORS middleware if a frontend from another domain calls this API.
- For schema migrations in production, use [Alembic](https://alembic.sqlalchemy.org/) instead of `Base.metadata.create_all()`.
