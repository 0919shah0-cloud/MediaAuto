"""Configuration Management"""
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

from utils.logger import setup_logger

logger = setup_logger(__name__)


class Config:
    """Manages application configuration"""

    def __init__(self, config_path: str = "config.json"):
        """Initialize configuration
        
        Args:
            config_path: Path to config file
        """
        self.config_path = Path(config_path)
        self.data = self._load_config()
        logger.info(f"Configuration loaded from {config_path}")

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file
        
        Returns:
            Configuration dictionary
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_config(self) -> None:
        """Save configuration to file"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        logger.info(f"Configuration saved to {self.config_path}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value
        
        Args:
            key: Configuration key (supports dot notation)
            default: Default value
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value if value is not None else default

    def set(self, key: str, value: Any) -> None:
        """Set configuration value
        
        Args:
            key: Configuration key (supports dot notation)
            value: Configuration value
        """
        keys = key.split('.')
        target = self.data
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        target[keys[-1]] = value

    # Convenient property accessors
    @property
    def bot(self) -> Dict[str, Any]:
        return self.data.get('bot', {})
    
    @property
    def database(self) -> Dict[str, Any]:
        return self.data.get('database', {})
    
    @property
    def panel(self) -> Dict[str, Any]:
        return self.data.get('panel', {})
    
    @property
    def api(self) -> Dict[str, Any]:
        return self.data.get('api', {})
    
    @property
    def channels(self) -> Dict[str, Any]:
        return self.data.get('channels', {})
    
    @property
    def scheduler(self) -> Dict[str, Any]:
        return self.data.get('scheduler', {})
    
    @property
    def ai(self) -> Dict[str, Any]:
        return self.data.get('ai', {})
    
    @property
    def download(self) -> Dict[str, Any]:
        return self.data.get('download', {})
    
    @property
    def processing(self) -> Dict[str, Any]:
        return self.data.get('processing', {})
    
    @property
    def duplicate_check(self) -> Dict[str, Any]:
        return self.data.get('duplicate_check', {})
    
    @property
    def logging_config(self) -> Dict[str, Any]:
        return self.data.get('logging', {})
