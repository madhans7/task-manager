from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import DevelopmentConfig

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app(config_class=DevelopmentConfig):
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configure proxy for Vercel
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    # Configure login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Register blueprints
    from app.auth import auth_bp
    from app.main import main_bp
    from app.tasks import tasks_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(tasks_bp)
    
    # Create database tables
    with app.app_context():
        try:
            import os
            if os.environ.get('VERCEL'):
                db_path = os.path.join('/tmp', 'task_manager.db')
                if not os.path.exists(db_path):
                    import shutil
                    # Copy bundled DB to /tmp
                    bundled_db = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'task_manager.db')
                    if os.path.exists(bundled_db):
                        shutil.copy2(bundled_db, db_path)
            db.create_all()
        except Exception as e:
            print(f"Error creating database: {e}")
    
    return app
