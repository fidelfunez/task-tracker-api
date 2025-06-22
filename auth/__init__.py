from flask import Blueprint

# Create auth blueprint
auth_bp = Blueprint('auth', __name__)

# Import routes to register them with the blueprint
from auth import routes
