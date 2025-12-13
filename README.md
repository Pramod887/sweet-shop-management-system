Sweet Shop Management System

A full-stack web application for managing a sweet shop, built using FastAPI for the backend and React with Vite for the frontend. The system supports secure authentication, inventory management, purchasing workflows, and admin-level controls using role-based access.

Project Overview

The Sweet Shop Management System is designed to manage the daily operations of a sweet shop in a simple and efficient way. Users can register, log in, browse available sweets, search based on different criteria, and purchase sweets depending on stock availability.

Admin users have additional privileges such as adding new sweets, updating existing ones, deleting sweets, and restocking inventory. The application follows RESTful API design principles and ensures secure access using JWT-based authentication.

Tech Stack
Backend

Python 3.10+

FastAPI

SQLAlchemy (ORM)

SQLite (persistent database)

JWT Authentication

Pytest for testing

Frontend

React 18

Vite

Axios

React Router DOM

CSS

Project Structure

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
│   └── create_admin.py
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
Prerequisites

Python 3.10 or higher
Node.js 18 or higher
npm

Backend Setup and Run (FastAPI)
Open a terminal and run the following commands:
# Navigate to backend directory
cd backend
# Create virtual environment (skip if already exists)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Linux or Mac:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
# Run the FastAPI server
uvicorn app.main:app --reload
Backend will run on:

Frontend Setup and Run (React + Vite)
Open a new terminal and run:
# Navigate to frontend directory
cd frontend
# Install dependencies
npm install
# Run development server
npm run dev
Frontend will run on:

# Default Admin Credentials (For Testing)

Use the following credentials to access admin features such as adding, updating, deleting, and restocking sweets:

Email: admin@admin.com

Password: 123456

These credentials are provided for demo and testing purposes only. In a real production environment, credentials should be managed securely and never hard-coded.

Optional: Create Admin User Manually

If the admin user does not exist, you can create one manually after starting the backend.

Make sure the virtual environment is activated and run:

# Application Flow Summary

Start the backend server first.

Start the frontend development server in a separate terminal.

Open http://localhost:5173
 in your browser.

The frontend automatically communicates with the backend API running on port 8000

# Roles and Permissions
USER

View all sweets

Search sweets

Purchase sweets

ADMIN

Add sweets

Update sweet details

Delete sweets

Restock sweets

Perform all user-level actions

# API Endpoints
Authentication

POST /api/auth/register – Register a new user
POST /api/auth/login – Login user

# Sweets

POST /api/sweets – Add a sweet (Admin only)
GET /api/sweets – View all sweets
GET /api/sweets/search – Search sweets
PUT /api/sweets/{id} – Update sweet details (Admin only)
DELETE /api/sweets/{id} – Delete a sweet (Admin only)

# Inventory

POST /api/sweets/{id}/purchase – Purchase a sweet
POST /api/sweets/{id}/restock – Restock a sweet (Admin only)

# Testing
Backend tests are written using Pytest.
cd backend
pytest

# Test-Driven Development Approach

Write a failing test

Implement the required functionality

Refactor the code while keeping tests passing

# Database

The application uses SQLite for data persistence. The database file is created automatically when the backend is run for the first time. The system does not rely on in-memory storage.

# My AI Usage

AI tools such as ChatGPT were used during development for:

Understanding project requirements

Generating initial boilerplate suggestions

# Improving documentation and test cases

All business logic, validations, and architectural decisions were implemented and reviewed manually. AI tools assisted productivity but did not replace understanding.

# Notes

The user interface is intentionally kept simple to focus on functionality.

The project emphasizes clean architecture and readable code.

Suitable for interviews, assignments, and learning purposes.