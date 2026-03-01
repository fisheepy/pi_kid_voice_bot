# Pi Kid Voice Bot

这是一个用于 Raspberry Pi 的儿童语音机器人项目，当前已支持基础“语音能力”运行链路：

- `keyboard` 模式：终端输入/输出（默认，零额外依赖）
- `microphone` 模式：麦克风采集 + TTS 播放（需安装可选依赖）
- `echo` 引擎：本地规则回声回复
- `chatgpt` 引擎：通过 OpenAI API 生成更有互动性的回答

## 当前内容

- 基础 Python 包结构（`src/pi_kid_voice_bot`）
- 可执行入口脚本（`main.py`）
- 语音运行时与规则引擎骨架（`voice_runtime.py`）
- 麦克风 + TTS 适配器（`audio_adapters.py`）
- ChatGPT 引擎（`llm_engine.py`）
- `pyproject.toml` 打包配置（可 `pip install -e .`）
- 基础单元测试（`tests/`）
- `systemd` 服务模板（`deploy/systemd/pi-kid-voice-bot.service`）
- 一键安装 service 脚本（`scripts/install_systemd_service.sh`）

## 快速开始（键盘模式）

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pi-kid-voice-bot --device pi-01 --mode keyboard --engine echo --once
pytest
```

## 互动模式（持续对话）

```bash
pi-kid-voice-bot --mode keyboard --engine echo
```

输入 `退出` / `exit` / `quit` / `bye` 可结束会话。

## 启用麦克风模式

先安装语音可选依赖：

```bash
pip install -e .[voice]
```

运行一轮语音对话：

```bash
pi-kid-voice-bot --mode microphone --engine echo --once
```

持续运行：

```bash
pi-kid-voice-bot --mode microphone --engine echo
```

> 说明：`speech_recognition` 默认调用 Google Web Speech 进行识别，需要网络；识别失败会返回空文本并触发“请再说一遍”。

## 启用 ChatGPT 互动引擎

安装 LLM 依赖并配置 API Key：

```bash
pip install -e .[llm]
export OPENAI_API_KEY="your_api_key"
```

键盘模式 + ChatGPT：

```bash
pi-kid-voice-bot --mode keyboard --engine chatgpt --openai-model gpt-4o-mini
```

麦克风模式 + ChatGPT：

```bash
pi-kid-voice-bot --mode microphone --engine chatgpt --openai-model gpt-4o-mini
```

也可以覆盖系统提示词：

```bash
pi-kid-voice-bot --mode keyboard --engine chatgpt --system-prompt "你是一个会讲睡前故事的儿童助手"
```

## 常见问题排查

- `FLAC conversion utility not available`
  - 执行：`sudo apt install -y flac`
- `No Default Input Device Available`
  - 先检查：`arecord -l`
  - 再配置默认设备（例如 WM8960 为 `card 3` 时）：
    ```bash
    cat > ~/.asoundrc <<'EOF'
    pcm.!default {
      type asym
      playback.pcm "plughw:3,0"
      capture.pcm "plughw:3,0"
    }
    ctl.!default {
      type hw
      card 3
    }
    EOF
    ```
- `pyttsx3` 初始化失败（缺少 `espeak-ng`）
  - 执行：`sudo apt install -y espeak-ng`

快速健康检查：

```bash
pytest -q
pi-kid-voice-bot --mode keyboard --engine echo --once --device pi-01
pi-kid-voice-bot --mode microphone --engine echo --once
```

## 在 Raspberry Pi 上部署为系统服务

先在项目目录完成安装：

```bash
cd ~/projects/pi_kid_voice_bot
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[voice]
```

如果要使用 ChatGPT，再安装并配置：

```bash
pip install -e .[llm]
export OPENAI_API_KEY="your_api_key"
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

1. 接入离线 STT（如 Vosk / Whisper.cpp）降低网络依赖。
2. 接入更自然的儿童语音 TTS 引擎。
3. 增加唤醒词与家长控制逻辑。
4. 补充硬件健康检查与自动更新流程。
