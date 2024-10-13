from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.auth import role_required
from app.models import RoleEnum, User
from app import db, bcrypt
from app.schemas import UserSchema
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

user_bp = Blueprint('user_bp', __name__)
user_schema = UserSchema()

@user_bp.route('/')
def index():
    return "Hello, User API!"



@user_bp.route('/users', methods=['GET'])
@jwt_required()  
@role_required(RoleEnum.ADMIN)  
def get_users():
    current_user = get_jwt_identity()
    users = User.query.all()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list), 200 

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user_schema.dump(user)), 200  

# Route pour mettre à jour un utilisateur 
@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@role_required(RoleEnum.ADMIN) 
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    try:
        updated_data = user_schema.load(request.json)

        user.username = updated_data['username']
        user.email = updated_data['email']
        user.password = bcrypt.generate_password_hash(updated_data['password']).decode('utf-8')
        db.session.commit()

        return jsonify(user_schema.dump(user)), 200

    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Route pour supprimer un utilisateur par son ID
@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required(RoleEnum.ADMIN)
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": f"User {user_id} deleted successfully"}), 200
