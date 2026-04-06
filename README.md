# Finance Backend API

A Flask-based backend system for managing financial records with role-based access control.

## Features
- User management (Admin, Analyst, Viewer)
- Financial record CRUD
- Dashboard analytics (income, expense, balance, category)
- Role-based access control

## Tech Stack
- Python
- Flask
- SQLAlchemy
- SQLite

## How to Run
1. Clone repo
2. Create virtual environment
3. Install dependencies
4. Run:
   python run.py

## API Testing
Tested using Postman

## API Documentation

### Base URL
http://127.0.0.1:5000/

---

### User APIs

**Create User**
POST /users  
Body:
{
  "name": "user",
  "password": "123",
  "role": "admin"
}

**Get All Users (Admin only)**
GET /users?admin_id=1

**Update User**
PUT /users/<user_id>?admin_id=1

**Delete User**
DELETE /users/<user_id>?admin_id=1

**Update User Status**
PUT /users/<user_id>/status?admin_id=1  
Body:
{
  "is_active": true
}

---

### Finance APIs

**Create Record**
POST /finance/<user_id>

**Get Records**
GET /finance/<user_id>

**Update Record**
PUT /finance/<finance_id>?admin_id=1

**Delete Record**
DELETE /finance/<finance_id>?admin_id=1

---

### Dashboard API

**Get Summary**
GET /dashboard/<user_id>

Returns:
- total_income
- total_expense
- balance
- category_breakdown
