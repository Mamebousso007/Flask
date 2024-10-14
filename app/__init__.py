# app/__init__.py
from datetime import timedelta
import os
from config import Config
from dotenv import load_dotenv
from flask import Config, Flask, app, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

# Initialisation des extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=Config):
    load_dotenv()
    app = Flask(__name__)


    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # Configuration
    app.config.from_object('config.Config')
    app.config.from_object(Config)

    

    # Initialisation des extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    from app.models import User, Post, Group  

    # Import des blueprints
    from app.routes import user_bp
    from app.auth import auth_bp
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

 
    @app.errorhandler(Exception)
    def handle_exception(e):
        response = {
            "status": "error",
            "message": str(e),
        }
        return jsonify(response), 500
    
    # Configuration de Swagger
    SWAGGER_URL = '/swagger'
    API_URL = '/swagger.json'  

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Mon API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Route pour servir swagger.json
    @app.route('/swagger.json')
    def swagger_json():
        return send_from_directory('', 'swagger.json')

    return app

app = create_app()
