"""Database Models"""
from datetime import datetime
from typing import Optional, List

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Channel(Base):
    """Telegram Channel Model"""
    __tablename__ = 'channels'
    
    id = Column(Integer, primary_key=True)
    channel_id = Column(String(50), unique=True, nullable=False)
    username = Column(String(255))
    title = Column(String(255), nullable=False)
    channel_type = Column(String(20), nullable=False)  # 'source' or 'destination'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    posts = relationship('Post', back_populates='source_channel')


class Post(Base):
    """Post/Message Model"""
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    source_channel_id = Column(String(50), ForeignKey('channels.channel_id'))
    original_caption = Column(Text)
    processed_caption = Column(Text)
    media_path = Column(String(500))
    media_type = Column(String(50))  # 'photo', 'video', 'document', 'gif', 'album'
    file_id = Column(String(255))
    status = Column(String(20), default='pending')  # 'pending', 'sent', 'failed', 'archived'
    scheduled_at = Column(DateTime)
    sent_at = Column(DateTime)
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    source_channel = relationship('Channel', back_populates='posts')


class User(Base):
    """User/Admin Model"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255))
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default='user')  # 'admin', 'user', 'moderator'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Setting(Base):
    """System Settings Model"""
    __tablename__ = 'settings'
    
    id = Column(Integer, primary_key=True)
    key = Column(String(255), unique=True, nullable=False)
    value = Column(Text, nullable=False)
    value_type = Column(String(50))  # 'string', 'integer', 'boolean', 'json'
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Log(Base):
    """Operation Log Model"""
    __tablename__ = 'logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(20))  # 'success', 'error', 'warning'
    ip_address = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)
