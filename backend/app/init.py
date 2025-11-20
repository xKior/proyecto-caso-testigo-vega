from flask import Flask
from flask_cors import CORS
from .database import init_db

def create_app():
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False

    CORS(app, resources={r"/*": {
        "origins": "https://proyecto-caso-testigo-vega-hr72n8bgp-angels-projects-8c86d77d.vercel.app",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
    }})

    init_db(app)
    
    from .routes import bp
    app.register_blueprint(bp)
    
    return app
