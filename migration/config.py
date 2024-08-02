# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # Or use your database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
