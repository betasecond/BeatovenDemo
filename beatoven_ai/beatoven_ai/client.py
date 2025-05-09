"""
Client module for interacting with the Beatoven.ai API.
"""
import asyncio
from pathlib import Path
from typing import Any, Dict, Optional, Union

import aiofiles
import aiohttp

from .config import get_settings, settings
from .logger import logger
from .models import TaskResponse, TextPrompt, TrackRequest, TrackStatus


class BeatovenAIError(Exception):
    """Base exception for Beatoven.ai API errors."""
    pass


class BeatovenClient:
    """
    Client for interfacing with the Beatoven.ai API.
    Provides methods for generating music based on text prompts.
    """

    def __init__(self, api_key: Optional[str] = None, env_file: Optional[Union[str, Path]] = None):
        """
        Initialize the Beatoven.ai client.
        
        Args:
            api_key: Optional API key. If not provided, will use the one from settings.
            env_file: Optional path to a custom .env file. If provided, will load settings from this file.
        """
        # Load custom settings if env_file is provided, otherwise use the global settings
        self.settings = get_settings(env_file) if env_file else settings.settings
        
        # Use the provided API key or the one from settings
        self.api_key = api_key or self.settings.API_KEY
        self.api_url = self.settings.API_URL
        
        # Validate API key
        if not self.api_key:
            raise ValueError("API key is required. Set it in the .env file or pass it to the constructor.")
    
    async def compose_track(
        self, 
        session: aiohttp.ClientSession,
        request_data: Union[TrackRequest, Dict[str, Any]]
    ) -> TaskResponse:
        """
        Send a composition request to the Beatoven.ai API.
        
        Args:
            session: aiohttp client session
            request_data: Track request data
            
        Returns:
            Task response with task_id
            
        Raises:
            BeatovenAIError: If the composition request fails
        """
        logger.info(f"Sending composition request: {request_data}")
        
        # Convert to dict if it's a Pydantic model
        if isinstance(request_data, TrackRequest):
            data = request_data.model_dump()
        else:
            data = request_data
        
        try:
            async with session.post(
                f"{self.api_url}/tracks/compose",
                json=data,
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=self.settings.REQUEST_TIMEOUT
            ) as response:
                response_data = await response.json()
                
                if response.status != 200 or not response_data.get("task_id"):
                    logger.error(f"Composition failed: {response_data}")
                    raise BeatovenAIError(f"Composition failed: {response_data}")
                
                logger.info(f"Composition request successful: {response_data}")
                return TaskResponse(task_id=response_data["task_id"])
                
        except aiohttp.ClientConnectionError as e:
            logger.error(f"Connection error: {str(e)}")
            raise BeatovenAIError(f"Could not connect to Beatoven.ai: {str(e)}") from e
            
        except aiohttp.ClientError as e:
            logger.error(f"HTTP error: {str(e)}")
            raise BeatovenAIError(f"HTTP error: {str(e)}") from e
            
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise BeatovenAIError(f"Unexpected error: {str(e)}") from e

    async def get_track_status(self, session: aiohttp.ClientSession, task_id: str) -> TrackStatus:
        """
        Get the status of a track generation task.
        
        Args:
            session: aiohttp client session
            task_id: Task ID from the compose_track response
            
        Returns:
            Track status information
            
        Raises:
            BeatovenAIError: If the status request fails
        """
        logger.debug(f"Checking status for task: {task_id}")
        
        try:
            async with session.get(
                f"{self.api_url}/tasks/{task_id}",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=self.settings.REQUEST_TIMEOUT
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.debug(f"Task status: {data}")
                    return TrackStatus(**data)
                else:
                    error_text = await response.text()
                    logger.error(f"Status check failed: {error_text}")
                    raise BeatovenAIError(f"Status check failed: {error_text}")
                    
        except aiohttp.ClientConnectionError as e:
            logger.error(f"Connection error: {str(e)}")
            raise BeatovenAIError(f"Could not connect: {str(e)}") from e
            
        except aiohttp.ClientError as e:
            logger.error(f"HTTP error: {str(e)}")
            raise BeatovenAIError(f"HTTP error: {str(e)}") from e
            
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise BeatovenAIError(f"Unexpected error: {str(e)}") from e

    async def handle_track_file(
        self, 
        session: aiohttp.ClientSession,
        track_url: str, 
        output_path: Optional[str] = None,
        filename: Optional[str] = None,
        format: str = "mp3"
    ) -> str:
        """
        Download the generated track file.
        
        Args:
            session: aiohttp client session
            track_url: URL to download the track from
            output_path: Directory to save the file (defaults to current directory)
            filename: Name for the saved file (without extension)
            format: Audio format extension
            
        Returns:
            Path to the downloaded file
            
        Raises:
            BeatovenAIError: If downloading fails
        """
        # Determine output directory
        output_dir = Path(output_path or self.settings.OUTPUT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename if not provided
        if not filename:
            filename = f"composed_track_{asyncio.get_event_loop().time():.0f}"
        
        # Ensure filename has the correct extension
        if not filename.endswith(f".{format}"):
            filename = f"{filename}.{format}"
        
        # Full path for saving the file
        file_path = output_dir / filename
        
        logger.info(f"Downloading track to {file_path}")
        
        try:
            async with session.get(track_url, timeout=self.settings.DOWNLOAD_TIMEOUT) as response:
                if response.status == 200:
                    async with aiofiles.open(file_path, "wb") as f:
                        await f.write(await response.read())
                    logger.info(f"Successfully downloaded track to {file_path}")
                    return str(file_path)
                else:
                    error_text = await response.text()
                    logger.error(f"Download failed: {error_text}")
                    raise BeatovenAIError(f"Download failed: {error_text}")
                    
        except aiohttp.ClientConnectionError as e:
            logger.error(f"Connection error while downloading: {str(e)}")
            raise BeatovenAIError(f"Could not download file: {str(e)}") from e
            
        except aiohttp.ClientError as e:
            logger.error(f"HTTP error while downloading: {str(e)}")
            raise BeatovenAIError(f"HTTP error: {str(e)}") from e
            
        except Exception as e:
            logger.error(f"Unexpected error while downloading: {str(e)}")
            raise BeatovenAIError(f"Unexpected error: {str(e)}") from e

    async def watch_task_status(
        self, 
        session: aiohttp.ClientSession,
        task_id: str, 
        interval: int = None
    ) -> TrackStatus:
        """
        Poll the task status until it completes or fails.
        
        Args:
            session: aiohttp client session
            task_id: Task ID to monitor
            interval: Polling interval in seconds
            
        Returns:
            Final track status
            
        Raises:
            BeatovenAIError: If the task fails
        """
        polling_interval = interval or self.settings.POLLING_INTERVAL
        logger.info(f"Watching task {task_id} with {polling_interval}s polling interval")
        
        while True:
            track_status = await self.get_track_status(session, task_id)
            
            if track_status.status == "composing":
                logger.info(f"Task {task_id} is still composing...")
                await asyncio.sleep(polling_interval)
            elif track_status.status == "failed":
                logger.error(f"Task {task_id} has failed")
                raise BeatovenAIError("Task failed")
            else:
                logger.info(f"Task {task_id} has completed")
                return track_status

    async def generate_music(
        self,
        prompt: str,
        duration: int = None,
        format: str = None,
        output_path: Optional[str] = None,
        filename: Optional[str] = None
    ) -> str:
        """
        Generate music from a text prompt.
        
        Args:
            prompt: Text description for music generation
            duration: Duration in seconds
            format: Audio format (mp3, wav, ogg)
            output_path: Directory to save the file
            filename: Name for the saved file (without extension)
            
        Returns:
            Path to the downloaded music file
            
        Raises:
            BeatovenAIError: If any step of the generation process fails
        """
        # Use defaults from settings if not provided
        duration = duration or self.settings.DEFAULT_DURATION
        format = format or self.settings.DEFAULT_FORMAT
        
        track_request = TrackRequest(
            prompt=TextPrompt(text=prompt),
            duration=duration,
            format=format
        )
        
        logger.info(f"Generating music with prompt: {prompt}, duration: {duration}s, format: {format}")
        
        async with aiohttp.ClientSession() as session:
            try:
                # Step 1: Start composition
                compose_response = await self.compose_track(session, track_request)
                task_id = compose_response.task_id
                logger.info(f"Composition started with task ID: {task_id}")
                
                # Step 2: Wait for completion
                final_status = await self.watch_task_status(session, task_id)
                
                if final_status.meta and "track_url" in final_status.meta:
                    track_url = final_status.meta["track_url"]
                    
                    # Step 3: Download the file
                    return await self.handle_track_file(
                        session, 
                        track_url, 
                        output_path=output_path,
                        filename=filename,
                        format=format
                    )
                else:
                    raise BeatovenAIError("No track URL in the completion response")
                    
            except BeatovenAIError:
                # Let these pass through
                raise
            except Exception as e:
                logger.error(f"Unexpected error in generate_music: {str(e)}")
                raise BeatovenAIError(f"Music generation failed: {str(e)}") from e