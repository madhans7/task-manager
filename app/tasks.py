from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models import Task, TaskUpdate, Rating, Employee
from app.forms import CreateTaskForm, TaskUpdateForm, RatingForm
from app.email_utils import send_task_assigned_email, send_update_notification_email, send_rating_notification_email

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_task():
    """Create a new task (manager only)"""
    if not current_user.is_manager:
        flash('Only managers can create tasks', 'danger')
        return redirect(url_for('main.dashboard'))
    
    form = CreateTaskForm()
    form.assigned_to.choices = [(emp.id, emp.get_full_name()) 
                                for emp in Employee.query.filter_by(is_manager=False).all()]
    
    if form.validate_on_submit():
        try:
            due_date = None
            if form.due_date.data:
                due_date = datetime.strptime(form.due_date.data, '%Y-%m-%d')
            
            task = Task(
                title=form.title.data,
                description=form.description.data,
                created_by=current_user.id,
                assigned_to=form.assigned_to.data,
                priority=form.priority.data,
                due_date=due_date
            )
            
            db.session.add(task)
            db.session.commit()
            
            # Send email notification
            assigned_employee = Employee.query.get(form.assigned_to.data)
            send_task_assigned_email(assigned_employee, task)
            
            flash(f'Task "{task.title}" created and assigned successfully!', 'success')
            return redirect(url_for('main.task_detail', task_id=task.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating task: {str(e)}', 'danger')
    
    return render_template('task_create.html', form=form)

@tasks_bp.route('/<int:task_id>/update', methods=['GET', 'POST'])
@login_required
def submit_update(task_id):
    """Submit task update"""
    task = Task.query.get_or_404(task_id)
    
    # Only assigned employee can submit updates
    if task.assigned_to != current_user.id:
        flash('You cannot update this task', 'danger')
        return redirect(url_for('main.dashboard'))
    
    form = TaskUpdateForm()
    if form.validate_on_submit():
        try:
            update = TaskUpdate(
                task_id=task_id,
                employee_id=current_user.id,
                update_text=None, # Message removed
                progress_percentage=form.progress_percentage.data,
                status=form.status.data
            )
            
            # Update task progress and status
            task.progress = form.progress_percentage.data
            task.status = form.status.data
            
            db.session.add(update)
            db.session.commit()
            
            # Send email to manager (optional, but keeping it for now)
            manager = Employee.query.get(task.created_by)
            send_update_notification_email(manager, task, current_user, update)
            
            flash('Update submitted successfully!', 'success')
            return redirect(url_for('main.task_detail', task_id=task_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error submitting update: {str(e)}', 'danger')
    
    return render_template('task_update.html', task=task, form=form)

@tasks_bp.route('/<int:task_id>/rate', methods=['POST'])
@login_required
def rate_task(task_id):
    """Rate a task/employee"""
    task = Task.query.get_or_404(task_id)
    
    # Cannot rate own task
    if task.assigned_to == current_user.id:
        return {'error': 'Cannot rate your own task'}, 403
    
    # Check if already rated
    existing_rating = Rating.query.filter_by(task_id=task_id, rater_id=current_user.id).first()
    if existing_rating:
        return {'error': 'You have already rated this task'}, 400
    
    try:
        stars = request.form.get('stars', type=int)
        
        if stars < 1 or stars > 5:
            return {'error': 'Rating must be between 1 and 5'}, 400
        
        rating = Rating(
            task_id=task_id,
            rater_id=current_user.id,
            stars=stars,
            comment=None # Comment removed
        )
        
        db.session.add(rating)
        db.session.commit()
        
        # Send email to employee
        employee = Employee.query.get(task.assigned_to)
        send_rating_notification_email(employee, current_user, task, rating)
        
        return {'message': 'Rating submitted successfully!'}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@tasks_bp.route('/employee/<int:employee_id>/flag', methods=['POST'])
@login_required
def add_red_flag(employee_id):
    """Add a red flag to an employee (manager only)"""
    if not current_user.is_manager:
        return {'error': 'Unauthorized'}, 403
    
    employee = Employee.query.get_or_404(employee_id)
    if employee.red_flags < 7:
        employee.red_flags += 1
        db.session.commit()
        return {'message': f'Red flag added to {employee.get_full_name()}. Total: {employee.red_flags}', 'count': employee.red_flags}, 200
    else:
        return {'error': 'Maximum red flags (7) reached'}, 400

@tasks_bp.route('/stats/contribution')
@login_required
def get_contribution_stats():
    """Get weekly contribution stats for interns"""
    from datetime import timedelta
    last_week = datetime.utcnow() - timedelta(days=7)
    
    interns = Employee.query.filter_by(is_manager=False).all()
    stats = []
    for intern in interns:
        updates_count = TaskUpdate.query.filter(
            TaskUpdate.employee_id == intern.id,
            TaskUpdate.created_at >= last_week
        ).count()
        stats.append({
            'name': intern.get_full_name(),
            'count': updates_count
        })
    return {'stats': stats}

@tasks_bp.route('/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    """Edit task (manager only)"""
    task = Task.query.get_or_404(task_id)
    
    if task.created_by != current_user.id and not current_user.is_manager:
        flash('You do not have permission to edit this task', 'danger')
        return redirect(url_for('main.dashboard'))
    
    form = CreateTaskForm()
    form.assigned_to.choices = [(emp.id, emp.get_full_name()) 
                                for emp in Employee.query.filter_by(is_manager=False).all()]
    
    if form.validate_on_submit():
        try:
            due_date = None
            if form.due_date.data:
                due_date = datetime.strptime(form.due_date.data, '%Y-%m-%d')
            
            task.title = form.title.data
            task.description = form.description.data
            task.assigned_to = form.assigned_to.data
            task.priority = form.priority.data
            task.due_date = due_date
            
            db.session.commit()
            flash('Task updated successfully!', 'success')
            return redirect(url_for('main.task_detail', task_id=task.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating task: {str(e)}', 'danger')
    elif request.method == 'GET':
        form.title.data = task.title
        form.description.data = task.description
        form.assigned_to.data = task.assigned_to
        form.priority.data = task.priority
        if task.due_date:
            form.due_date.data = task.due_date.strftime('%Y-%m-%d')
    
    return render_template('task_edit.html', task=task, form=form)

@tasks_bp.route('/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    """Delete task (manager only)"""
    task = Task.query.get_or_404(task_id)
    
    if task.created_by != current_user.id and not current_user.is_manager:
        flash('You do not have permission to delete this task', 'danger')
        return redirect(url_for('main.dashboard'))
    
    try:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting task: {str(e)}', 'danger')
    
    return redirect(url_for('main.dashboard'))

@tasks_bp.route('/search')
@login_required
def search_tasks():
    """Search tasks"""
    query = request.args.get('q', '', type=str)
    page = request.args.get('page', 1, type=int)
    
    if current_user.is_manager:
        tasks = Task.query.filter(
            (Task.title.ilike(f'%{query}%')) | 
            (Task.description.ilike(f'%{query}%'))
        ).paginate(page=page, per_page=10)
    else:
        tasks = Task.query.filter(
            (Task.assigned_to == current_user.id) &
            ((Task.title.ilike(f'%{query}%')) | 
             (Task.description.ilike(f'%{query}%')))
        ).paginate(page=page, per_page=10)
    
    return render_template('search_results.html', tasks=tasks, query=query)
