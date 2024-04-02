from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = ('Please log in to access this page.')
login.login_message_category = ('warning')

def create_app(config_class = Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    
    # register blueprints
    from app.auth import blueprint as auth_bp
    app.register_blueprint(auth_bp)

    from app.records import blueprint as records_bp
    app.register_blueprint(records_bp)

    from app.expenses import blueprint as expenses_bp
    app.register_blueprint(expenses_bp)

    from app.incomes import blueprint as incomes_bp
    app.register_blueprint(incomes_bp)

    from app.budgets import blueprint as budgets_bp
    app.register_blueprint(budgets_bp)

    from app.subscriptions import blueprint as subs_bp
    app.register_blueprint(subs_bp)

    from app.main import blueprint as main_bp
    app.register_blueprint(main_bp)


    return app

from app import models