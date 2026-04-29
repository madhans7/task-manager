# Task Management Application

A comprehensive Python-based task management system that allows managers to assign tasks to employees and track their progress with real-time updates, star ratings, and email notifications.

## Features

✨ **Core Features:**
- ✅ **Task Management**: Create, assign, edit, and delete tasks
- 📊 **Progress Tracking**: Real-time progress bars (0-100%)
- ⭐ **Star Ratings**: Rate employee performance on completed tasks
- 📧 **Email Notifications**: Automatic email updates for task assignments, progress, and ratings
- 👥 **Role-Based Access**: Separate views for managers and employees
- 🔐 **User Authentication**: Secure login and registration system
- 📋 **Task Updates**: Employees can submit detailed progress updates

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Email**: Flask-Mail (SMTP)
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF with WTForms

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone or navigate to project directory:**
   ```bash
   cd c:\Users\kmvai\Desktop\webapp
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Email Settings:**
   - Open `config.py`
   - Update the following with your email credentials:
     ```python
     MAIL_USERNAME = 'your_email@gmail.com'
     MAIL_PASSWORD = 'your_app_password'  # Use Gmail App Password, not regular password
     MAIL_DEFAULT_SENDER = ('Task Manager', 'your_email@gmail.com')
     ```

   **For Gmail:**
   - Enable 2-Factor Authentication on your Google Account
   - Generate an App Password: https://myaccount.google.com/apppasswords
   - Use the generated 16-character password in config.py

6. **Initialize the database:**
   ```bash
   python
   >>> from app import create_app, db
   >>> app = create_app()
   >>> with app.app_context():
   >>>     db.create_all()
   >>> exit()
   ```

7. **Run the application:**
   ```bash
   python run.py
   ```

8. **Access the application:**
   - Open your browser and go to: `http://localhost:5000`

## Default Credentials

After initial setup, you can create accounts through the registration page.

## User Roles

### Manager
- Create and assign tasks to employees
- View all tasks and employee updates
- Rate employee performance
- View employee statistics and profiles
- Send email notifications

### Employee
- View assigned tasks
- Submit task progress updates
- Receive ratings and feedback
- See all updates from other employees
- Update profile information

## Application Structure

```
webapp/
├── app/
│   ├── templates/
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── email/
│   │   │   ├── task_assigned.html
│   │   │   ├── update_notification.html
│   │   │   └── rating_notification.html
│   │   ├── errors/
│   │   │   ├── 404.html
│   │   │   └── 500.html
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── task_detail.html
│   │   ├── task_create.html
│   │   ├── task_update.html
│   │   ├── task_edit.html
│   │   ├── profile.html
│   │   ├── my_updates.html
│   │   ├── all_updates.html
│   │   ├── employees.html
│   │   └── search_results.html
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── main.js
│   │   └── images/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── auth.py
│   ├── main.py
│   ├── tasks.py
│   └── email_utils.py
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

## Database Models

### Employee
- Username, Email, Password
- First/Last Name
- Manager Flag
- Active Status

### Task
- Title, Description
- Created By, Assigned To
- Status (Pending, In Progress, Completed)
- Priority (Low, Medium, High)
- Progress (0-100%)
- Due Date

### TaskUpdate
- Task Reference
- Employee (Author)
- Update Text
- Progress Percentage
- Status
- Timestamp

### Rating
- Task Reference
- Rater (Employee/Manager)
- Stars (1-5)
- Comment
- Timestamp

## Usage Guide

### For Managers

1. **Create a Task:**
   - Go to "Create Task" in navigation
   - Fill in title, description, assign to employee
   - Set priority and due date
   - Click "Create Task"

2. **View Updates:**
   - Go to "Dashboard" to see all tasks
   - Click on any task to see updates and ratings
   - Reviews will be sent via email

3. **Rate Employees:**
   - Open a task assigned to an employee
   - Rate the work from 1-5 stars
   - Add optional comment

### For Employees

1. **View Tasks:**
   - Dashboard shows all assigned tasks
   - Click on a task for details

2. **Submit Updates:**
   - Open assigned task
   - Click "Submit Update"
   - Add progress message
   - Update progress percentage (0-100%)
   - Change status as needed
   - Manager will be notified via email

3. **View All Updates:**
   - Click on "All Updates" in navigation
   - See what other employees are working on
   - Click through to view complete task details

## Features in Detail

### Progress Tracking
- **Real-time Progress Bars**: Visual representation of task completion
- **Automatic Updates**: Progress is updated when employees submit updates
- **Historical Tracking**: See all progress updates over time

### Star Rating System
- **5-Star Scale**: Rate employee performance from 1-5 stars
- **Comments**: Add feedback with ratings
- **Average Ratings**: View average rating for employees
- **Prevent Self-Rating**: Employees cannot rate their own tasks

### Email Notifications
- **Task Assignment**: Employee receives email when task is assigned
- **Progress Updates**: Manager receives email when employee submits update
- **Ratings**: Employee receives email when they're rated

### Search & Filter
- **Task Search**: Search tasks by title or description
- **Status Filter**: Filter tasks by status
- **Priority Filter**: Filter by task priority
- **Pagination**: Navigate through large task lists

## API Endpoints

### Authentication
- `POST /auth/register` - Create new account
- `POST /auth/login` - User login
- `GET /auth/logout` - User logout

### Main
- `GET /` - Dashboard
- `GET /dashboard` - Dashboard
- `GET /task/<id>` - View task details
- `GET /my-updates` - View my updates
- `GET /all-updates` - View all updates
- `GET /profile` - User profile
- `GET /employees` - View all employees

### Tasks
- `GET /tasks/create` - Create task form
- `POST /tasks/create` - Submit create task
- `GET /tasks/<id>/update` - Submit update form
- `POST /tasks/<id>/update` - Submit update
- `POST /tasks/<id>/rate` - Submit rating
- `GET /tasks/<id>/edit` - Edit task form
- `POST /tasks/<id>/edit` - Submit edit
- `POST /tasks/<id>/delete` - Delete task
- `GET /tasks/search` - Search tasks

## Troubleshooting

### Email Not Sending
1. Check email credentials in `config.py`
2. Verify Gmail App Password (not regular password)
3. Ensure "Less secure app access" is disabled for modern Gmail
4. Check that MAIL_SERVER is set to 'smtp.gmail.com'

### Database Issues
1. Delete `task_manager.db` file if corrupted
2. Reinitialize database with the setup instructions
3. Check file permissions in the webapp directory

### Login Issues
1. Ensure you've created an account via registration
2. Check that account is active (is_active = True)
3. Verify username/password are correct

### Static Files Not Loading
1. Ensure you're in the correct directory
2. Check that `app/static/` folder exists with CSS/JS files
3. Clear browser cache and refresh

## Security Considerations

- Passwords are hashed using Werkzeug security
- CSRF protection enabled with Flask-WTF
- Session management with Flask-Login
- SQL injection protection via SQLAlchemy ORM
- Email validation for new accounts

**⚠️ For Production:**
- Change `SECRET_KEY` in config.py
- Use environment variables for sensitive data
- Enable HTTPS/SSL
- Use a production database (PostgreSQL, MySQL)
- Implement rate limiting
- Add CORS configuration if needed

## Development

### Running in Debug Mode
```bash
python run.py
```

### Creating Test Data
```bash
python
>>> from app import create_app, db
>>> from app.models import Employee
>>> app = create_app()
>>> with app.app_context():
>>>     # Create test manager
>>>     manager = Employee(username='manager', email='manager@test.com', first_name='John', last_name='Manager', is_manager=True)
>>>     manager.set_password('password123')
>>>     db.session.add(manager)
>>>     
>>>     # Create test employee
>>>     emp = Employee(username='employee', email='emp@test.com', first_name='Jane', last_name='Employee')
>>>     emp.set_password('password123')
>>>     db.session.add(emp)
>>>     db.session.commit()
```

## Future Enhancements

- [ ] Real-time notifications with WebSocket
- [ ] File attachments for updates
- [ ] Advanced analytics and reporting
- [ ] Team/Department management
- [ ] Calendar view for tasks
- [ ] Mobile app version
- [ ] Integration with Slack/Teams
- [ ] Automated reports and dashboards
- [ ] Task templates
- [ ] Recurring tasks

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please create an issue in the repository or contact the development team.

---

**Built with ❤️ for better task management**
