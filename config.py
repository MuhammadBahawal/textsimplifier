"""
Configuration and API key management for Phrase Simplifier.
"""
import os
import json
from pathlib import Path

# Application Info
APP_NAME = "Phrase Simplifier"
APP_VERSION = "1.0.0"
APP_AUTHOR = "AI Assistant"

# Paths
APP_DATA_DIR = Path(os.getenv('APPDATA', '')) / 'PhraseSimplifier'
CONFIG_FILE = APP_DATA_DIR / 'config.json'

# Default API Key (user provided)
DEFAULT_API_KEY = "AIzaSyCNsqinz7wTQ_wgUTrFG-qJsgmnxYtT5w0"

# Default settings
DEFAULT_CONFIG = {
    'theme': 'dark',
    'gemini_api_key': DEFAULT_API_KEY,
    'font_size': 14,
    'auto_switch_mode': True
}

def ensure_app_data_dir():
    """Create app data directory if it doesn't exist."""
    APP_DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_config() -> dict:
    """Load configuration from file."""
    ensure_app_data_dir()
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Merge with defaults for any missing keys
                return {**DEFAULT_CONFIG, **config}
        except (json.JSONDecodeError, IOError):
            pass
    return DEFAULT_CONFIG.copy()

def save_config(config: dict):
    """Save configuration to file."""
    ensure_app_data_dir()
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

def get_api_key() -> str:
    """
    Get the Gemini API key.
    Priority:
    1. Environment variable GEMINI_API_KEY
    2. Saved in config file
    3. Default built-in key
    """
    # Check environment variable first
    env_key = os.getenv('GEMINI_API_KEY', '')
    if env_key:
        return env_key
    
    # Check config file
    config = load_config()
    key = config.get('gemini_api_key', '')
    if key:
        return key
    
    # Use default key
    return DEFAULT_API_KEY

def set_api_key(api_key: str):
    """Save API key to config file."""
    config = load_config()
    config['gemini_api_key'] = api_key
    save_config(config)

def get_theme() -> str:
    """Get current theme setting."""
    config = load_config()
    return config.get('theme', 'dark')

def set_theme(theme: str):
    """Save theme preference."""
    config = load_config()
    config['theme'] = theme
    save_config(config)
