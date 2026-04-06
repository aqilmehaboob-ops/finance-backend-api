from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(300))
    role = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)

class Finance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    tpe = db.Column(db.String)
    category = db.Column(db.String)
    date = db.Column(db.String)
    notes = db.Column(db.String)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=True)

