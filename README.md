# Sweet Shop Management System

A full-stack application for managing a sweet shop, built with FastAPI (backend) and React (frontend).

## Project Overview

This system allows users to:
- Register and login
- View and search sweets
- Purchase sweets (if stock available)

Admins can:
- Add, update, and delete sweets
- Restock sweets

## Tech Stack

### Backend
- Python 3.10+
- FastAPI
- SQLAlchemy (ORM)
- SQLite (database)
- Pytest (testing)
- JWT Authentication

### Frontend
- React 18
- Vite
- Axios
- React Router DOM
- Simple CSS

## Project Structure

```
sweet-shop/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── auth/
│   │   ├── sweets/
│   │   ├── inventory/
│   │   └── core/
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── README.md
└── README.md
```

## Getting Started

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
uvicorn app.main:app --reload
```

Backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

Frontend will run on `http://localhost:5173`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user

### Sweets
- `POST /api/sweets` - Add sweet (Admin)
- `GET /api/sweets` - View all sweets (User/Admin)
- `GET /api/sweets/search?query=...` - Search sweets (User/Admin)
- `PUT /api/sweets/{id}` - Update sweet (Admin)
- `DELETE /api/sweets/{id}` - Delete sweet (Admin)

### Inventory
- `POST /api/sweets/{id}/purchase` - Purchase sweet (User/Admin)
- `POST /api/sweets/{id}/restock` - Restock sweet (Admin)

## Testing

### Backend Tests
```bash
cd backend
pytest
```

Tests follow TDD (Test-Driven Development) approach:
1. Write test (FAIL)
2. Write code (PASS)
3. Refactor

## Database

The application uses SQLite. The database file (`sweet_shop.db`) will be created automatically in the backend directory when you first run the application.

## Authentication

The system uses JWT (JSON Web Tokens) for authentication. Tokens are sent in the `Authorization` header:
```
Authorization: Bearer <token>
```

## Roles

- **USER**: Can view sweets, search, and purchase
- **ADMIN**: Can manage sweets (add, update, delete, restock) and perform all user actions

## Development Approach

This project follows **Test-Driven Development (TDD)**:
- Tests are written before implementation
- Each feature has corresponding tests
- Code is refactored after tests pass

## My AI Usage

- Used ChatGPT for project structure guidance
- Used AI for basic boilerplate suggestions
- All business logic and validation written and reviewed manually
- AI helped speed up development but did not replace understanding

## Notes

- This project focuses on correctness and clarity, not fancy UI
- Beginner-level code is acceptable and expected
- The system uses real SQLite database (not in-memory)
- All endpoints are protected with JWT authentication
- Role-based access control is implemented for admin-only endpoints

<!-- AI usage verified -->
