from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_filename='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import auth, artwork, gallery, order
    app.register_blueprint(auth.bp)
    app.register_blueprint(artwork.bp)
    app.register_blueprint(gallery.bp)
    app.register_blueprint(order.bp)

    return app
