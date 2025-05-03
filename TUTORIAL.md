# Beatoven AI 使用教程

本教程将指导您如何使用 Beatoven AI 音乐生成器包生成 AI 音乐。

## 安装

### 使用虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

# 安装包
pip install -e .
```

### 使用 uv（更快）

```bash
uv venv .venv
.venv\Scripts\activate
uv pip install -e .
```

## 配置

创建 `.env` 文件在项目根目录下，填写以下内容：

```bash
# API Configuration
BEATOVEN_API_KEY=-xBRMpR9cjzS8cwQFF53Dw
BEATOVEN_API_URL=https://public-api.beatoven.ai/api/v1

# 可选设置
# BEATOVEN_DEFAULT_DURATION=180
# BEATOVEN_DEFAULT_FORMAT=mp3
# BEATOVEN_OUTPUT_DIR=./outputs
```

## 基本使用方法

### 命令行使用

最简单的使用方式是通过命令行：

```bash
# 使用默认设置生成音乐
beatoven --prompt "一个平静的钢琴曲，带有轻微的弦乐伴奏"

# 指定时长和格式
beatoven --prompt "活力四射的电子舞曲" --duration 240 --format wav

# 指定输出目录和文件名
beatoven --prompt "深沉的古典音乐" --output ./my_music --filename my_classical_piece

# 显示详细日志
beatoven --prompt "轻松的爵士乐" --verbose

# 保存日志到文件
beatoven --prompt "欢快的流行风格" --log-file music_generation.log
```

### 在 Python 代码中使用

#### 简单用法

```python
import asyncio
from beatoven_ai import generate_music

async def main():
    output_file = await generate_music(
        prompt="一个放松的环境音乐，带有自然声音",
        duration=180,  # 秒
        format="mp3",
        output_path="./outputs",
        filename="relaxing_ambient"
    )
    print(f"音乐已生成: {output_file}")

if __name__ == "__main__":
    asyncio.run(main())
```

#### 高级用法

```python
import asyncio
from beatoven_ai import BeatovenClient, logger
import logging

# 设置详细日志记录
logger.setLevel(logging.DEBUG)

async def main():
    # 创建客户端实例（可以提供自己的API密钥）
    client = BeatovenClient(api_key="your_api_key_here")
    
    # 生成音乐
    output_file = await client.generate_music(
        prompt="一首激励人心的配乐，适合视频背景",
        duration=300,
        format="mp3",
        output_path="./custom_outputs",
        filename="inspirational_track"
    )
    
    print(f"音乐已生成: {output_file}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 批量生成多首音乐

```python
import asyncio
from beatoven_ai import BeatovenClient

async def generate_multiple_tracks(prompts, output_dir="./outputs"):
    client = BeatovenClient()
    results = []
    
    for i, prompt in enumerate(prompts):
        filename = f"track_{i+1}"
        print(f"生成音乐 {i+1}/{len(prompts)}: {prompt[:30]}...")
        
        output_file = await client.generate_music(
            prompt=prompt,
            output_path=output_dir,
            filename=filename
        )
        
        results.append(output_file)
        print(f"✅ 已完成: {output_file}")
    
    return results

async def main():
    # 准备一组音乐提示
    prompts = [
        "一个优美的钢琴旋律，带有轻微的弦乐伴奏，适合深思和冥想",
        "一个积极向上的电子音乐，带有有力的节奏和鼓点，适合运动",
        "一首轻松愉快的流行歌曲风格音乐",
    ]
    
    # 批量生成音乐
    output_files = await generate_multiple_tracks(prompts)
    
    print("\n所有音乐已生成:")
    for file in output_files:
        print(f"- {file}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 故障排除

### 常见问题

1. **API密钥错误**：确保您在 `.env` 文件中设置了正确的 API 密钥。

2. **连接超时**：如果网络连接不稳定，可以在 `.env` 文件中增加超时时间：
   ```
   BEATOVEN_REQUEST_TIMEOUT=60
   BEATOVEN_DOWNLOAD_TIMEOUT=120
   ```

3. **音乐生成失败**：尝试使用 `--verbose` 参数查看详细日志，以便排查问题。

4. **输出目录不存在**：系统会自动创建输出目录，如果无法创建请检查权限。

### 获取帮助

如果您遇到任何问题，请查阅以下资源：

- 查看 README.md 文件获取更多信息
- 查看 MIGRATION_GUIDE.md 了解从旧版脚本迁移的指南
- 检查 examples 目录中的示例代码

## 高级功能

### 自定义日志配置

```python
from beatoven_ai import setup_logger
import logging

# 创建自定义日志记录器
logger = setup_logger(
    name="my_music_app",
    log_level=logging.DEBUG,
    log_file="music_generation.log"
)

# 使用自定义日志记录器
logger.info("开始生成音乐...")
```

### 使用原始API

如果需要直接访问底层API，可以使用客户端类的低级方法：

```python
import asyncio
import aiohttp
from beatoven_ai import BeatovenClient, TextPrompt, TrackRequest

async def use_raw_api():
    client = BeatovenClient()
    
    async with aiohttp.ClientSession() as session:
        # 1. 创建请求
        request = TrackRequest(
            prompt=TextPrompt(text="钢琴与弦乐的和谐旋律"),
            duration=240,
            format="mp3"
        )
        
        # 2. 发送作曲请求
        response = await client.compose_track(session, request)
        task_id = response.task_id
        print(f"作曲任务创建成功，ID: {task_id}")
        
        # 3. 监控状态
        final_status = await client.watch_task_status(session, task_id)
        print(f"状态: {final_status.status}")
        
        # 4. 下载文件
        if final_status.status == "completed":
            track_url = final_status.meta["track_url"]
            file_path = await client.handle_track_file(
                session, track_url, output_path="./outputs"
            )
            print(f"音乐已下载: {file_path}")

if __name__ == "__main__":
    asyncio.run(use_raw_api())
```