from flask import Flask
from flask_cors import CORS
from .database import init_db

def create_app():
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    
    CORS(app)
    init_db(app)
    
    from .routes import bp
    app.register_blueprint(bp)
    
    return app