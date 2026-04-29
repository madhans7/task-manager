from app import create_app, db
from app.models import Employee

app = create_app()
with app.app_context():
    users = Employee.query.all()
    print(f"Total users: {len(users)}")
    for user in users:
        print(f"Username: {user.username}, Is Manager: {user.is_manager}, Is Active: {user.is_active}")
