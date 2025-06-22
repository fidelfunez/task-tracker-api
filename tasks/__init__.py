from flask import Blueprint

# Create tasks blueprint
tasks_bp = Blueprint('tasks', __name__)

# Import routes to register them with the blueprint
from tasks import routes
