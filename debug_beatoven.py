"""
Debug script to test the beatoven_ai package.
"""
import asyncio
import logging
import sys

from beatoven_ai import generate_music, logger
from beatoven_ai.beatoven_ai.config import settings


async def main():
    # Set up logging to stdout
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Print settings for debugging
    print(f"API URL: {settings.API_URL}")
    print(f"API KEY: {settings.API_KEY[:5]}...{settings.API_KEY[-4:]}")
    print(f"OUTPUT DIR: {settings.OUTPUT_DIR}")
    
    try:
        # Test music generation
        output_path = await generate_music(
            prompt="简短的钢琴旋律",
            duration=30,
            format="mp3",
            output_path="./outputs",
            filename="debug_test"
        )
        print(f"Success! Music generated at: {output_path}")
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())