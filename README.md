# Sweet Shop Management System

A full-stack web application built using **FastAPI** for the backend and **React + Vite** for the frontend. The project manages sweet shop operations with secure authentication, inventory handling, and role-based access control.

## Overview

Users can register, log in, view and search sweets, and purchase items based on stock availability. Admin users can add, update, delete, and restock sweets. The application follows RESTful API standards and uses JWT for secure authentication.

## Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication
- Pytest

### Frontend
- React
- Vite
- Axios
- React Router
- CSS

## How to Run the Project

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows (use source venv/bin/activate for Mac/Linux)
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs on `http://127.0.0.1:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

## Admin Credentials (For Testing)

- **Email:** `admin@admin.com`
- **Password:** `123456`

## User Roles

- **User:** View, search, and purchase sweets
- **Admin:** Add, update, delete, and restock sweets

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - User login

### Sweets Management
- `GET /api/sweets` - Get all sweets
- `GET /api/sweets/search` - Search sweets
- `POST /api/sweets` - Add new sweet (Admin only)
- `PUT /api/sweets/{id}` - Update sweet (Admin only)
- `DELETE /api/sweets/{id}` - Delete sweet (Admin only)

### Inventory Management
- `POST /api/sweets/{id}/purchase` - Purchase sweet
- `POST /api/sweets/{id}/restock` - Restock sweet (Admin only)

## Testing

The backend follows a **Test-Driven Development (TDD)** approach.

```bash
cd backend
pytest
```

## Database

The application uses **SQLite** for persistent storage. The database is created automatically when the backend starts.

## AI Usage

ChatGPT was used for requirement understanding, boilerplate guidance, and documentation improvements. All business logic and validations were implemented and reviewed manually.

## Notes

The UI is intentionally simple with a focus on functionality and clean architecture. This project is suitable for interviews, assignments, and learning full-stack development.

## License

This project is open source and available for educational purposes.