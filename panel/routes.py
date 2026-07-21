"""Panel Routes"""
from flask import Blueprint, render_template, jsonify, request, session
from functools import wraps
from datetime import datetime

from utils.logger import setup_logger
from utils.security import verify_password, hash_password
from database.manager import DatabaseManager
from database.models import User, Channel, Post

logger = setup_logger(__name__)

bp = Blueprint('panel', __name__, url_prefix='/')

db_manager = None


def init_db(db: DatabaseManager):
    """Initialize database manager for routes
    
    Args:
        db: DatabaseManager instance
    """
    global db_manager
    db_manager = db


def login_required(f):
    """Decorator for login requirement"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function


# Authentication Routes
@bp.route('/api/auth/login', methods=['POST'])
def login():
    """Login endpoint"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        user = db_manager.get_user(username)
        if not user or not verify_password(password, user.password_hash):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        session['user_id'] = user.id
        logger.info(f"User {username} logged in")
        return jsonify({'success': True, 'message': 'Logged in successfully'})
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    """Logout endpoint"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out'})


# Dashboard Routes
@bp.route('/api/dashboard/stats', methods=['GET'])
@login_required
def get_stats():
    """Get dashboard statistics"""
    try:
        posts = db_manager.get_posts()
        pending = db_manager.get_posts(status='pending')
        sent = db_manager.get_posts(status='sent')
        failed = db_manager.get_posts(status='failed')
        
        stats = {
            'total_posts': len(posts),
            'pending_posts': len(pending),
            'sent_posts': len(sent),
            'failed_posts': len(failed),
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': str(e)}), 500


# Channel Management Routes
@bp.route('/api/channels', methods=['GET'])
@login_required
def get_channels():
    """Get all channels"""
    try:
        channels = db_manager.get_channels()
        return jsonify([{
            'id': ch.id,
            'channel_id': ch.channel_id,
            'title': ch.title,
            'type': ch.channel_type,
            'is_active': ch.is_active,
            'created_at': ch.created_at.isoformat()
        } for ch in channels])
        
    except Exception as e:
        logger.error(f"Error getting channels: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/api/channels', methods=['POST'])
@login_required
def add_channel():
    """Add new channel"""
    try:
        data = request.json
        channel_id = data.get('channel_id')
        title = data.get('title')
        channel_type = data.get('type', 'source')
        
        if not channel_id or not title:
            return jsonify({'error': 'Channel ID and title required'}), 400
        
        channel = Channel(
            channel_id=channel_id,
            title=title,
            channel_type=channel_type
        )
        
        db_manager.add_channel(channel)
        logger.info(f"Channel added: {title}")
        return jsonify({'success': True, 'channel_id': channel.id})
        
    except Exception as e:
        logger.error(f"Error adding channel: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/api/channels/<channel_id>', methods=['DELETE'])
@login_required
def delete_channel(channel_id):
    """Delete channel"""
    try:
        db_manager.delete_channel(channel_id)
        return jsonify({'success': True, 'message': 'Channel deleted'})
        
    except Exception as e:
        logger.error(f"Error deleting channel: {e}")
        return jsonify({'error': str(e)}), 500


# Post Management Routes
@bp.route('/api/posts', methods=['GET'])
@login_required
def get_posts():
    """Get all posts"""
    try:
        posts = db_manager.get_posts()
        return jsonify([{
            'id': p.id,
            'caption': p.original_caption[:100],
            'status': p.status,
            'created_at': p.created_at.isoformat(),
            'sent_at': p.sent_at.isoformat() if p.sent_at else None
        } for p in posts])
        
    except Exception as e:
        logger.error(f"Error getting posts: {e}")
        return jsonify({'error': str(e)}), 500


# Settings Routes
@bp.route('/api/settings/<key>', methods=['GET'])
@login_required
def get_setting(key):
    """Get setting value"""
    try:
        setting = db_manager.get_setting(key)
        if setting:
            return jsonify({'key': key, 'value': setting.value})
        return jsonify({'error': 'Setting not found'}), 404
        
    except Exception as e:
        logger.error(f"Error getting setting: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/api/settings/<key>', methods=['POST'])
@login_required
def set_setting(key):
    """Set setting value"""
    try:
        data = request.json
        value = data.get('value')
        
        db_manager.set_setting(key, value)
        return jsonify({'success': True, 'message': 'Setting updated'})
        
    except Exception as e:
        logger.error(f"Error setting value: {e}")
        return jsonify({'error': str(e)}), 500


# Frontend Routes
@bp.route('/', methods=['GET'])
def index():
    """Serve main page"""
    if 'user_id' not in session:
        return render_template('login.html')
    return render_template('index.html')


@bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """Serve dashboard"""
    return render_template('dashboard.html')


@bp.route('/channels', methods=['GET'])
@login_required
def channels():
    """Serve channels page"""
    return render_template('channels.html')


@bp.route('/posts', methods=['GET'])
@login_required
def posts():
    """Serve posts page"""
    return render_template('posts.html')


@bp.route('/settings', methods=['GET'])
@login_required
def settings():
    """Serve settings page"""
    return render_template('settings.html')
