from pathlib import Path
from dotenv import load_dotenv
import os
from flask import Flask, send_from_directory
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from server.config import Config
from server.db.database import db
from flask_cors import CORS

# Load environment variables
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

def create_app(config_class=Config):
    app = Flask(__name__,
                static_folder='../client/dist',  # Adjust this to 'build' if using Create React App
                static_url_path='')  # Serve at root

    app.config.from_object(config_class)

    # Init extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    CORS(app)

    # Register blueprints
    from server.controllers.auth_controller import auth_bp
    from server.controllers.mood_controller import mood_bp
    from server.controllers.user_controller import users_bp
    from server.controllers.artist_controller import artist_bp
    from server.controllers.genre_controller import genre_bp
    from server.controllers.music_controller import music_bp
    from server.controllers.songs_controller import songs_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(mood_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(artist_bp)
    app.register_blueprint(genre_bp)
    app.register_blueprint(music_bp)
    app.register_blueprint(songs_bp)

    # Serve frontend index.html
    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    # Serve static assets (e.g., CSS, JS)
    @app.route('/<path:path>')
    def serve_static(path):
        file_path = os.path.join(app.static_folder, path)
        if os.path.exists(file_path):
            return send_from_directory(app.static_folder, path)
        else:
            # Fallback to index.html for React Router
            return send_from_directory(app.static_folder, 'index.html')

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return {"error": "Resource not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {"error": "Internal server error"}, 500

    return app

app = create_app()
