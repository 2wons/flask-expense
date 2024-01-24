from flask import Flask
from app.config import Config

def create_app(config_class = Config):

    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # register blueprints
    from app.auth import blueprint as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import blueprint as main_bp
    app.register_blueprint(main_bp)


    return app