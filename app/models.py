from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class Employee(UserMixin, db.Model):
    """Employee/User model"""
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    is_manager = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    red_flags = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tasks = db.relationship('Task', backref='assigned_to_user', lazy=True, foreign_keys='Task.assigned_to')
    created_tasks = db.relationship('Task', backref='created_by_user', lazy=True, foreign_keys='Task.created_by')
    updates = db.relationship('TaskUpdate', backref='author', lazy=True)
    ratings_given = db.relationship('Rating', backref='rater', lazy=True, foreign_keys='Rating.rater_id')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password is correct"""
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """Get employee's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f'<Employee {self.username}>'

class Task(db.Model):
    """Task model"""
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    progress = db.Column(db.Integer, default=0)  # 0-100
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    updates = db.relationship('TaskUpdate', backref='task', lazy=True, cascade='all, delete-orphan')
    ratings = db.relationship('Rating', backref='task', lazy=True, cascade='all, delete-orphan')
    
    def get_average_rating(self):
        """Get average rating for the task/employee"""
        if not self.ratings:
            return 0
        total = sum(r.stars for r in self.ratings)
        return round(total / len(self.ratings), 2)
    
    def get_status_color(self):
        """Get color code for status"""
        colors = {
            'pending': '#FFC107',
            'in_progress': '#2196F3',
            'completed': '#4CAF50'
        }
        return colors.get(self.status, '#999')
    
    def __repr__(self):
        return f'<Task {self.title}>'

class TaskUpdate(db.Model):
    """Task update/progress model"""
    __tablename__ = 'task_updates'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    update_text = db.Column(db.Text, nullable=True)
    progress_percentage = db.Column(db.Integer, default=0)  # 0-100
    status = db.Column(db.String(20), default='in_progress')  # pending, in_progress, completed
    attachment_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<TaskUpdate {self.id} for Task {self.task_id}>'

class Rating(db.Model):
    """Star rating model for employee/task performance"""
    __tablename__ = 'ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    rater_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    stars = db.Column(db.Integer, default=5)  # 1-5 stars
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('task_id', 'rater_id', name='unique_rating_per_user'),
    )
    
    def __repr__(self):
        return f'<Rating {self.stars} stars for Task {self.task_id}>'

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return Employee.query.get(int(user_id))
