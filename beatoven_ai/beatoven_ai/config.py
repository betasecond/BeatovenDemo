"""
Configuration module with environment variable support.
"""
from functools import lru_cache
from pathlib import Path
from typing import Optional, Union, Dict, Any
from pydantic import Field, Extra
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    """Application settings that can be loaded from environment variables."""
    
    # API configuration
    API_URL: str = Field(
        default="https://public-api.beatoven.ai/api/v1",
        description="Beatoven.ai API URL"
    )
    API_KEY: str = Field(
        default="",
        description="Beatoven.ai API key"
    )
    
    # Default music generation settings
    DEFAULT_DURATION: int = Field(
        default=180,
        description="Default music duration in seconds",
        ge=30,
        le=600
    )
    DEFAULT_FORMAT: str = Field(
        default="mp3",
        description="Default audio format (mp3, wav, ogg)"
    )
    
    # Output directory
    OUTPUT_DIR: str = Field(
        default="./",
        description="Directory to save generated music files"
    )
    
    # Timeout settings
    REQUEST_TIMEOUT: int = Field(
        default=30,
        description="API request timeout in seconds"
    )
    DOWNLOAD_TIMEOUT: int = Field(
        default=60,
        description="Download timeout in seconds"
    )
    POLLING_INTERVAL: int = Field(
        default=10,
        description="Interval in seconds between status checks"
    )
    
    # Allow extra fields so we can load from env files with additional variables
    model_config = SettingsConfigDict(
        extra="ignore",  # Allow extra fields and ignore them
    )


def find_env_file(default_name: str = ".env") -> Optional[Path]:
    """
    Find the .env file by looking in several common locations.
    
    Args:
        default_name: Default environment file name to look for
        
    Returns:
        Path to the found env file or None if not found
    """
    # Places to look for the .env file in order of preference
    search_paths = [
        # Current working directory
        Path.cwd() / default_name,
        
        # Module directory
        Path(__file__).parent / default_name,
        
        # Package root directory
        Path(__file__).parent.parent.parent / default_name,
        
        # User home directory
        Path.home() / default_name
    ]
    
    # Look for the .env file
    for path in search_paths:
        if path.exists():
            return path
    
    return None


# Cache the settings objects to avoid recreating them
@lru_cache(maxsize=32)
def get_settings(env_file: Optional[Union[str, Path]] = None) -> Settings:
    """
    Create and return a Settings instance with optional custom env file path.
    
    Args:
        env_file: Optional path to a custom .env file. Can be string or Path object.
               If None, will search for ".env" in common locations.
    
    Returns:
        Settings instance configured with the specified env file
    """
    config_dict = {
        "env_file_encoding": "utf-8",
        "env_prefix": "BEATOVEN_",
        "case_sensitive": False,
        "extra": "ignore",  # Allow extra fields in the env file
    }
    
    if env_file is not None:
        # Convert to Path if it's a string
        if isinstance(env_file, str):
            env_file = Path(env_file).resolve()
            
        # Ensure the file exists
        if env_file.exists():
            config_dict["env_file"] = str(env_file)
            # Don't print anything if the file exists - let the caller handle messaging
        else:
            print(f"Warning: Specified environment file {env_file} not found. Using default settings without any env file.")
    else:
        # Only search for .env file if no specific file was provided
        found_env_file = find_env_file()
        if found_env_file:
            config_dict["env_file"] = str(found_env_file)
            print(f"Using environment file: {found_env_file}")
    
    # Create a new Settings class with the dynamic model_config
    class DynamicSettings(Settings):
        model_config = SettingsConfigDict(**config_dict)
    
    return DynamicSettings()


# Create a lazy-loaded settings property
class LazySettings:
    """Lazy-loaded settings that only get initialized when accessed."""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._settings = None
        return cls._instance
    
    @property
    def settings(self):
        """Get or create the settings instance."""
        if self._settings is None:
            self._settings = get_settings()
        return self._settings
    
    def __getattr__(self, name):
        """Forward attribute access to the settings object."""
        return getattr(self.settings, name)


# Export a lazy-loaded global settings instance
settings = LazySettings()

# For backward compatibility, define constants as properties
def get_backend_v1_api_url():
    """Get API URL from settings lazily."""
    return settings.API_URL

def get_backend_api_header_key():
    """Get API key from settings lazily, with fallback."""
    return settings.API_KEY or "-xBRMpR9cjzS8cwQFF53Dw"

# Define properties for backward compatibility
BACKEND_V1_API_URL = property(get_backend_v1_api_url)
BACKEND_API_HEADER_KEY = property(get_backend_api_header_key)