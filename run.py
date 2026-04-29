from app import create_app, db
import os

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Context for Flask shell"""
    return {'db': db}

@app.before_request
def before_request():
    """Before each request"""
    from flask import session
    from datetime import timedelta
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=7)

@app.errorhandler(404)
def not_found(e):
    """404 error handler"""
    from flask import render_template
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """500 error handler"""
    from flask import render_template
    db.session.rollback()
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
