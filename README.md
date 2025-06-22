# Task Tracker API

A Flask-based REST API for task management with JWT authentication. Users can register, login, and manage their personal tasks with full CRUD operations.

## Features

- **User Authentication**: Registration and login with JWT token-based authentication
- **Task Management**: Complete CRUD operations for tasks
- **User Isolation**: Users can only access and manage their own tasks
- **Input Validation**: Comprehensive validation for all inputs
- **Error Handling**: Detailed error messages and appropriate HTTP status codes
- **Pagination**: Paginated task listings
- **Task Statistics**: Get completion statistics for tasks
- **RESTful Design**: Clean and intuitive API endpoints

## Tech Stack

- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **Flask-JWT-Extended**: JWT token authentication
- **Flask-Bcrypt**: Password hashing
- **Marshmallow**: Input validation and serialization
- **SQLite**: Database (development) / PostgreSQL (production ready)

## Project Structure

