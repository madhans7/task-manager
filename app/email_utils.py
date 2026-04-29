from flask import render_template
from flask_mail import Message
from app import mail
import threading

def send_async_email(app, msg):
    """Send email asynchronously"""
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipient, text_body, html_body, app=None):
    """Send email notification"""
    if app is None:
        from flask import current_app
        app = current_app
    
    msg = Message(subject, recipients=[recipient])
    msg.body = text_body
    msg.html = html_body
    
    # Send email asynchronously
    thread = threading.Thread(send_async_email, args=(app, msg))
    thread.start()
    return thread

def send_task_assigned_email(employee, task):
    """Send email when task is assigned"""
    subject = f"New Task Assigned: {task.title}"
    text_body = f"""Hi {employee.get_full_name()},

A new task has been assigned to you:

Title: {task.title}
Description: {task.description}
Priority: {task.priority.upper()}
Due Date: {task.due_date.strftime('%Y-%m-%d') if task.due_date else 'Not set'}

Please log in to the Task Manager to view more details and submit your updates.

Best regards,
Task Manager System"""
    
    html_body = render_template('email/task_assigned.html', 
                               employee=employee, task=task)
    
    from flask import current_app
    send_email(subject, employee.email, text_body, html_body, current_app._get_current_object())

def send_update_notification_email(manager, task, employee, update):
    """Send email when employee submits an update"""
    subject = f"Task Update: {task.title} from {employee.get_full_name()}"
    text_body = f"""Hi {manager.get_full_name()},

{employee.get_full_name()} has submitted an update for the task "{task.title}":

Update: {update.update_text}
Progress: {update.progress_percentage}%
Status: {update.status.upper()}

Please log in to the Task Manager to view more details and provide feedback.

Best regards,
Task Manager System"""
    
    html_body = render_template('email/update_notification.html',
                               manager=manager, task=task, employee=employee, update=update)
    
    from flask import current_app
    send_email(subject, manager.email, text_body, html_body, current_app._get_current_object())

def send_rating_notification_email(employee, rater, task, rating):
    """Send email when employee receives a rating"""
    subject = f"New Rating on Task: {task.title}"
    text_body = f"""Hi {employee.get_full_name()},

{rater.get_full_name()} has given you a rating for the task "{task.title}":

Rating: {'⭐' * rating.stars} ({rating.stars}/5)
Comment: {rating.comment if rating.comment else 'No comment'}

Keep up the great work!

Best regards,
Task Manager System"""
    
    html_body = render_template('email/rating_notification.html',
                               employee=employee, rater=rater, task=task, rating=rating)
    
    from flask import current_app
    send_email(subject, employee.email, text_body, html_body, current_app._get_current_object())
