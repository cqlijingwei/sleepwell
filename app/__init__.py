from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import yaml

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = config['database']['url']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    from app.routes import api
    app.register_blueprint(api)
    
    with app.app_context():
        db.create_all()
    
    return app