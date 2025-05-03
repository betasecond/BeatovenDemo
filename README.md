# Beatoven AI Music Generator

一个用于通过文字描述生成AI音乐的Python包，基于Beatoven.ai API。

## 功能特点

- ✨ 通过文字描述生成高质量音乐
- 🚀 异步API，高效处理请求
- 📦 完整的Python包结构
- 🔧 灵活的配置选项，支持.env环境变量
- 📝 详细的日志记录
- 🔄 支持多种音频格式（mp3、wav、ogg）
- 🧩 提供简单易用的函数和完整客户端API
- 🧪 包含全面的测试用例

## 安装

### 使用pip

```bash
pip install beatoven-ai
```

### 使用uv

```bash
uv install beatoven-ai
```

### 从源码安装

```bash
git clone https://github.com/yourusername/beatoven-ai.git
cd beatoven-ai
pip install -e .
```

## 快速开始

### 环境变量配置

创建`.env`文件设置API密钥和其他配置（参考`.env.example`）：

```bash
BEATOVEN_API_KEY=your_api_key_here
```

### 命令行使用

```bash
# 使用默认设置生成音乐
beatoven --prompt "一个平静的钢琴曲，带有轻微的弦乐伴奏"

# 指定时长和格式
beatoven --prompt "活力四射的电子舞曲" --duration 240 --format wav

# 指定输出目录和文件名
beatoven --prompt "深沉的古典音乐" --output ./my_music --filename my_classical_piece
```

### Python代码中使用

```python
import asyncio
from beatoven_ai import generate_music

async def main():
    # 简单的函数调用
    output_path = await generate_music(
        prompt="一个放松的环境音乐，带有自然声音",
        duration=180,  # 秒
        format="mp3",
        output_path="./outputs",
        filename="relaxing_ambient"
    )
    print(f"音乐已生成: {output_path}")

if __name__ == "__main__":
    asyncio.run(main())
```

### 使用完整的客户端API

```python
import asyncio
from beatoven_ai import BeatovenClient

async def main():
    # 创建客户端实例
    client = BeatovenClient(api_key="your_api_key")
    
    # 生成音乐
    output_path = await client.generate_music(
        prompt="一首激励人心的配乐，适合视频背景",
        duration=300,
        format="mp3"
    )
    
    print(f"音乐已生成: {output_path}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 高级用法

### 使用Pydantic模型

```python
import asyncio
import aiohttp
from beatoven_ai import BeatovenClient, TrackRequest, TextPrompt

async def main():
    client = BeatovenClient()
    
    # 使用Pydantic模型构建请求
    request = TrackRequest(
        prompt=TextPrompt(text="一首轻松愉快的流行歌曲风格音乐"),
        duration=240,
        format="mp3"
    )
    
    async with aiohttp.ClientSession() as session:
        # 开始生成任务
        response = await client.compose_track(session, request)
        task_id = response.task_id
        
        # 等待任务完成
        final_status = await client.watch_task_status(session, task_id)
        
        # 下载生成的音乐
        if final_status.status == "completed":
            track_url = final_status.meta["track_url"]
            file_path = await client.handle_track_file(
                session, track_url, output_path="./outputs"
            )
            print(f"音乐已生成: {file_path}")

if __name__ == "__main__":
    asyncio.run(main())
```

### 自定义日志配置

```python
from beatoven_ai import setup_logger, generate_music
import logging
import asyncio

# 配置详细的日志记录
logger = setup_logger(
    name="my_music_app",
    log_level=logging.DEBUG,
    log_file="music_generation.log"
)

async def main():
    try:
        output_path = await generate_music("一首舒缓的古典音乐")
        logger.info(f"成功生成音乐: {output_path}")
    except Exception as e:
        logger.error(f"生成失败: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
```

## API参考

### 主要函数和类

- `generate_music(prompt, duration=None, format=None, output_path=None, filename=None, api_key=None)` - 生成音乐的便捷函数
- `BeatovenClient` - 与Beatoven.ai API交互的客户端类
- `TrackRequest`, `TextPrompt`, `TrackStatus` - 数据模型
- `setup_logger` - 配置日志记录

## 环境变量配置

支持通过`.env`文件或系统环境变量进行配置：

| 环境变量 | 描述 | 默认值 |
|----------|------|--------|
| `BEATOVEN_API_KEY` | Beatoven.ai API密钥 | - |
| `BEATOVEN_API_URL` | API端点URL | https://public-api.beatoven.ai/api/v1 |
| `BEATOVEN_DEFAULT_DURATION` | 默认音乐时长（秒） | 180 |
| `BEATOVEN_DEFAULT_FORMAT` | 默认音频格式 | mp3 |
| `BEATOVEN_OUTPUT_DIR` | 默认输出目录 | ./ |

## 开发

### 安装开发依赖

```bash
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest
```

### 代码检查

使用ruff进行代码检查：

```bash
ruff check .
```

### 代码格式化

```bash
ruff format .
```

## 贡献

欢迎提交Pull Request和Issue。

## 许可证

MIT License