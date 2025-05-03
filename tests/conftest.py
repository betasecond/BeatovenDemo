"""
Common pytest fixtures for testing.
"""
from unittest.mock import AsyncMock, MagicMock

import aiohttp
import pytest
from dotenv import load_dotenv

from beatoven_ai.beatoven_ai.client import BeatovenClient

# Load environment variables for testing
load_dotenv()


@pytest.fixture
def api_key():
    """Provide a test API key."""
    return "test_api_key"


@pytest.fixture
def client(api_key):
    """Create a client instance with a test API key."""
    return BeatovenClient(api_key=api_key)


@pytest.fixture
def mock_session():
    """Mock aiohttp ClientSession."""
    session = MagicMock(spec=aiohttp.ClientSession)
    session.__aenter__ = AsyncMock(return_value=session)
    session.__aexit__ = AsyncMock(return_value=None)
    return session


@pytest.fixture
def mock_response():
    """Create a mock response object."""
    response = MagicMock()
    response.status = 200
    response.json = AsyncMock(return_value={})
    response.text = AsyncMock(return_value="")
    response.read = AsyncMock(return_value=b"")
    return response