from flask import Blueprint, request, jsonify
from app import db
from .models import Finance, User

finance = Blueprint("finance", __name__)

def require_role(user, allowed_role):
    if user.role not in allowed_role:
        return False
    return True

@finance.route("/finance", methods=['GET'])
def all_transaction():

    admin_id = request.args.get('admin_id', type=int)

    if not admin_id:
        return {"error": "admin id required"}, 400
    
    admin = User.query.get(admin_id)

    if not admin:
        return {"error": "User not found"}, 404
    
    if not admin.is_active:
        return {"error": "Forbidden"}, 403
    
    if not require_role(admin, ["admin"]):
        return {"error": "Forbidden"}, 403

    all_transaction = Finance.query.all()

    lst=[]

    for transaction in all_transaction:
        lst.append({
            "transaction_id": transaction.id,
            "transaction_amount": transaction.amount,
            "transaction_type": transaction.tpe,
            "transaction_category": transaction.category,
            "transaction_date": transaction.date,
            "transaction_notes": transaction.notes,
            "transaction_user_id": transaction.user_id
        })

    return jsonify(lst), 200



@finance.route("/finance/<int:user_id>", methods=['POST'])
def create_record(user_id):

    data = request.get_json()

    user = User.query.filter_by(id=user_id).first_or_404()

    amount = data.get('amount')
    tpe = data.get('tpe')
    category = data.get('category')
    date = data.get('date')
    notes = data.get('notes')

    if not amount or not tpe or not category or not date or not notes:
        return {"error": "Invalid data"}, 400

    if not require_role(user, ["admin", "analyst"]):
        return {"error": "Forbidden"}, 403

    finance = Finance(amount=amount, tpe=tpe, category=category, date=date, notes=notes, user_id=user.id)

    db.session.add(finance)
    db.session.commit()

    return jsonify({
        "message": "finance_record_created_magic",
        "id": finance.id,
        "amount": finance.amount,
        "type": finance.tpe,
        "category": finance.category,
        "date": finance.date,
        "notes": finance.notes,
        "role": user.role,
        "user_id": user.id
    }), 200

@finance.route("/finance/<int:user_id>", methods=['GET'])
def get_finance(user_id):

    user = User.query.get_or_404(user_id)

    if not require_role(user, ["viewer", "admin", "analyst"]):
        return {"error": "unauthorized"}, 403
    
    lst=[]

    all_finance = Finance.query.filter_by(user_id=user_id).all()

    for finance in all_finance:
        lst.append({
        "id": finance.id,
        "amount": finance.amount,
        "type": finance.tpe,
        "category": finance.category,
        "date": finance.date,
        "notes": finance.notes,
        "user_id": finance.user_id,
        "user_role": user.role
        })

    return jsonify(lst), 200



@finance.route("/finance/<int:finance_id>", methods=['PUT'])
def update_finance(finance_id):

    admin_id = request.args.get('admin_id', type=int)

    if not admin_id:
        return {"error": "Admin_id required"}, 400
    
    admin = User.query.get_or_404(admin_id)
    
    if not require_role(admin, ["admin"]):
        return {"error": "Forbidden"}, 403

    data = request.get_json()

    finance = Finance.query.get_or_404(finance_id)

    finance.amount = data.get('amount')
    finance.tpe = data.get('tpe')
    finance.category = data.get('category')
    finance.date = data.get('date')
    finance.notes = data.get('notes')

    db.session.commit()

    return jsonify({"message": "updated"}), 200



@finance.route("/finance/<int:finance_id>", methods=["DELETE"])
def delete_finance(finance_id):

    admin_id = request.args.get('admin_id', type=int)

    if not admin_id:
        return {"error": "Admin_id required"}, 400
    
    admin = User.query.get_or_404(admin_id)
    
    if not require_role(admin, ["admin"]):
        return {"error": "Forbidden"}, 403

    finance = Finance.query.get_or_404(finance_id)

    db.session.delete(finance)
    db.session.commit()

    return {"message": "finance deleted"}, 200
