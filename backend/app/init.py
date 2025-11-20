from flask import Flask, request, make_response
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

    # Ensure the app responds to preflight OPTIONS requests for any path
    @app.before_request
    def handle_options():
        if request.method == 'OPTIONS':
            resp = make_response()
            resp.headers['Access-Control-Allow-Origin'] = "https://proyecto-caso-testigo-vega-hr72n8bgp-angels-projects-8c86d77d.vercel.app"
            resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
            resp.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
            resp.headers['Access-Control-Max-Age'] = '86400'
            return resp

    @app.after_request
    def add_cors_headers(response):
        # Reinforce CORS headers on all responses
        response.headers.setdefault('Access-Control-Allow-Origin', "https://proyecto-caso-testigo-vega-hr72n8bgp-angels-projects-8c86d77d.vercel.app")
        response.headers.setdefault('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
        response.headers.setdefault('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        return response

    init_db(app)
    
    from .routes import bp
    app.register_blueprint(bp)
    
    return app
