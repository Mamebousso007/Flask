from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    FLASK_APP = os.getenv("FLASK_APP")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG")
    FLASK_ENV = os.getenv("FLASK_ENV")
    

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    SECRET_KEY = os.getenv('SECRET_KEY') 
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') 



# class TestingConfig(Config):
#     TESTING = True
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SECRET_KEY = os.getenv('SECRET_KEY')  # Utilise la clé du fichier .env
#     JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') 
