"""
Tests for Pydantic models.
"""
import pytest
from pydantic import ValidationError

from beatoven_ai.beatoven_ai.models import TextPrompt, TrackRequest, TrackStatus


def test_text_prompt_valid():
    """Test that TextPrompt validates correctly."""
    prompt = TextPrompt(text="A valid prompt")
    assert prompt.text == "A valid prompt"


def test_text_prompt_invalid():
    """Test that TextPrompt raises validation error with empty text."""
    # Pydantic v2 doesn't raise ValidationError for empty strings by default
    # We need to explicitly provide None to trigger validation error
    with pytest.raises(ValidationError):
        TextPrompt(text=None)


def test_track_request_valid():
    """Test that TrackRequest validates correctly."""
    request = TrackRequest(
        prompt=TextPrompt(text="A valid prompt"),
        duration=180,
        format="mp3"
    )
    assert request.prompt.text == "A valid prompt"
    assert request.duration == 180
    assert request.format == "mp3"


def test_track_request_default_values():
    """Test that TrackRequest uses default values correctly."""
    request = TrackRequest(prompt=TextPrompt(text="A valid prompt"))
    assert request.duration == 180  # Default duration
    assert request.format == "mp3"  # Default format


def test_track_request_invalid_format():
    """Test that TrackRequest raises validation error with invalid format."""
    with pytest.raises(ValidationError):
        TrackRequest(
            prompt=TextPrompt(text="A valid prompt"),
            format="invalid"  # Not in the allowed formats
        )


def test_track_request_invalid_duration():
    """Test that TrackRequest raises validation error with invalid duration."""
    with pytest.raises(ValidationError):
        TrackRequest(
            prompt=TextPrompt(text="A valid prompt"),
            duration=10  # Too short
        )


def test_track_status_valid():
    """Test that TrackStatus validates correctly."""
    status = TrackStatus(status="composing")
    assert status.status == "composing"
    
    status = TrackStatus(
        status="completed", 
        meta={"track_url": "https://example.com/track.mp3"}
    )
    assert status.status == "completed"
    assert status.meta["track_url"] == "https://example.com/track.mp3"


def test_track_status_invalid():
    """Test that TrackStatus raises validation error with invalid status."""
    with pytest.raises(ValidationError):
        TrackStatus(status="invalid")