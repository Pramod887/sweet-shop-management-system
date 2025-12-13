# Sweet Shop Management System - Backend

## Overview

This is the backend API for the Sweet Shop Management System, built with FastAPI, SQLAlchemy, and SQLite.

## Features

- JWT-based authentication
- Role-based access control (Admin & User)
- RESTful API for managing sweets
- Inventory management (purchase & restock)
- Test-driven development (TDD) approach

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Running Tests

```bash
pytest
```

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth/                # Authentication module
│   │   ├── router.py
│   │   ├── service.py
│   │   └── test_auth.py
│   ├── sweets/              # Sweets management module
│   │   ├── router.py
│   │   ├── service.py
│   │   └── test_sweets.py
│   ├── inventory/           # Inventory management module
│   │   ├── router.py
│   │   ├── service.py
│   │   └── test_inventory.py
│   └── core/                # Core utilities
│       ├── security.py      # JWT & password hashing
│       └── dependencies.py  # FastAPI dependencies
└── requirements.txt
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token

### Sweets (Protected)
- `POST /api/sweets` - Add sweet (Admin only)
- `GET /api/sweets` - View all sweets (User/Admin)
- `GET /api/sweets/search?query=...` - Search sweets (User/Admin)
- `PUT /api/sweets/{id}` - Update sweet (Admin only)
- `DELETE /api/sweets/{id}` - Delete sweet (Admin only)

### Inventory
- `POST /api/sweets/{id}/purchase` - Purchase sweet (User/Admin)
- `POST /api/sweets/{id}/restock` - Restock sweet (Admin only)

## My AI Usage

- Used ChatGPT for project structure guidance
- Used AI for basic boilerplate suggestions
- All business logic and validation written and reviewed manually
- AI helped speed up development but did not replace understanding

