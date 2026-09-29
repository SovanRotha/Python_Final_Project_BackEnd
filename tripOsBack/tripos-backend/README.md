# TripOS Backend

TripOS Backend is a FastAPI service for travel planning. It uses SQLAlchemy for persistence, PostgreSQL for normal development/deployment, JWT bearer tokens for authentication, and Alembic for database schema migrations.

## Requirements

- Python 3.10 or newer
- PostgreSQL 14 or newer
- PowerShell on Windows, or a shell with the equivalent Python commands

## Project layout

```text
app/
	main.py                 FastAPI application and router registration
	core/
		config.py             Environment-backed application settings
		database.py           SQLAlchemy engine, base class, and DB session dependency
		security.py           Password hashing and JWT creation/validation
	models/                 SQLAlchemy database tables
	schemas/                Pydantic request and response validation
	controllers/            Auth, user, admin, and domain CRUD logic
	routes/                 HTTP endpoints; delegates work to controllers
	services/               Reusable service helpers for trips, budgets, uploads, AI, etc.
	utils/                  Small shared utility functions
tests/                    Pytest API tests; use an isolated in-memory SQLite database
migrations/
	env.py                  Alembic metadata and database configuration
	versions/               Generated, reviewed migration revisions
uploads/
	documents/              Document upload storage location
	screenshots/            Screenshot upload storage location
	memories/               Memory upload storage location
.env                      Local environment configuration
alembic.ini               Alembic migration configuration
requirements.txt          Python dependencies
```

### Request flow

An HTTP request enters through a module in `app/routes/`. Protected endpoints use `app/api/deps.py` to resolve the current user from a bearer token. The route calls a controller in `app/controllers/`; controllers own the database operations and authorization scope. SQLAlchemy models define persisted fields, while Pydantic schemas validate incoming and outgoing API data. `app/services/` contains helpers that can be shared across controllers.

The resource controllers share `ResourceController` for list, create, get, and delete behavior. These endpoints are user-scoped. Most resource types currently accept `name`, `description`, and a JSON `data` object, plus selected common fields such as dates, amount, currency, and category. Add fields to the relevant SQLAlchemy model and Pydantic schema when a domain requires stricter structure.

## Install and configure

From the project directory, create and activate a virtual environment:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Create a PostgreSQL role and database. For example, from `psql` as a database administrator:

```sql
CREATE USER tripos_user WITH PASSWORD 'choose-a-local-password';
CREATE DATABASE tripos_db OWNER tripos_user;
```

Copy `.env.example` to `.env` if `.env` is missing, then set values appropriate for your machine:

```dotenv
APP_NAME=TripOS API
API_V1_PREFIX=/api/v1
DATABASE_URL=postgresql+psycopg://tripos_user:choose-a-local-password@localhost:5432/tripos_db
JWT_SECRET_KEY=replace-with-a-long-random-secret
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

The repository ignores `.env` so local credentials are not committed. If you want to create the database user with the sample credentials, run the SQL below in `psql`; otherwise use the username and password already configured in PostgreSQL:

```sql
CREATE USER tripos_user WITH PASSWORD 'change-me';
CREATE DATABASE tripos_db OWNER tripos_user;
```

If a password contains reserved URL characters, percent-encode them in `DATABASE_URL`. Replace the example JWT secret before deployment. Do not commit real credentials or production secrets.

## Database migrations

The application does not create or alter tables when it starts. Use Alembic to apply versioned schema changes. Make sure PostgreSQL is running and `DATABASE_URL` points to an existing database before running these commands from the project root.

The initial schema migration is checked in under `migrations/versions/`. For a new, empty database, apply it with:

```powershell
python -m alembic upgrade head
```

If you already have a database created by an earlier version of this app, do not run the initial migration against its existing tables. Back up the database first. If its schema exactly matches the checked-in baseline, mark that revision as applied without changing tables:

```powershell
python -m alembic stamp head
```

`stamp` only updates Alembic's version tracking; it does not create, alter, or verify tables. If the existing schema differs, compare it with the baseline and write an appropriate migration, or use a fresh development database and apply `upgrade head`.

For future model changes:

1. Update the SQLAlchemy model and its Pydantic schema.
2. Generate a revision: `python -m alembic revision --autogenerate -m "describe the change"`.
3. Review and, if necessary, edit the generated upgrade and downgrade operations.
4. Apply it locally with `python -m alembic upgrade head`.
5. Commit the migration file with the model and schema changes.

Useful commands:

```powershell
python -m alembic current
python -m alembic history
python -m alembic upgrade head
python -m alembic downgrade -1
```

Autogeneration is a starting point, not a substitute for reviewing the migration. Back up important databases before upgrades or downgrades. Test migrations against a disposable database before production.

## Run the API

After dependencies are installed and migrations are applied:

```powershell
python -m uvicorn app.main:app --reload
```

By default, the service listens on `http://127.0.0.1:8000`.

- Interactive API docs: `http://127.0.0.1:8000/docs`
- Alternative docs: `http://127.0.0.1:8000/redoc`
- Health check: `http://127.0.0.1:8000/health`

To use another port: `python -m uvicorn app.main:app --reload --port 8001`.

## Run with Docker

Docker Compose runs the API and PostgreSQL with pinned image versions. The API installs the exact package versions in `requirements.lock`, waits for PostgreSQL, and applies Alembic migrations before starting. PostgreSQL data persists in the `postgres_data` volume.

Start the stack from the project directory:

```powershell
docker compose up --build
```

Open `http://localhost:8000/docs` for the API. To stop the containers while keeping the database, press `Ctrl+C` and run `docker compose down`. To also delete the stored database, run `docker compose down --volumes`.

Both developers should use the same committed `Dockerfile`, `compose.yaml`, and `requirements.lock`. To change the dependency set, update the lock file and commit it along with the code changes. The Compose defaults are for local development only; set `POSTGRES_PASSWORD` and `JWT_SECRET_KEY` through a local `.env` file or environment variables before exposing the service beyond your machine.

## Authentication and API use

Register an account using `POST /api/v1/auth/register` with `email`, `password` (at least 8 characters), and optional `full_name`. Then log in using `POST /api/v1/auth/login` with the email and password. The response contains an `access_token`.

Send the token on protected requests using this header:

```text
Authorization: Bearer <access_token>
```

For example, after starting the server, use the Swagger UI at `/docs` to register, authorize, then try the protected endpoints. `GET /api/v1/users/me` returns the current account. Resource endpoints generally provide `GET` (list), `POST` (create), `GET /{id}` (fetch one), and `DELETE /{id}` operations. Users can only read or delete their own resources.

### Route groups

- Authentication and account: `/api/v1/auth`, `/api/v1/users`
- Destinations and places: `/api/v1/destinations`, `/api/v1/places`, `/api/v1/saved-places`
- Trip planning: `/api/v1/trips`, `/api/v1/itineraries`
- Money: `/api/v1/budgets`, `/api/v1/wallets`, `/api/v1/expenses`
- Preparation and bookings: `/api/v1/packing`, `/api/v1/checklists`, `/api/v1/accommodations`, `/api/v1/transports`
- Travel records: `/api/v1/documents`, `/api/v1/screenshots`, `/api/v1/reminders`, `/api/v1/notifications`, `/api/v1/memories`
- AI request records: `/api/v1/ai/requests`
- Admin utility: `/api/v1/admin/users/count`

The admin utility currently requires authentication but does not implement role-based admin authorization. Do not expose it as an admin-only feature until roles and permission checks are added. The AI endpoint stores request records; it is not yet connected to an AI provider. Document and screenshot resource endpoints currently store metadata; production file upload/download endpoints and storage policies still need to be implemented.

## Tests

Run the suite from the project root:

```powershell
python -m pytest
```

Tests override the configured database with in-memory SQLite and reset the tables per test. They do not require a running PostgreSQL server and do not test PostgreSQL-specific behavior or migrations.

## Before deployment

- Set a unique, strong `JWT_SECRET_KEY` and keep it secret.
- Configure PostgreSQL credentials through deployment environment variables or a secrets manager.
- Apply and verify Alembic migrations before starting application workers.
- Use private, durable file storage instead of relying on the local `uploads/` directories.
- Add role checks before treating admin routes as privileged.
- Configure HTTPS, CORS policy, logging, backups, and database connection/pool limits for the hosting environment.