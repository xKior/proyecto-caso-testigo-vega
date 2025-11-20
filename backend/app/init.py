from flask import Flask, request, make_response
from flask_cors import CORS
from .database import init_db
import os

def create_app():
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False

    # Allow multiple origins via environment variable (comma-separated). Default includes project Vercel URL and localhost dev ports.
    default_origins = [
        "https://proyecto-caso-testigo-vega-hr72n8bgp-angels-projects-8c86d77d.vercel.app",
        "http://localhost:3000",
        "http://localhost:5173",
    ]
    raw = os.getenv('ALLOWED_ORIGINS')
    if raw:
        allowed_origins = [o.strip() for o in raw.split(',') if o.strip()]
    else:
        allowed_origins = default_origins

    # Scope CORS to /api/* (your blueprint uses url_prefix='/api')
    CORS(app, resources={r"/api/*": {"origins": allowed_origins, "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})

    # Reinforce CORS headers dynamically for any response (helps with some reverse proxies)
    @app.after_request
    def add_cors_headers(response):
        origin = request.headers.get('Origin')
        if '*' in allowed_origins:
            response.headers.setdefault('Access-Control-Allow-Origin', '*')
        elif origin and origin in allowed_origins:
            response.headers.setdefault('Access-Control-Allow-Origin', origin)
        response.headers.setdefault('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
        response.headers.setdefault('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        return response

    init_db(app)
    
    from .routes import bp
    app.register_blueprint(bp)
    
    return app
