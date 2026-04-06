#CRUD OPERATIONS ON USERS

from app import db
from flask import Blueprint, request, jsonify
from .models import User
from .financial_records import require_role

users = Blueprint("users", __name__)

@users.route("/users", methods=['POST'])
def create_user():

    data = request.get_json()

    if not data:
        return {"error": "invalid data"}

    name = data.get('name')
    password = data.get('password')
    role = data.get('role')

    if not name or not password or not role:
        return {"error": "invalid data"}, 400
    
    existing_user = User.query.filter_by(name=name).first()
    if existing_user:
        return {"error": "Username already exists"}, 400

    user = User(name=name, password=password, role=role)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User created",
        "user_id": user.id,
        "name": user.name,
        "role": user.role
        }), 201



@users.route("/users", methods=['GET'])
def view_user():

    admin_id = request.args.get('admin_id', type=int)

    if not admin_id:
        return {"error": "admin_id required"}, 400
    
    admin = User.query.get(admin_id)

    if not admin:
        return {"error": "user not found"}, 404
    
    if not require_role(admin, ["admin"]):
        return {"error": "Forbidden"}, 403

    if not admin.is_active:
        return {"error": "User inactive"}, 403

    lst = []

    users = User.query.all()

    for u in users:
        lst.append({
            "user_id": u.id,
            "user_name": u.name,
            "user_role": u.role,
            "user_status": u.is_active
        })

    return jsonify(lst), 200



@users.route("/users/<int:user_id>", methods=['PUT'])
def update_user(user_id):

    admin_id = request.args.get('admin_id', type=int)

    if not admin_id:
        return {"error": "Admin_id required"}, 400
    
    admin = User.query.get_or_404(admin_id)
    
    if not require_role(admin, ["admin"]):
        return {"error": "Forbidden"}, 403
    
    data = request.get_json()

    if not data:
        return {"error": "Invalid data"}, 400
    
    existing_user = User.query.filter_by(name=data['name']).first()
    if existing_user:
        return {"error": "Username already exists"}, 400

    user = User.query.get_or_404(user_id)

    if 'name' in data:
        user.name = data['name']
    
    if 'role' in data:
        user.role = data['role']

    db.session.commit()

    return jsonify({
        "message": "user updated",
        "user_name": user.name,
        "user_role": user.role
    }), 200



@users.route("/users/<int:user_id>", methods=['DELETE'])
def delete_user(user_id):

    admin_id = request.args.get('admin_id', type=int)

    if not admin_id:
        return {"error": "Admin_id required"}, 400
    
    admin = User.query.get_or_404(admin_id)
    
    if not require_role(admin, ["admin"]):
        return {"error": "Forbidden"}, 403

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return jsonify({
        "message": "user_deleted"
    }), 200



@users.route("/users/<int:user_id>/status", methods=['PUT'])
def update_status(user_id):

    admin_id = request.args.get('admin_id')

    if not admin_id:
        return {"error": "Admin_id required"}, 400
    
    admin = User.query.get_or_404(admin_id)
    
    if not require_role(admin, ["admin"]):
        return {"error": "Forbidden"}, 403

    data = request.get_json()

    is_active = data.get('is_active')

    user = User.query.get_or_404(user_id)

    if isinstance(data.get('is_active'), bool):
        user.is_active = data.get('is_active')
    else:
        return {"error": "Invalid status"}, 400

    db.session.commit()

    return {"message": "status updated"}, 200
