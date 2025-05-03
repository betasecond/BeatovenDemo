"""
Beatoven.ai music generation package core modules.
"""

from .client import BeatovenAIError, BeatovenClient
from .config import settings
from .logger import logger, setup_logger
from .models import TextPrompt, TrackRequest, TrackStatus

__all__ = [
    "BeatovenClient", 
    "BeatovenAIError",
    "TrackRequest", 
    "TextPrompt", 
    "TrackStatus",
    "settings",
    "logger", 
    "setup_logger"
]