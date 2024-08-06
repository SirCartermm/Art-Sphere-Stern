from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///artsphere.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)
api = Api(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
CORS(app)  # Initialize CORS with default settings
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
migrate = Migrate(app, db)
