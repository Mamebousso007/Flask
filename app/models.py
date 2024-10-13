from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, Enum  # Importez Enum à partir de SQLAlchemy
from app import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class RoleEnum(PyEnum):
    ADMIN = "ADMIN"
    USER = "USER"

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(50), unique=True, nullable=False) 
    email = db.Column(db.String(120), unique=True, nullable=False)  
    password = db.Column(db.String(255), nullable=False)  # Utiliser 'password' pour stocker le hachage
    role = db.Column(Enum(RoleEnum), nullable=False) 

    def set_password(self, password):
        # Hache le mot de passe et le stocke dans le champ 'password'
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        # Vérifie si le mot de passe donné correspond au mot de passe haché
        return bcrypt.check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }

    def __repr__(self):
        return f'<User {self.username}>'

# One-to-Many (Un à Plusieurs)
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  

    user = db.relationship('User', backref='posts') 

    def __repr__(self):
        return f'<Post {self.title}>'


# Many-to-Many
group_user = db.Table('group_user',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True)
)

class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    users = db.relationship('User', secondary=group_user, backref='groups')  # Relation Many-to-Many

    def __repr__(self):
        return f'<Group {self.name}>'
