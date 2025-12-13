# Sweet Shop Management System - Frontend

## Overview

This is the frontend application for the Sweet Shop Management System, built with React and Vite.

## Features

- User registration and login
- JWT token-based authentication
- Dashboard for viewing and purchasing sweets
- Search functionality
- Admin panel for managing sweets
- Simple, beginner-friendly React code

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Build for Production

```bash
npm run build
```

## Project Structure

```
frontend/
├── src/
│   ├── api/
│   │   └── axios.js          # Axios configuration
│   ├── pages/
│   │   ├── Login.jsx         # Login page
│   │   ├── Register.jsx      # Registration page
│   │   ├── Dashboard.jsx     # User dashboard
│   │   └── Admin.jsx         # Admin panel
│   ├── components/
│   │   └── SweetCard.jsx     # Sweet card component
│   ├── App.jsx               # Main app component
│   ├── main.jsx              # Entry point
│   └── index.css             # Global styles
├── package.json
└── vite.config.js
```

## Features by Page

### Login Page
- Email and password authentication
- Redirects to dashboard/admin based on role

### Register Page
- User registration
- Automatic login after registration

### Dashboard (User)
- View all available sweets
- Search sweets by name or category
- Purchase sweets (if in stock)

### Admin Panel
- Add new sweets
- Update existing sweets
- Delete sweets
- Restock sweets

## My AI Usage

- Used ChatGPT for project structure guidance
- Used AI for basic boilerplate suggestions
- All business logic and validation written and reviewed manually
- AI helped speed up development but did not replace understanding

