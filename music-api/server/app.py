from pathlib import Path
from dotenv import load_dotenv
import os
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from server.config import Config
from server.db.database import db, init_db
from flask_cors import CORS

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Register blueprints - ADD ALL CONTROLLERS HERE
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    CORS(app)

    # Initialize the database
    with app.app_context():
        db.create_all()

    

    # Register blueprints - ADD ALL CONTROLLERS HERE
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
    app.register_blueprint(songs_bp)
    app.register_blueprint(music_bp)
    
    
    # ADD ERROR HANDLERS
    @app.errorhandler(404)
    def not_found_error(error):
        return {"error": "Resource not found"}, 404
        
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {"error": "Internal server error"}, 500
    
    return app