"""Database Manager"""
import json
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker, Session

from .models import Base, Channel, Post, User, Setting, Log
from utils.logger import setup_logger

logger = setup_logger(__name__)


class DatabaseManager:
    """Manages database operations"""

    def __init__(self, config: Dict[str, Any]):
        """Initialize database
        
        Args:
            config: Database configuration dict
        """
        db_type = config.get('type', 'sqlite')
        
        if db_type == 'sqlite':
            db_path = config.get('path', 'data/mediaauto.db')
            connection_string = f'sqlite:///{db_path}'
        elif db_type == 'postgresql':
            user = config.get('user', 'postgres')
            password = config.get('password', '')
            host = config.get('host', 'localhost')
            port = config.get('port', 5432)
            dbname = config.get('dbname', 'mediaauto')
            connection_string = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
        
        self.engine = create_engine(connection_string, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        
        # Create tables
        Base.metadata.create_all(self.engine)
        logger.info(f"Database initialized: {db_type}")

    def get_session(self) -> Session:
        """Get a database session
        
        Returns:
            SQLAlchemy Session
        """
        return self.Session()

    # Channel operations
    def add_channel(self, channel: Channel) -> Channel:
        """Add a new channel
        
        Args:
            channel: Channel object
            
        Returns:
            Added channel object
        """
        session = self.get_session()
        try:
            session.add(channel)
            session.commit()
            logger.info(f"Channel added: {channel.title}")
            return channel
        except Exception as e:
            session.rollback()
            logger.error(f"Error adding channel: {e}")
            raise
        finally:
            session.close()

    def get_channels(self, channel_type: Optional[str] = None, is_active: bool = True) -> List[Channel]:
        """Get channels
        
        Args:
            channel_type: 'source' or 'destination'
            is_active: Filter by active status
            
        Returns:
            List of Channel objects
        """
        session = self.get_session()
        try:
            query = session.query(Channel)
            if channel_type:
                query = query.filter_by(channel_type=channel_type)
            if is_active:
                query = query.filter_by(is_active=True)
            return query.all()
        finally:
            session.close()

    def get_channel(self, channel_id: str) -> Optional[Channel]:
        """Get a specific channel
        
        Args:
            channel_id: Telegram channel ID
            
        Returns:
            Channel object or None
        """
        session = self.get_session()
        try:
            return session.query(Channel).filter_by(channel_id=channel_id).first()
        finally:
            session.close()

    def delete_channel(self, channel_id: str) -> bool:
        """Delete a channel
        
        Args:
            channel_id: Telegram channel ID
            
        Returns:
            True if deleted
        """
        session = self.get_session()
        try:
            channel = session.query(Channel).filter_by(channel_id=channel_id).first()
            if channel:
                session.delete(channel)
                session.commit()
                logger.info(f"Channel deleted: {channel_id}")
                return True
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting channel: {e}")
            raise
        finally:
            session.close()

    # Post operations
    def add_post(self, post: Post) -> Post:
        """Add a new post
        
        Args:
            post: Post object
            
        Returns:
            Added post object
        """
        session = self.get_session()
        try:
            session.add(post)
            session.commit()
            logger.info(f"Post added: {post.id}")
            return post
        except Exception as e:
            session.rollback()
            logger.error(f"Error adding post: {e}")
            raise
        finally:
            session.close()

    def get_posts(self, status: Optional[str] = None, limit: int = 100) -> List[Post]:
        """Get posts
        
        Args:
            status: Filter by status
            limit: Maximum number of posts
            
        Returns:
            List of Post objects
        """
        session = self.get_session()
        try:
            query = session.query(Post)
            if status:
                query = query.filter_by(status=status)
            return query.order_by(Post.created_at.desc()).limit(limit).all()
        finally:
            session.close()

    def get_post(self, post_id: int) -> Optional[Post]:
        """Get a specific post
        
        Args:
            post_id: Post ID
            
        Returns:
            Post object or None
        """
        session = self.get_session()
        try:
            return session.query(Post).filter_by(id=post_id).first()
        finally:
            session.close()

    def update_post(self, post: Post) -> Post:
        """Update a post
        
        Args:
            post: Post object
            
        Returns:
            Updated post object
        """
        session = self.get_session()
        try:
            session.merge(post)
            session.commit()
            logger.info(f"Post updated: {post.id}")
            return post
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating post: {e}")
            raise
        finally:
            session.close()

    def is_duplicate(self, caption: str, days: int = 30) -> bool:
        """Check if caption is duplicate
        
        Args:
            caption: Caption text
            days: Check within last N days
            
        Returns:
            True if duplicate exists
        """
        session = self.get_session()
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            exists = session.query(Post).filter(
                and_(
                    Post.original_caption == caption,
                    Post.created_at > cutoff_date,
                    Post.status != 'failed'
                )
            ).first()
            return exists is not None
        finally:
            session.close()

    # User operations
    def add_user(self, user: User) -> User:
        """Add a new user
        
        Args:
            user: User object
            
        Returns:
            Added user object
        """
        session = self.get_session()
        try:
            session.add(user)
            session.commit()
            logger.info(f"User added: {user.username}")
            return user
        except Exception as e:
            session.rollback()
            logger.error(f"Error adding user: {e}")
            raise
        finally:
            session.close()

    def get_user(self, username: str) -> Optional[User]:
        """Get a user
        
        Args:
            username: Username
            
        Returns:
            User object or None
        """
        session = self.get_session()
        try:
            return session.query(User).filter_by(username=username).first()
        finally:
            session.close()

    def get_users(self) -> List[User]:
        """Get all users
        
        Returns:
            List of User objects
        """
        session = self.get_session()
        try:
            return session.query(User).all()
        finally:
            session.close()

    # Settings operations
    def get_setting(self, key: str) -> Optional[Setting]:
        """Get a setting
        
        Args:
            key: Setting key
            
        Returns:
            Setting object or None
        """
        session = self.get_session()
        try:
            return session.query(Setting).filter_by(key=key).first()
        finally:
            session.close()

    def set_setting(self, key: str, value: str, value_type: str = 'string') -> Setting:
        """Set a setting
        
        Args:
            key: Setting key
            value: Setting value
            value_type: Type of value
            
        Returns:
            Setting object
        """
        session = self.get_session()
        try:
            setting = session.query(Setting).filter_by(key=key).first()
            if setting:
                setting.value = value
                setting.value_type = value_type
            else:
                setting = Setting(key=key, value=value, value_type=value_type)
                session.add(setting)
            session.commit()
            logger.info(f"Setting updated: {key}")
            return setting
        except Exception as e:
            session.rollback()
            logger.error(f"Error setting value: {e}")
            raise
        finally:
            session.close()
