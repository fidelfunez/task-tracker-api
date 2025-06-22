from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from datetime import datetime
from tasks import tasks_bp
from app import db
from models import Task, User
from schemas import TaskCreateSchema, TaskUpdateSchema
from utils import parse_date
import logging

# Initialize schemas
task_create_schema = TaskCreateSchema()
task_update_schema = TaskUpdateSchema()

@tasks_bp.route('', methods=['GET'])
@jwt_required()
def get_tasks():
    """Get all tasks for the current user"""
    try:
        current_user_id = get_jwt_identity()
        
        # Query parameters for filtering and pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        completed = request.args.get('completed', type=str)
        
        # Build query
        query = Task.query.filter_by(user_id=current_user_id)
        
        # Filter by completion status if provided
        if completed is not None:
            if completed.lower() == 'true':
                query = query.filter_by(completed=True)
            elif completed.lower() == 'false':
                query = query.filter_by(completed=False)
        
        # Order by creation date (newest first)
        query = query.order_by(Task.created_at.desc())
        
        # Paginate results
        pagination = query.paginate(
            page=page, 
            per_page=min(per_page, 100),  # Limit max per_page to 100
            error_out=False
        )
        
        tasks = [task.to_dict() for task in pagination.items]
        
        return jsonify({
            'tasks': tasks,
            'pagination': {
                'page': pagination.page,
                'pages': pagination.pages,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        logging.error(f"Get tasks error: {str(e)}")
        return jsonify({'error': 'Failed to retrieve tasks'}), 500

@tasks_bp.route('', methods=['POST'])
@jwt_required()
def create_task():
    """Create a new task for the current user"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get JSON data from request
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No input data provided'}), 400
        
        # Validate input data
        data = task_create_schema.load(json_data)
        
        # Parse due_date if provided
        due_date = None
        if data.get('due_date'):
            due_date = parse_date(data['due_date'])
            if not due_date:
                return jsonify({'error': 'Invalid due_date format. Use YYYY-MM-DD'}), 400
        
        # Create new task
        task = Task(
            title=data['title'],
            description=data.get('description', ''),
            due_date=due_date,
            completed=data.get('completed', False),
            user_id=current_user_id
        )
        
        # Save to database
        db.session.add(task)
        db.session.commit()
        
        logging.info(f"New task created: {task.title} by user {current_user_id}")
        
        return jsonify({
            'message': 'Task created successfully',
            'task': task.to_dict()
        }), 201
        
    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'messages': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        logging.error(f"Create task error: {str(e)}")
        return jsonify({'error': 'Failed to create task', 'message': str(e)}), 500

@tasks_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    """Get a specific task by ID"""
    try:
        current_user_id = get_jwt_identity()
        
        # Find task and ensure it belongs to current user
        task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        return jsonify({
            'task': task.to_dict()
        }), 200
        
    except Exception as e:
        logging.error(f"Get task error: {str(e)}")
        return jsonify({'error': 'Failed to retrieve task'}), 500

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """Update a specific task"""
    try:
        current_user_id = get_jwt_identity()
        
        # Find task and ensure it belongs to current user
        task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        # Get JSON data from request
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No input data provided'}), 400
        
        # Validate input data
        data = task_update_schema.load(json_data)
        
        # Update task fields
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'due_date' in data:
            if data['due_date']:
                due_date = parse_date(data['due_date'])
                if not due_date:
                    return jsonify({'error': 'Invalid due_date format. Use YYYY-MM-DD'}), 400
                task.due_date = due_date
            else:
                task.due_date = None
        if 'completed' in data:
            task.completed = data['completed']
        
        # Update timestamp
        task.updated_at = datetime.utcnow()
        
        # Save changes
        db.session.commit()
        
        logging.info(f"Task updated: {task.title} by user {current_user_id}")
        
        return jsonify({
            'message': 'Task updated successfully',
            'task': task.to_dict()
        }), 200
        
    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'messages': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        logging.error(f"Update task error: {str(e)}")
        return jsonify({'error': 'Failed to update task', 'message': str(e)}), 500

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """Delete a specific task"""
    try:
        current_user_id = get_jwt_identity()
        
        # Find task and ensure it belongs to current user
        task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        # Delete task
        db.session.delete(task)
        db.session.commit()
        
        logging.info(f"Task deleted: {task.title} by user {current_user_id}")
        
        return jsonify({
            'message': 'Task deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Delete task error: {str(e)}")
        return jsonify({'error': 'Failed to delete task', 'message': str(e)}), 500

@tasks_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_task_stats():
    """Get task statistics for the current user"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get task counts
        total_tasks = Task.query.filter_by(user_id=current_user_id).count()
        completed_tasks = Task.query.filter_by(user_id=current_user_id, completed=True).count()
        pending_tasks = total_tasks - completed_tasks
        
        # Get overdue tasks (due_date < today and not completed)
        today = datetime.utcnow().date()
        overdue_tasks = Task.query.filter(
            Task.user_id == current_user_id,
            Task.completed == False,
            Task.due_date < today
        ).count()
        
        return jsonify({
            'stats': {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'pending_tasks': pending_tasks,
                'overdue_tasks': overdue_tasks,
                'completion_rate': round((completed_tasks / total_tasks * 100), 2) if total_tasks > 0 else 0
            }
        }), 200
        
    except Exception as e:
        logging.error(f"Get task stats error: {str(e)}")
        return jsonify({'error': 'Failed to retrieve task statistics'}), 500
