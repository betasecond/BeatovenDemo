"""
Beatoven.ai music generation package.

This package provides simple access to the Beatoven.ai API for AI-powered music generation.
"""

from beatoven_ai.beatoven_ai.cli import main
from beatoven_ai.beatoven_ai.client import BeatovenAIError, BeatovenClient
from beatoven_ai.beatoven_ai.config import settings, get_settings
from beatoven_ai.beatoven_ai.logger import logger, setup_logger
from beatoven_ai.beatoven_ai.models import TextPrompt, TrackRequest, TrackStatus

__all__ = [
    "BeatovenClient",
    "BeatovenAIError",
    "TrackRequest",
    "TextPrompt",
    "TrackStatus",
    "settings",
    "get_settings",
    "logger",
    "setup_logger",
    "main",
    "generate_music"
]

# Convenience function for simple API access
async def generate_music(
    prompt: str,
    duration: int = None,
    format: str = None, 
    output_path: str = None,
    filename: str = None,
    api_key: str = None,
    env_file: str = None
) -> str:
    """
    Generate music from a text prompt using Beatoven.ai API.
    
    Args:
        prompt: Text description for music generation
        duration: Duration in seconds
        format: Audio format (mp3, wav, ogg)
        output_path: Directory to save the file
        filename: Name for the saved file (without extension)
        api_key: Optional API key (uses environment variable or default if not provided)
        env_file: Optional path to a custom .env file
        
    Returns:
        Path to the downloaded music file
    """
    client = BeatovenClient(api_key=api_key, env_file=env_file)
    return await client.generate_music(
        prompt=prompt,
        duration=duration,
        format=format,
        output_path=output_path,
        filename=filename
    )