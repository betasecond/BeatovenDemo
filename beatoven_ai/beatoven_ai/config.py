"""
Configuration module with environment variable support.
"""
from pathlib import Path
from typing import Optional, Union
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


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
    
    # The model_config will be set based on the env_file parameter when creating the instance


def get_settings(env_file: Optional[Union[str, Path]] = None) -> Settings:
    """
    Create and return a Settings instance with optional custom env file path.
    
    Args:
        env_file: Optional path to a custom .env file. Can be string or Path object.
               If None, defaults to looking for ".env" in the current directory.
    
    Returns:
        Settings instance configured with the specified env file
    """
    config_dict = {
        "env_file_encoding": "utf-8",
        "env_prefix": "BEATOVEN_",
        "case_sensitive": False,
    }
    
    if env_file is not None:
        # Convert to Path if it's a string
        if isinstance(env_file, str):
            env_file = Path(env_file)
            
        # Ensure the file exists
        if not env_file.exists():
            print(f"Warning: Environment file {env_file} not found. Using default settings.")
        
        config_dict["env_file"] = str(env_file)
    else:
        config_dict["env_file"] = ".env"
    
    # Create a new Settings class with the dynamic model_config
    class DynamicSettings(Settings):
        model_config = SettingsConfigDict(**config_dict)
    
    return DynamicSettings()


# Create and export a global settings instance with default env file location
settings = get_settings()

# For backward compatibility, maintain these constants
BACKEND_V1_API_URL = settings.API_URL
# Use the provided API key or the one from environment variables
BACKEND_API_HEADER_KEY = settings.API_KEY or "-xBRMpR9cjzS8cwQFF53Dw"