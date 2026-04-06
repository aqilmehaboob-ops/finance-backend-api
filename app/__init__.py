from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///zovryn.db"

    db.init_app(app)

    from .user import users
    from .financial_records import finance
    from .dashboard import dashboard

    app.register_blueprint(users)
    app.register_blueprint(finance)
    app.register_blueprint(dashboard)

    return app