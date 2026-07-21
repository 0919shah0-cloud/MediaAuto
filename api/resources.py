"""API Resources"""
from flask_restful import Resource, reqparse
from flask import request
from datetime import datetime

from utils.logger import setup_logger
from database.manager import DatabaseManager
from database.models import Channel, Post

logger = setup_logger(__name__)

db_manager = None


def init_db(db: DatabaseManager):
    """Initialize database manager
    
    Args:
        db: DatabaseManager instance
    """
    global db_manager
    db_manager = db


class HealthResource(Resource):
    """Health check endpoint"""
    
    def get(self):
        """Get health status"""
        return {'status': 'ok', 'timestamp': datetime.now().isoformat()}


class StatsResource(Resource):
    """Statistics endpoint"""
    
    def get(self):
        """Get statistics"""
        try:
            posts = db_manager.get_posts()
            sent = len([p for p in posts if p.status == 'sent'])
            pending = len([p for p in posts if p.status == 'pending'])
            failed = len([p for p in posts if p.status == 'failed'])
            
            return {
                'total_posts': len(posts),
                'sent_posts': sent,
                'pending_posts': pending,
                'failed_posts': failed,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {'error': str(e)}, 500


class PostsResource(Resource):
    """Posts endpoint"""
    
    def get(self, post_id=None):
        """Get posts"""
        try:
            if post_id:
                post = db_manager.get_post(post_id)
                if not post:
                    return {'error': 'Post not found'}, 404
                return self._format_post(post)
            
            posts = db_manager.get_posts()
            return [self._format_post(p) for p in posts]
        except Exception as e:
            logger.error(f"Error getting posts: {e}")
            return {'error': str(e)}, 500
    
    def post(self):
        """Create post"""
        try:
            data = request.json
            post = Post(
                original_caption=data.get('caption'),
                media_path=data.get('media_path'),
                status='pending'
            )
            db_manager.add_post(post)
            return {'success': True, 'post_id': post.id}, 201
        except Exception as e:
            logger.error(f"Error creating post: {e}")
            return {'error': str(e)}, 500
    
    @staticmethod
    def _format_post(post):
        """Format post for JSON"""
        return {
            'id': post.id,
            'caption': post.original_caption,
            'status': post.status,
            'created_at': post.created_at.isoformat(),
            'sent_at': post.sent_at.isoformat() if post.sent_at else None
        }


class ChannelsResource(Resource):
    """Channels endpoint"""
    
    def get(self, channel_id=None):
        """Get channels"""
        try:
            if channel_id:
                channel = db_manager.get_channel(channel_id)
                if not channel:
                    return {'error': 'Channel not found'}, 404
                return self._format_channel(channel)
            
            channels = db_manager.get_channels()
            return [self._format_channel(ch) for ch in channels]
        except Exception as e:
            logger.error(f"Error getting channels: {e}")
            return {'error': str(e)}, 500
    
    def post(self):
        """Add channel"""
        try:
            data = request.json
            channel = Channel(
                channel_id=data.get('channel_id'),
                title=data.get('title'),
                channel_type=data.get('type', 'source')
            )
            db_manager.add_channel(channel)
            return {'success': True, 'channel_id': channel.id}, 201
        except Exception as e:
            logger.error(f"Error adding channel: {e}")
            return {'error': str(e)}, 500
    
    def delete(self, channel_id):
        """Delete channel"""
        try:
            db_manager.delete_channel(channel_id)
            return {'success': True, 'message': 'Channel deleted'}
        except Exception as e:
            logger.error(f"Error deleting channel: {e}")
            return {'error': str(e)}, 500
    
    @staticmethod
    def _format_channel(channel):
        """Format channel for JSON"""
        return {
            'id': channel.id,
            'channel_id': channel.channel_id,
            'title': channel.title,
            'type': channel.channel_type,
            'is_active': channel.is_active,
            'created_at': channel.created_at.isoformat()
        }


class SettingsResource(Resource):
    """Settings endpoint"""
    
    def get(self, key=None):
        """Get settings"""
        try:
            if key:
                setting = db_manager.get_setting(key)
                if not setting:
                    return {'error': 'Setting not found'}, 404
                return {'key': key, 'value': setting.value}
            return {'error': 'Key required'}, 400
        except Exception as e:
            logger.error(f"Error getting setting: {e}")
            return {'error': str(e)}, 500
    
    def post(self, key=None):
        """Set setting"""
        try:
            if not key:
                return {'error': 'Key required'}, 400
            
            data = request.json
            db_manager.set_setting(key, data.get('value'))
            return {'success': True, 'message': 'Setting updated'}
        except Exception as e:
            logger.error(f"Error setting value: {e}")
            return {'error': str(e)}, 500
