# -*- coding: utf-8 -*-
"""
Task Manager - Database Initialization Script
This script helps initialize the database and create sample data
"""

from app import create_app, db
from app.models import Employee, Task, TaskUpdate, Rating
from datetime import datetime, timedelta

def init_database():
    """Initialize the database"""
    app = create_app()
    
    with app.app_context():
        # Drop all tables to apply schema changes
        print("Dropping existing tables...")
        db.drop_all()
        print("Creating database tables...")
        db.create_all()
        print("[DONE] Database tables created successfully!")

def create_sample_data():
    """Create sample data for testing"""
    app = create_app()
    
    with app.app_context():
        # Check if data already exists
        if Employee.query.first():
            print("[WARN] Sample data already exists in database. Skipping creation.")
            return
        
        print("\nCreating sample data...")
        
        # Create manager
        manager = Employee(
            username='manager',
            email='manager@taskmanager.com',
            first_name='John',
            last_name='Manager',
            is_manager=True,
            is_active=True
        )
        manager.set_password('manager123')
        db.session.add(manager)
        
        # Create employees
        employees = []
        emp_data = [
            ('john_emp', 'john@taskmanager.com', 'John', 'Doe'),
            ('jane_emp', 'jane@taskmanager.com', 'Jane', 'Smith'),
            ('bob_emp', 'bob@taskmanager.com', 'Bob', 'Wilson'),
        ]
        
        for username, email, first_name, last_name in emp_data:
            emp = Employee(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_manager=False,
                is_active=True
            )
            emp.set_password('employee123')
            db.session.add(emp)
            employees.append(emp)
        
        db.session.commit()
        print(f"[DONE] Created 1 manager and {len(employees)} employees")
        
        # Create sample tasks
        due_date = datetime.utcnow() + timedelta(days=7)
        
        task1 = Task(
            title='Design Homepage',
            description='Create mockups and design for the new homepage',
            created_by=manager.id,
            assigned_to=employees[0].id,
            priority='high',
            due_date=due_date,
            status='in_progress',
            progress=60
        )
        
        task2 = Task(
            title='Fix Login Bug',
            description='Resolve the login authentication issue',
            created_by=manager.id,
            assigned_to=employees[1].id,
            priority='high',
            due_date=due_date - timedelta(days=2),
            status='in_progress',
            progress=45
        )
        
        task3 = Task(
            title='Database Optimization',
            description='Optimize database queries for better performance',
            created_by=manager.id,
            assigned_to=employees[2].id,
            priority='medium',
            due_date=due_date + timedelta(days=3),
            status='pending',
            progress=0
        )
        
        db.session.add_all([task1, task2, task3])
        db.session.commit()
        print("[DONE] Created 3 sample tasks")
        
        # Create sample updates
        update1 = TaskUpdate(
            task_id=task1.id,
            employee_id=employees[0].id,
            update_text='Completed the initial design mockups. Working on the color scheme refinement.',
            progress_percentage=60,
            status='in_progress'
        )
        
        update2 = TaskUpdate(
            task_id=task2.id,
            employee_id=employees[1].id,
            update_text='Identified the issue in the authentication middleware. Currently implementing the fix.',
            progress_percentage=45,
            status='in_progress'
        )
        
        db.session.add_all([update1, update2])
        db.session.commit()
        print("[DONE] Created sample task updates")
        
        # Create sample ratings
        rating1 = Rating(
            task_id=task1.id,
            rater_id=manager.id,
            stars=5,
            comment='Excellent work on the homepage design!'
        )
        
        rating2 = Rating(
            task_id=task2.id,
            rater_id=employees[2].id,
            stars=4,
            comment='Good progress on the authentication fix.'
        )
        
        db.session.add_all([rating1, rating2])
        db.session.commit()
        print("[DONE] Created sample ratings")
        
        print("\n" + "="*50)
        print("Sample data created successfully!")
        print("="*50)
        print("\nTest Credentials:")
        print("-" * 50)
        print("Manager Account:")
        print("  Username: manager")
        print("  Password: manager123")
        print("\nEmployee Accounts:")
        for i, (username, email, first_name, last_name) in enumerate(emp_data):
            print(f"  Username: {username}")
            print(f"  Password: employee123")
            if i < len(emp_data) - 1:
                print()
        print("\n" + "="*50)

def main():
    """Main function"""
    print("+" + "-"*50 + "+")
    print("|     Task Manager - Database Initialization      |")
    print("+" + "-"*50 + "+\n")
    
    try:
        init_database()
        create_sample_data()
        print("\n* Initialization complete! You're ready to go.")
        print("  Start the app with: python run.py")
    except Exception as e:
        print(f"\n[ERROR] Error during initialization: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
