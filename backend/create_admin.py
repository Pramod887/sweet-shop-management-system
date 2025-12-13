"""
Script to create an admin user for testing purposes.
Run this after setting up the database.

Usage:
    cd backend
    source venv/bin/activate  # On Windows: venv\\Scripts\\activate
    python create_admin.py
"""

import sys
import os

# Ensure we're in the right directory
if not os.path.exists('app'):
    print("Error: Please run this script from the backend directory")
    print("Example: cd backend && source venv/bin/activate && python create_admin.py")
    sys.exit(1)

try:
    from sqlalchemy.orm import Session
    from app.database import SessionLocal
    from app.models import User, UserRole
    from app.core.security import get_password_hash
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you have activated the virtual environment:")
    print("  source venv/bin/activate  # On Windows: venv\\\\Scripts\\\\activate")
    print("And installed dependencies:")
    print("  pip install -r requirements.txt")
    sys.exit(1)

def create_admin(email: str, password: str):
    db: Session = SessionLocal()
    try:
        # Check if admin already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"User with email {email} already exists!")
            if existing_user.role == UserRole.ADMIN:
                print("This user is already an admin.")
            else:
                # Update to admin
                existing_user.role = UserRole.ADMIN
                existing_user.password = get_password_hash(password)
                db.commit()
                print(f"User {email} has been updated to admin role.")
            return
        
        # Create new admin user
        hashed_password = get_password_hash(password)
        admin_user = User(
            email=email,
            password=hashed_password,
            role=UserRole.ADMIN
        )
        db.add(admin_user)
        db.commit()
        print(f"Admin user created successfully!")
        print(f"Email: {email}")
        print(f"Password: {password}")
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    email = input("Enter admin email (default: admin@example.com): ").strip() or "admin@example.com"
    password = input("Enter admin password (default: admin123): ").strip() or "admin123"
    
    create_admin(email, password)

