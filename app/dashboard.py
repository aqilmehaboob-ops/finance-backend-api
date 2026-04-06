from flask import Blueprint, jsonify, request
from app import db
from .models import Finance, User
from sqlalchemy import func
from .financial_records import require_role

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/dashboard/<int:user_id>", methods=['GET'])
def dashboard_summary(user_id):

    user = User.query.get_or_404(user_id)

    if not require_role(user, ["admin", "analyst"]):
        return {"error": "Forbidden"}, 403

    total_income = db.session.query(func.sum(Finance.amount))\
        .filter_by(tpe="income", user_id=user_id).scalar() or 0
    
    total_expense = db.session.query(func.sum(Finance.amount))\
        .filter_by(tpe = "expense", user_id=user_id).scalar() or 0
    
    category_totals = db.session.query(
    Finance.category,
    func.sum(Finance.amount)
).filter_by(user_id=user_id).group_by(Finance.category).all()
    
    category_data = []

    for category, total in category_totals:
        category_data.append({
            "category": category,
            "total": total
        })
    
    balance = total_income - total_expense

    return jsonify({
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "category_breakdown": category_data
    }), 200

