from marshmallow import Schema, fields, validate, validates, ValidationError
import re

class UserRegistrationSchema(Schema):
    """Schema for user registration validation"""
    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, max=64, error="Username must be between 3 and 64 characters"),
            validate.Regexp(
                r'^[a-zA-Z0-9_]+$',
                error="Username can only contain letters, numbers, and underscores"
            )
        ]
    )
    email = fields.Email(
        required=True,
        validate=validate.Length(max=120, error="Email must be less than 120 characters")
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6, max=128, error="Password must be between 6 and 128 characters")
    )
    
    @validates('password')
    def validate_password(self, value, **kwargs):
        """Validate password strength"""
        if not re.search(r'[A-Za-z]', value):
            raise ValidationError('Password must contain at least one letter')
        if not re.search(r'[0-9]', value):
            raise ValidationError('Password must contain at least one number')

class UserLoginSchema(Schema):
    """Schema for user login validation"""
    username_or_email = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=120, error="Username or email is required")
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Password is required")
    )

class TaskCreateSchema(Schema):
    """Schema for task creation validation"""
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=200, error="Title must be between 1 and 200 characters")
    )
    description = fields.Str(
        load_default='',
        validate=validate.Length(max=1000, error="Description must be less than 1000 characters")
    )
    due_date = fields.Str(
        load_default=None,
        allow_none=True,
        validate=validate.Regexp(
            r'^\d{4}-\d{2}-\d{2}$',
            error="Due date must be in YYYY-MM-DD format"
        )
    )
    completed = fields.Bool(load_default=False)

class TaskUpdateSchema(Schema):
    """Schema for task update validation"""
    title = fields.Str(
        validate=validate.Length(min=1, max=200, error="Title must be between 1 and 200 characters")
    )
    description = fields.Str(
        validate=validate.Length(max=1000, error="Description must be less than 1000 characters")
    )
    due_date = fields.Str(
        allow_none=True,
        validate=validate.Regexp(
            r'^\d{4}-\d{2}-\d{2}$',
            error="Due date must be in YYYY-MM-DD format"
        )
    )
    completed = fields.Bool()
