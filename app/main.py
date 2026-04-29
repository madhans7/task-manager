from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models import Task, Employee, TaskUpdate, Rating
from app.forms import CreateTaskForm, TaskUpdateForm, RatingForm, UpdateProfileForm
from app.email_utils import send_task_assigned_email, send_update_notification_email, send_rating_notification_email

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    page = request.args.get('page', 1, type=int)
    
    # For managers, see all tasks and all interns
    if current_user.is_manager:
        tasks = Task.query.paginate(page=page, per_page=10)
        interns = Employee.query.filter_by(is_manager=False).all()
    else:
        # Interns see only their assigned tasks
        tasks = Task.query.filter_by(assigned_to=current_user.id).paginate(page=page, per_page=10)
        interns = []
    
    # Get task statistics
    if current_user.is_manager:
        total_tasks = Task.query.count()
        pending_tasks = Task.query.filter_by(status='pending').count()
        in_progress = Task.query.filter_by(status='in_progress').count()
        completed = Task.query.filter_by(status='completed').count()
    else:
        total_tasks = Task.query.filter_by(assigned_to=current_user.id).count()
        pending_tasks = Task.query.filter_by(assigned_to=current_user.id, status='pending').count()
        in_progress = Task.query.filter_by(assigned_to=current_user.id, status='in_progress').count()
        completed = Task.query.filter_by(assigned_to=current_user.id, status='completed').count()
    
    stats = {
        'total': total_tasks,
        'pending': pending_tasks,
        'in_progress': in_progress,
        'completed': completed
    }
    
    return render_template('dashboard.html', tasks=tasks, stats=stats, interns=interns)

@main_bp.route('/all-tasks')
@login_required
def all_tasks():
    """View all tasks (visible to everyone)"""
    page = request.args.get('page', 1, type=int)
    tasks = Task.query.paginate(page=page, per_page=10)
    return render_template('all_tasks.html', tasks=tasks)

@main_bp.route('/task/<int:task_id>')
@login_required
def task_detail(task_id):
    """View task details"""
    task = Task.query.get_or_404(task_id)
    
    # Everyone can view any task
    pass
    
    updates = TaskUpdate.query.filter_by(task_id=task_id).order_by(TaskUpdate.created_at.desc()).all()
    ratings = Rating.query.filter_by(task_id=task_id).all()
    average_rating = task.get_average_rating()
    
    # Check if current user can rate
    user_rating = Rating.query.filter_by(task_id=task_id, rater_id=current_user.id).first()
    can_rate = current_user.id != task.assigned_to and not user_rating
    
    form = RatingForm()
    return render_template('task_detail.html', task=task, updates=updates, ratings=ratings, 
                          average_rating=average_rating, form=form, can_rate=can_rate)

@main_bp.route('/my-updates')
@login_required
def my_updates():
    """View all updates submitted by current employee"""
    page = request.args.get('page', 1, type=int)
    updates = TaskUpdate.query.filter_by(employee_id=current_user.id).order_by(
        TaskUpdate.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('my_updates.html', updates=updates)

@main_bp.route('/all-updates')
@login_required
def all_updates():
    """View all updates from all employees (visible to everyone)"""
    page = request.args.get('page', 1, type=int)
    updates = TaskUpdate.query.order_by(TaskUpdate.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('all_updates.html', updates=updates)

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page"""
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    
    # Get user's task statistics
    if current_user.is_manager:
        created_tasks = Task.query.filter_by(created_by=current_user.id).count()
        avg_rating = db.session.query(db.func.avg(Rating.stars)).filter(
            Task.created_by == current_user.id,
            Rating.task_id == Task.id
        ).scalar() or 0
    else:
        created_tasks = Task.query.filter_by(assigned_to=current_user.id).count()
        avg_rating = db.session.query(db.func.avg(Rating.stars)).filter(
            Task.assigned_to == current_user.id,
            Rating.task_id == Task.id
        ).scalar() or 0
    
    stats = {
        'tasks': created_tasks,
        'average_rating': round(avg_rating, 2) if avg_rating else 0
    }
    
    return render_template('profile.html', form=form, stats=stats, user=current_user)

@main_bp.route('/employees')
@login_required
def employees():
    """View all employees (manager only)"""
    if not current_user.is_manager:
        flash('Only managers can view this page', 'danger')
        return redirect(url_for('main.dashboard'))
    
    employees = Employee.query.filter_by(is_manager=False).all()
    employee_stats = []
    
    for emp in employees:
        tasks = Task.query.filter_by(assigned_to=emp.id).count()
        avg_rating = db.session.query(db.func.avg(Rating.stars)).filter(
            Task.assigned_to == emp.id,
            Rating.task_id == Task.id
        ).scalar() or 0
        
        employee_stats.append({
            'employee': emp,
            'tasks': tasks,
            'average_rating': round(avg_rating, 2)
        })
    
    return render_template('employees.html', employee_stats=employee_stats)
