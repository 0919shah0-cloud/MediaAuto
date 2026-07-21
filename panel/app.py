"""Flask Application Factory"""
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from utils.logger import setup_logger

logger = setup_logger(__name__)

db = SQLAlchemy()


def create_app(config_path: str = "config.json") -> Flask:
    """Create Flask application
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Configuration
    app.config['JSON_AS_ASCII'] = False
    app.config['JSON_SORT_KEYS'] = False
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    
    # Register blueprints
    from .routes import bp
    app.register_blueprint(bp)
    
    logger.info("Flask app created")
    return app
