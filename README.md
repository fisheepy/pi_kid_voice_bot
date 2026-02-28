# Pi Kid Voice Bot

这是一个用于 Raspberry Pi 的儿童语音机器人项目，目前提供可运行的 Python 包骨架与基础测试。

## 当前内容

- 基础 Python 包结构（`src/pi_kid_voice_bot`）
- 可执行入口脚本（`main.py`）
- `pyproject.toml` 打包配置（可 `pip install -e .`）
- 基础单元测试（`tests/test_main.py`）
- 依赖清单模板（`requirements.txt`）
- Python 常用忽略项（`.gitignore`）

## 快速开始

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pi-kid-voice-bot --device pi-01 --dry-run
pytest
```

## 下一步建议

1. 接入语音输入（如 `pyaudio` / `sounddevice`）。
2. 添加 STT/TTS 模块（例如 Whisper + edge-tts）。
3. 增加热词唤醒与家长控制逻辑。
4. 补充 systemd 部署脚本与硬件健康检查。
