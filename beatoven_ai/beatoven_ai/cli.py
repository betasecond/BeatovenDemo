"""
Command-line interface for beatoven_ai.
"""
import argparse
import asyncio
import sys
from typing import List, Optional

from .client import BeatovenAIError, BeatovenClient
from .config import settings
from .logger import logger, setup_logger


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Args:
        args: Command line arguments (uses sys.argv if not provided)
        
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description='Beatoven.ai Music Generator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        '--prompt',
        type=str,
        default="我需要一个环境、平静和冥想的轨道，带有柔软的合成器垫和慢速的瑜伽",
        help='音乐描述文本'
    )
    
    parser.add_argument(
        '--duration',
        type=int,
        default=settings.DEFAULT_DURATION,
        help='音乐时长（秒）'
    )
    
    parser.add_argument(
        '--format',
        type=str,
        default=settings.DEFAULT_FORMAT,
        choices=["mp3", "wav", "ogg"],
        help='音频格式'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=settings.OUTPUT_DIR,
        help='输出文件目录'
    )
    
    parser.add_argument(
        '--filename',
        type=str,
        default=None,
        help='输出文件名（不含扩展名）'
    )
    
    parser.add_argument(
        '--api-key',
        type=str,
        default=None,
        help='Beatoven.ai API 密钥（默认使用环境变量或内置密钥）'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='启用详细日志记录'
    )
    
    parser.add_argument(
        '--log-file',
        type=str,
        default=None,
        help='日志文件路径'
    )
    
    return parser.parse_args(args)


async def main_async(args: argparse.Namespace) -> int:
    """
    Main async entry point.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    # Configure logger based on verbosity
    log_level = 10 if args.verbose else 20  # DEBUG if verbose, else INFO
    setup_logger(
        log_level=log_level,
        log_file=args.log_file
    )
    
    try:
        # Create client with API key from args or config
        client = BeatovenClient(api_key=args.api_key)
        
        # Generate music
        logger.info(f"Generating music with prompt: {args.prompt}")
        output_path = await client.generate_music(
            prompt=args.prompt,
            duration=args.duration,
            format=args.format,
            output_path=args.output,
            filename=args.filename
        )
        
        logger.info(f"Music generated successfully! File saved to: {output_path}")
        print(f"\n✅ 音乐已生成: {output_path}")
        return 0
        
    except BeatovenAIError as e:
        logger.error(f"Failed to generate music: {str(e)}")
        print(f"\n❌ 生成失败: {str(e)}")
        return 1
        
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        print("\n🛑 已取消")
        return 130
        
    except Exception as e:
        logger.exception("Unexpected error occurred")
        print(f"\n❌ 发生错误: {str(e)}")
        return 1


def main(args: Optional[List[str]] = None) -> int:
    """
    Command-line entry point.
    
    Args:
        args: Command-line arguments
        
    Returns:
        Exit code
    """
    parsed_args = parse_args(args)
    return asyncio.run(main_async(parsed_args))


if __name__ == "__main__":
    sys.exit(main())