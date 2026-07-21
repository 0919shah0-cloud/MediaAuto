"""API Module"""
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from utils.logger import setup_logger

logger = setup_logger(__name__)


def create_api_app(config_path: str = "config.json") -> Flask:
    """Create API Flask application
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Configuration
    app.config['JSON_AS_ASCII'] = False
    
    # Initialize extensions
    CORS(app)
    api = Api(app)
    
    # Register resources
    from .resources import (
        PostsResource, ChannelsResource, SettingsResource,
        StatsResource, HealthResource
    )
    
    api.add_resource(HealthResource, '/health')
    api.add_resource(StatsResource, '/stats')
    api.add_resource(PostsResource, '/posts', '/posts/<int:post_id>')
    api.add_resource(ChannelsResource, '/channels', '/channels/<channel_id>')
    api.add_resource(SettingsResource, '/settings', '/settings/<key>')
    
    logger.info("API app created")
    return app
