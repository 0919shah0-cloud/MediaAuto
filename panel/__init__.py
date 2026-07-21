"""Panel Module - Web Dashboard"""
from .app import create_app
from .routes import bp

__all__ = ['create_app', 'bp']
