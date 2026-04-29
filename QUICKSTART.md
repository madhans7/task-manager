"""
Quick Start Guide - Task Manager Application
Execute this interactively in Python shell
"""

# Setup steps:

# 1. Create virtual environment and activate it
# python -m venv venv
# venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 2. Install dependencies
# pip install -r requirements.txt

# 3. Initialize database with sample data
# python init_db.py

# 4. Update email configuration in config.py
# Set MAIL_USERNAME and MAIL_PASSWORD with your Gmail credentials

# 5. Run the application
# python run.py

# Manual database initialization (if needed):
"""
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print("Database created!")
"""

# Create a new user manually:
"""
from app import create_app, db
from app.models import Employee

app = create_app()
with app.app_context():
    user = Employee(
        username='testuser',
        email='test@example.com',
        first_name='Test',
        last_name='User',
        is_manager=False
    )
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    print(f"User {user.username} created!")
"""

# Query users:
"""
from app import create_app, db
from app.models import Employee

app = create_app()
with app.app_context():
    users = Employee.query.all()
    for user in users:
        print(f"{user.username} - {user.email}")
"""

# Clear database:
"""
from app import create_app, db

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database cleared and recreated!")
"""

print(__doc__)
