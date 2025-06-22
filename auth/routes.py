from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError
from auth import auth_bp
from app import db, bcrypt
from models import User
from schemas import UserRegistrationSchema, UserLoginSchema
import logging

# Initialize schemas
user_registration_schema = UserRegistrationSchema()
user_login_schema = UserLoginSchema()

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        # Get JSON data from request
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No input data provided'}), 400
        
        # Validate input data
        data = user_registration_schema.load(json_data)
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 409
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 409
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        logging.info(f"New user registered: {user.username}")
        
        # Create access token
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'access_token': access_token
        }), 201
        
    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'messages': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        logging.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'Registration failed', 'message': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return token"""
    try:
        # Get JSON data from request
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No input data provided'}), 400
        
        # Validate input data
        data = user_login_schema.load(json_data)
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == data['username_or_email']) | 
            (User.email == data['username_or_email'])
        ).first()
        
        # Check if user exists and password is correct
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Create access token
        access_token = create_access_token(identity=str(user.id))
        
        logging.info(f"User logged in: {user.username}")
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token
        }), 200
        
    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'messages': err.messages}), 400
    except Exception as e:
        logging.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed', 'message': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        logging.error(f"Get current user error: {str(e)}")
        return jsonify({'error': 'Failed to get user information'}), 500
