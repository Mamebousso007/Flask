from functools import wraps
from flask import Blueprint, jsonify, request, current_app
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.models import User, db, RoleEnum
from app.schemas import UserSchema
from marshmallow import ValidationError
import jwt

auth_bp = Blueprint('auth_bp', __name__)
bcrypt = Bcrypt()
user_schema = UserSchema()

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Vérifier si le token est fourni dans le header
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({"message": "Token is missing"}), 401
            
            # Retirer le mot 'Bearer ' du token
            token = token.split()[1] if 'Bearer' in token else token

            try:
                # Décoder le token JWT
                data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
                user = User.query.get(data['sub'])  # Vérification de l'utilisateur par l'ID

                # Vérifier le rôle
                if user.role != role:
                    return jsonify({"message": "You do not have permission to access this resource."}), 403
            except jwt.ExpiredSignatureError:
                return jsonify({"message": "Token has expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Invalid token"}), 401

            return f(*args, **kwargs)
        return decorated
    return decorator


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        # Validation des données avec Marshmallow
        data = user_schema.load(request.get_json())

        if User.query.filter_by(email=data['email']).first():
            return jsonify({"message": "User already exists"}), 400

        new_user = User(
            username=data['username'],
            email=data['email'],
            #role=RoleEnum.ADMIN if data.get('is_admin') else RoleEnum.USER
            #role=RoleEnum.ADMIN if data.get('is_admin', False) else RoleEnum.USER 
            role=RoleEnum[data['role']]
        )
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except ValidationError as err:
        return jsonify(err.messages), 400

@auth_bp.route('/login', methods=['POST'], endpoint='login')
def login():
    data = request.get_json()
    
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id)  
        return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route('/protected', methods=['GET'])
@jwt_required() 
def protected_route():
    current_user = get_jwt_identity()
    return jsonify({"message": "You have access to this route!"}), 200

@auth_bp.route('/admin', methods=['GET'])
@jwt_required()
@role_required(RoleEnum.ADMIN)  # Vérifie que l'utilisateur a le rôle ADMIN
def admin_route():
    return jsonify({"message": "Welcome Admin!"}), 200
