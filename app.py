import os
import logging
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from config import Config

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Set secret key for sessions
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
    
    # ProxyFix for proper URL generation
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    # Register blueprints
    from auth import auth_bp
    from tasks import tasks_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
    
    # Global error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request', 'message': str(error)}), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': 'Forbidden', 'message': 'Insufficient permissions'}), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found', 'message': 'Resource not found'}), 404
    
    @app.errorhandler(422)
    def validation_error(error):
        return jsonify({'error': 'Validation error', 'message': str(error)}), 422
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error', 'message': 'Something went wrong'}), 500
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token expired', 'message': 'The token has expired'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Invalid token', 'message': 'The token is invalid'}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'error': 'Authorization required', 'message': 'Request does not contain an access token'}), 401
    
    # Root endpoint redirect
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Task Tracker API',
            'version': '1.0.0',
            'api_endpoint': '/api'
        })
    
    # API info endpoint
    @app.route('/api')
    def api_info():
        return jsonify({
            'message': 'Task Tracker API',
            'version': '1.0.0',
            'endpoints': {
                'auth': {
                    'register': 'POST /api/auth/register',
                    'login': 'POST /api/auth/login'
                },
                'tasks': {
                    'list': 'GET /api/tasks',
                    'create': 'POST /api/tasks',
                    'get': 'GET /api/tasks/<id>',
                    'update': 'PUT /api/tasks/<id>',
                    'delete': 'DELETE /api/tasks/<id>'
                }
            }
        })
    
    # Create database tables
    with app.app_context():
        # Import models to ensure they're registered
        import models
        db.create_all()
        logging.info("Database tables created successfully")
    
    return app

# Create app instance
app = create_app()
