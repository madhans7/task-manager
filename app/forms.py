from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import Employee

class LoginForm(FlaskForm):
    """User login form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    """User registration form"""
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    is_manager = BooleanField('Register as Manager')
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        """Check if username already exists"""
        user = Employee.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        """Check if email already exists"""
        user = Employee.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')

class CreateTaskForm(FlaskForm):
    """Form to create a new task"""
    title = StringField('Task Title', validators=[DataRequired(), Length(min=5, max=120)])
    description = TextAreaField('Description', validators=[Length(max=1000)])
    assigned_to = SelectField('Assign To', coerce=int, validators=[DataRequired()])
    priority = SelectField('Priority', choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    due_date = StringField('Due Date (YYYY-MM-DD)', validators=[])
    submit = SubmitField('Create Task')

class TaskUpdateForm(FlaskForm):
    """Form to submit task updates"""
    update_text = TextAreaField('Comment', validators=[Length(max=500)])
    progress_percentage = IntegerField('Progress %', validators=[DataRequired()], render_kw={"min": 0, "max": 100})
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ])
    submit = SubmitField('Submit Update')

class RatingForm(FlaskForm):
    """Form to rate a task/employee"""
    stars = IntegerField('Rating (1-5)', validators=[DataRequired()], render_kw={"min": 1, "max": 5})
    submit = SubmitField('Submit Rating')

class UpdateProfileForm(FlaskForm):
    """Form to update user profile"""
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Profile')
    
    def validate_email(self, email):
        """Check if email already exists (excluding current user)"""
        from flask_login import current_user
        if email.data != current_user.email:
            user = Employee.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already registered. Please use a different one.')
