# Pi Kid Voice Bot

这是一个用于 Raspberry Pi 的儿童语音机器人项目，目前提供可运行的 Python 包骨架与基础测试。

## 当前内容

- 基础 Python 包结构（`src/pi_kid_voice_bot`）
- 可执行入口脚本（`main.py`）
- `pyproject.toml` 打包配置（可 `pip install -e .`）
- 基础单元测试（`tests/test_main.py`）
- `systemd` 服务模板（`deploy/systemd/pi-kid-voice-bot.service`）
- 一键安装 service 脚本（`scripts/install_systemd_service.sh`）
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

## 在 Raspberry Pi 上部署为系统服务

先在项目目录完成安装：

```bash
cd ~/projects/pi_kid_voice_bot
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

然后安装并启动 `systemd` 服务：

```bash
./scripts/install_systemd_service.sh
```

查看状态与日志：

```bash
sudo systemctl status pi-kid-voice-bot.service
journalctl -u pi-kid-voice-bot.service -f
```

> 默认服务用户、目录与设备参数在 `deploy/systemd/pi-kid-voice-bot.service` 里，可按你的 Pi 环境修改。

## 下一步建议

1. 接入语音输入（如 `pyaudio` / `sounddevice`）。
2. 添加 STT/TTS 模块（例如 Whisper + edge-tts）。
3. 增加热词唤醒与家长控制逻辑。
4. 补充硬件健康检查与自动更新流程。
