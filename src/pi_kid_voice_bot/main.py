"""Entrypoint for Pi Kid Voice Bot."""

from __future__ import annotations

import argparse
import datetime as dt
import time

from .voice_runtime import ConsoleTextToSpeech, EchoRuleEngine, KeyboardSpeechToText, VoiceBotRuntime

EXIT_WORDS = {"退出", "exit", "quit", "bye"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Pi Kid Voice Bot")
    parser.add_argument("--device", default="raspberry-pi", help="Device identifier")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only print startup info without running bot loop",
    )
    parser.add_argument(
        "--mode",
        choices=["keyboard", "microphone"],
        default="keyboard",
        help="Input/output mode: keyboard (fallback) or microphone (requires optional deps)",
    )
    parser.add_argument(
        "--engine",
        choices=["echo", "chatgpt"],
        default="echo",
        help="Reply engine: local echo rule or ChatGPT API",
    )
    parser.add_argument(
        "--openai-model",
        default="gpt-4o-mini",
        help="OpenAI model name when --engine chatgpt",
    )
    parser.add_argument(
        "--system-prompt",
        default="你是一个面向儿童的温柔语音助手，请用简短、友好的中文回答。",
        help="System prompt when --engine chatgpt",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run one interaction turn and exit",
    )
    return parser


def build_runtime(mode: str, engine: str, openai_model: str, system_prompt: str) -> VoiceBotRuntime:
    if mode == "microphone":
        from .audio_adapters import MicrophoneSpeechToText, PyttsxTextToSpeech

        stt = MicrophoneSpeechToText()
        tts = PyttsxTextToSpeech()
    else:
        stt = KeyboardSpeechToText()
        tts = ConsoleTextToSpeech()

    if engine == "chatgpt":
        from .llm_engine import ChatGPTRuleEngine

        rule_engine = ChatGPTRuleEngine(model=openai_model, system_prompt=system_prompt)
    else:
        rule_engine = EchoRuleEngine()

    return VoiceBotRuntime(stt=stt, tts=tts, engine=rule_engine)


def run(
    device: str,
    dry_run: bool = False,
    mode: str = "keyboard",
    engine: str = "echo",
    openai_model: str = "gpt-4o-mini",
    system_prompt: str = "你是一个面向儿童的温柔语音助手，请用简短、友好的中文回答。",
    once: bool = False,
) -> int:
    now = dt.datetime.now().isoformat(timespec="seconds")
    print(f"[{now}] Pi Kid Voice Bot starting on device: {device}")

    if dry_run:
        print("Dry run enabled. Exiting without starting voice loop.")
        return 0

    try:
        runtime = build_runtime(mode, engine, openai_model, system_prompt)
    except Exception as exc:
        print(f"[error] Failed to initialize runtime in '{mode}' mode with engine '{engine}': {exc}")
        return 1

    print(f"Voice runtime started in '{mode}' mode with '{engine}' engine.")

    if once:
        try:
            runtime.run_turn()
            return 0
        except Exception as exc:
            print(f"[error] Runtime failed in once mode: {exc}")
            return 1

    while True:
        try:
            turn = runtime.run_turn()
            if turn.user_text.strip().lower() in EXIT_WORDS:
                print("收到退出指令，正在结束会话。")
                return 0
        except Exception as exc:
            print(f"[warn] Runtime loop error: {exc}")
            time.sleep(1)


def main() -> int:
    args = build_parser().parse_args()
    return run(
        device=args.device,
        dry_run=args.dry_run,
        mode=args.mode,
        engine=args.engine,
        openai_model=args.openai_model,
        system_prompt=args.system_prompt,
        once=args.once,
    )


if __name__ == "__main__":
    raise SystemExit(main())
