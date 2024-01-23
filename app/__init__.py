from flask import Flask

def create_app():

    app = Flask(__name__)
    
    # register blueprints
    from app.auth import blueprint as auth_bp
    app.register_blueprint(auth_bp)


    return app