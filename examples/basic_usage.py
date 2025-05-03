"""
Basic usage example for the beatoven_ai package.
"""
import asyncio
import os
from pathlib import Path

# Import directly from the package
from beatoven_ai import BeatovenClient, generate_music


async def example_direct_function():
    """Example using the convenience function."""
    print("Example 1: Using the convenience function")
    
    # Generate a music track with a text prompt
    output_path = await generate_music(
        prompt="一个优美的钢琴旋律，带有轻微的弦乐伴奏，适合深思和冥想",
        duration=120,  # 2 minutes
        format="mp3",
        output_path="./outputs",
        filename="piano_meditation"
    )
    
    print(f"Music generated at: {output_path}")
    return output_path


async def example_client_usage():
    """Example using the client directly for more control."""
    print("\nExample 2: Using the client directly")
    
    # Create a client instance
    client = BeatovenClient()
    
    # Create output directory if it doesn't exist
    output_dir = Path("./outputs")
    output_dir.mkdir(exist_ok=True)
    
    # Generate a music track
    output_path = await client.generate_music(
        prompt="一个积极向上的电子音乐，带有有力的节奏和鼓点，适合运动",
        duration=180,  # 3 minutes
        format="mp3",
        output_path=str(output_dir),
        filename="workout_beat"
    )
    
    print(f"Music generated at: {output_path}")
    return output_path


async def main():
    """Run all examples."""
    try:
        # Create output directory
        os.makedirs("./outputs", exist_ok=True)
        
        # Run examples
        await example_direct_function()
        await example_client_usage()
        
        print("\nAll examples completed successfully!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())