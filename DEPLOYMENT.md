# FastAPI Blog API Deployment Guide

This project should deploy the package app, not the old course scratch file.

Use this production start command:

```bash
uvicorn blog.main:app --host 0.0.0.0 --port $PORT
```

Do not deploy with Deta Micros. Deta Micros is retired.

## Deployment checklist

- Use `blog.main:app` as the app entrypoint.
- Keep `main.py` at the repository root out of deployment; it is an old scratch file and contains a `breakpoint()`.
- Use PostgreSQL in production. Do not use `blog.db` on Render.
- Set `SECRET_KEY` as an environment variable.
- Set `DATABASE_URL` from Render PostgreSQL.
- Install dependencies from `requirements.txt`.
- Confirm `/docs` loads after deployment.
- Create a user through the user endpoint.
- Login through `/login` using OAuth2 form data.
- Use the returned bearer token to call protected `/blog` routes.

## Required environment variables

| Variable | Required | Example / Notes |
|---|---:|---|
| `SECRET_KEY` | Yes | Generate a long random value. In Render, use Generate Value. |
| `DATABASE_URL` | Yes | Render PostgreSQL connection string. The app also accepts `postgres://` and converts it. |
| `JWT_ALGORITHM` | No | Defaults to `HS256`. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | Defaults to `30`. |

## Render deployment steps

1. Push this project to GitHub.
2. In Render, create a new PostgreSQL database, or use the included `render.yaml` blueprint.
3. Create a new Web Service from the GitHub repository.
4. Use these settings:

```text
Runtime: Python
Build Command: pip install -r requirements.txt
Start Command: uvicorn blog.main:app --host 0.0.0.0 --port $PORT
```

5. Add environment variables:

```text
SECRET_KEY=<Render generated secret>
DATABASE_URL=<Render PostgreSQL internal connection string>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

6. Deploy.
7. Open:

```text
https://your-render-service.onrender.com/docs
```

## Common FastAPI production fixes

- Do not hardcode secrets in source code.
- Do not use SQLite for Render production deployments.
- Render provides the port in `$PORT`; bind uvicorn to `0.0.0.0`.
- Add `python-multipart` when using `OAuth2PasswordRequestForm`.
- Add `psycopg2-binary` for PostgreSQL with SQLAlchemy.
- Avoid root-level scratch files as deployment entrypoints.
- Do not commit `.env`, local database files, or `__pycache__`.
- Add CORS middleware later if a frontend calls this API from another domain.
- For a real production app, use Alembic migrations instead of `Base.metadata.create_all(engine)`.
