# Task Tracker API 🧠✅

A simple but powerful Flask-based backend API that allows users to register, log in, and manage personal tasks securely. Built with SQLAlchemy, JWT authentication, and deployed on Render.

---

## 🚀 Live Demo

🔗 https://task-tracker-api-plv0.onrender.com/

---

## 📦 Features

- ✅ User Registration & Login
- 🔐 JWT-based Token Authentication
- 📝 Create, Read, Update, and Delete Tasks (CRUD)
- 📊 Task stats endpoint (optional)
- 🛠️ Modular Flask structure with Blueprints
- 🌐 Deployed live using Render

---

## 🔧 Tech Stack

- **Backend**: Python, Flask, Flask-JWT-Extended, SQLAlchemy
- **Database**: SQLite (PostgreSQL-ready)
- **Authentication**: JWT
- **Deployment**: Render.com
- **Tools**: Gunicorn, Git, GitHub

---

## 📫 How to Use (with Postman or curl)

### 🔐 Register

```http
POST /register
Content-Type: application/json

{
  "username": "fidel",
  "password": "secure123"
}
```

### 🔑 Login

```http
POST /login
Content-Type: application/json

{
  "username": "fidel",
  "password": "secure123"
}
```

**Returns:**

```json
{
  "access_token": "your.jwt.token.here"
}
```

Include this token in the Authorization header for all subsequent requests:

```
Authorization: Bearer your.jwt.token.here
```

---

### 📋 Create a Task

```http
POST /tasks
Content-Type: application/json

{
  "title": "Build README",
  "description": "Polish the final step",
  "due_date": "2025-07-01",
  "completed": false
}
```

### 📥 Get Tasks

```http
GET /tasks
Authorization: Bearer <your_token>
```

### ✏️ Update Task

```http
PUT /tasks/<id>
Authorization: Bearer <your_token>
```

### ❌ Delete Task

```http
DELETE /tasks/<id>
Authorization: Bearer <your_token>
```

---

## 📁 Project Structure

```
├── app.py
├── main.py
├── config.py
├── models.py
├── utils.py
├── auth/
│   ├── __init__.py
│   └── routes.py
├── tasks/
│   ├── __init__.py
│   └── routes.py
├── requirements.txt
├── Procfile
```

---

## 🙋‍♂️ About Me

Hi, I’m Fidel Fúnez. I'm a backend developer and Bitcoin educator based in Honduras, currently building my portfolio while helping others understand tech and financial freedom! - ₿

---

## 💡 Future Improvements (Perhaps) 

- Add a frontend (HTML/Flask or React)
- Role-based access control
- Email/password reset flow

---

## 📜 License

MIT — use it, fork it, build with it.
