"""Entrypoint for Pi Kid Voice Bot."""

from __future__ import annotations

import argparse
import datetime as dt
import time

from .voice_runtime import ConsoleTextToSpeech, EchoRuleEngine, KeyboardSpeechToText, VoiceBotRuntime


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
        "--once",
        action="store_true",
        help="Run one interaction turn and exit",
    )
    return parser


def build_runtime(mode: str) -> VoiceBotRuntime:
    if mode == "microphone":
        from .audio_adapters import MicrophoneSpeechToText, PyttsxTextToSpeech

        stt = MicrophoneSpeechToText()
        tts = PyttsxTextToSpeech()
    else:
        stt = KeyboardSpeechToText()
        tts = ConsoleTextToSpeech()

    return VoiceBotRuntime(stt=stt, tts=tts, engine=EchoRuleEngine())


def run(device: str, dry_run: bool = False, mode: str = "keyboard", once: bool = False) -> int:
    now = dt.datetime.now().isoformat(timespec="seconds")
    print(f"[{now}] Pi Kid Voice Bot starting on device: {device}")

    if dry_run:
        print("Dry run enabled. Exiting without starting voice loop.")
        return 0

    try:
        runtime = build_runtime(mode)
    except Exception as exc:
        print(f"[error] Failed to initialize runtime in '{mode}' mode: {exc}")
        return 1

    print(f"Voice runtime started in '{mode}' mode.")

    if once:
        try:
            runtime.run_once()
            return 0
        except Exception as exc:
            print(f"[error] Runtime failed in once mode: {exc}")
            return 1

    while True:
        try:
            runtime.run_once()
        except Exception as exc:
            print(f"[warn] Runtime loop error: {exc}")
            time.sleep(1)


def main() -> int:
    args = build_parser().parse_args()
    return run(device=args.device, dry_run=args.dry_run, mode=args.mode, once=args.once)


if __name__ == "__main__":
    raise SystemExit(main())
