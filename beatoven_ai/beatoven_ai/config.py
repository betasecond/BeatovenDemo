"""
Configuration module with environment variable support.
"""
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
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="BEATOVEN_",
        case_sensitive=False,
    )


# Create and export a global settings instance
settings = Settings()

# For backward compatibility, maintain these constants
BACKEND_V1_API_URL = settings.API_URL
# Use the provided API key or the one from environment variables
BACKEND_API_HEADER_KEY = settings.API_KEY or "-xBRMpR9cjzS8cwQFF53Dw"