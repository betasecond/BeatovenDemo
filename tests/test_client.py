"""
Tests for the BeatovenClient.
"""
import os
from unittest.mock import patch, MagicMock, AsyncMock

import pytest

from beatoven_ai.beatoven_ai.client import BeatovenClient, BeatovenAIError
from beatoven_ai.beatoven_ai.models import TrackRequest, TextPrompt


@pytest.fixture
def client():
    """Client fixture."""
    return BeatovenClient(api_key="test_api_key")


@pytest.fixture
def mock_response():
    """Mock response fixture."""
    mock = MagicMock()
    mock.status = 200
    mock.json = AsyncMock(return_value={"task_id": "test_task_id"})
    mock.text = AsyncMock(return_value="Error text")
    mock.read = AsyncMock(return_value=b"file content")
    return mock


@pytest.mark.asyncio
async def test_compose_track_success(client):
    """Test successful track composition."""
    # Create mock response
    response_mock = MagicMock()
    response_mock.status = 200
    response_mock.json = AsyncMock(return_value={"task_id": "test_task_id"})
    
    # Create mock context manager
    cm_mock = MagicMock()
    cm_mock.__aenter__ = AsyncMock(return_value=response_mock)
    cm_mock.__aexit__ = AsyncMock(return_value=None)
    
    # Create mock session
    session_mock = MagicMock()
    session_mock.post = AsyncMock(return_value=cm_mock)
    
    # Test the compose_track method
    response = await client.compose_track(
        session_mock,
        TrackRequest(prompt=TextPrompt(text="Test prompt"))
    )
    
    # Verify the response
    assert response.task_id == "test_task_id"
    session_mock.post.assert_called_once()


@pytest.mark.asyncio
async def test_compose_track_error(client):
    """Test error during track composition."""
    # Create mock response with error
    response_mock = MagicMock()
    response_mock.status = 400
    response_mock.json = AsyncMock(return_value={"error": "Bad request"})
    
    # Create mock context manager
    cm_mock = MagicMock()
    cm_mock.__aenter__ = AsyncMock(return_value=response_mock)
    cm_mock.__aexit__ = AsyncMock(return_value=None)
    
    # Create mock session
    session_mock = MagicMock()
    session_mock.post = AsyncMock(return_value=cm_mock)
    
    # Test error handling
    with pytest.raises(BeatovenAIError):
        await client.compose_track(
            session_mock,
            TrackRequest(prompt=TextPrompt(text="Test prompt"))
        )


@pytest.mark.asyncio
async def test_get_track_status_success(client):
    """Test successful track status retrieval."""
    # Create mock response
    response_mock = MagicMock()
    response_mock.status = 200
    response_mock.json = AsyncMock(
        return_value={"status": "completed", "meta": {"track_url": "https://example.com/track.mp3"}}
    )
    
    # Create mock context manager
    cm_mock = MagicMock()
    cm_mock.__aenter__ = AsyncMock(return_value=response_mock)
    cm_mock.__aexit__ = AsyncMock(return_value=None)
    
    # Create mock session
    session_mock = MagicMock()
    session_mock.get = AsyncMock(return_value=cm_mock)
    
    status = await client.get_track_status(session_mock, "test_task_id")
    
    # Verify the response
    assert status.status == "completed"
    assert status.meta["track_url"] == "https://example.com/track.mp3"
    session_mock.get.assert_called_once()


@pytest.mark.asyncio
async def test_get_track_status_error(client):
    """Test error during track status retrieval."""
    # Create mock response with error
    response_mock = MagicMock()
    response_mock.status = 404
    response_mock.text = AsyncMock(return_value="Not found")
    
    # Create mock context manager
    cm_mock = MagicMock()
    cm_mock.__aenter__ = AsyncMock(return_value=response_mock)
    cm_mock.__aexit__ = AsyncMock(return_value=None)
    
    # Create mock session
    session_mock = MagicMock()
    session_mock.get = AsyncMock(return_value=cm_mock)
    
    with pytest.raises(BeatovenAIError):
        await client.get_track_status(session_mock, "test_task_id")


@pytest.mark.asyncio
async def test_handle_track_file_success(client, tmp_path):
    """Test successful track file download."""
    # Create mock response
    response_mock = MagicMock()
    response_mock.status = 200
    response_mock.read = AsyncMock(return_value=b"file content")
    
    # Create mock context manager for http response
    cm_mock = MagicMock()
    cm_mock.__aenter__ = AsyncMock(return_value=response_mock)
    cm_mock.__aexit__ = AsyncMock(return_value=None)
    
    # Create mock session
    session_mock = MagicMock()
    session_mock.get = AsyncMock(return_value=cm_mock)
    
    # Create mock file context manager
    file_mock = MagicMock()
    file_mock.__aenter__ = AsyncMock()
    file_mock.__aexit__ = AsyncMock()
    file_mock.__aenter__.return_value.write = AsyncMock()
    
    # Test the handle_track_file method
    with patch("aiofiles.open", return_value=file_mock):
        file_path = await client.handle_track_file(
            session_mock,
            "https://example.com/track.mp3",
            output_path=str(tmp_path),
            filename="test_track",
            format="mp3"
        )
    
    # Verify results
    assert "test_track.mp3" in file_path
    assert str(tmp_path) in file_path
    file_mock.__aenter__.return_value.write.assert_called_once_with(b"file content")


@pytest.mark.asyncio
async def test_generate_music_integration(client):
    """
    Test the full music generation flow with mocked responses.
    """
    # Mock all the client methods
    client.compose_track = AsyncMock(return_value=MagicMock(task_id="test_task_id"))
    client.watch_task_status = AsyncMock(
        return_value=MagicMock(
            status="completed",
            meta={"track_url": "https://example.com/track.mp3"}
        )
    )
    client.handle_track_file = AsyncMock(return_value="/path/to/downloaded/file.mp3")
    
    # Create a mock session context manager
    mock_session = MagicMock()
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)
    
    with patch("aiohttp.ClientSession", return_value=mock_session):
        result = await client.generate_music(
            prompt="Test prompt",
            duration=180,
            format="mp3"
        )
    
    # Verify the result
    assert result == "/path/to/downloaded/file.mp3"
    
    # Verify the method calls
    client.compose_track.assert_called_once()
    client.watch_task_status.assert_called_once_with(mock_session, "test_task_id")
    client.handle_track_file.assert_called_once_with(
        mock_session, 
        "https://example.com/track.mp3", 
        output_path=None,
        filename=None,
        format="mp3"
    )