# ThreadOS

A clean, stable Threads automation dashboard for a single user.

## Features

- **Connect**: Authentic with Threads API (Meta Graph).
- **Compose**: Create and publish text posts.
- **Inbox**: View and reply to comments.
- **Analytics**: View post insights snapshots.
- **Data Ownership**: Local SQLite database and backup system.

## Project Structure

- `/backend`: Python FastAPI application.
- `/frontend`: React + Tailwind CSS application (Vite).
- `/storage`: SQLite database and backups (persisted outside code folders).

## Local Run Instructions

### Prerequisites

- Python 3.9+
- Node.js 16+
- Meta Developer App (for Threads API credentials)

### Backend Setup

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configure environment variables:
    - Copy `.env.example` to `.env`.
    - Update `THREADS_CLIENT_ID` and `THREADS_CLIENT_SECRET`.
5.  Run database migrations:
    ```bash
    alembic upgrade head
    ```
6.  Start the backend server:
    ```bash
    uvicorn app.main:app --reload --port 8000
    ```
    Documentation available at http://localhost:8000/docs.

### Frontend Setup

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```
    Access the app at http://localhost:5173.

## Backup

To backup the database:
```bash
python backend/scripts/backup_db.py
```
Backups are stored in `storage/backups`.
