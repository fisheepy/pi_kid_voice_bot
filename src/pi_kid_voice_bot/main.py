"""Entrypoint for Pi Kid Voice Bot."""

from __future__ import annotations

import argparse
import datetime as dt

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

    runtime = build_runtime(mode)
    print(f"Voice runtime started in '{mode}' mode.")

    if once:
        runtime.run_once()
        return 0

    while True:
        runtime.run_once()


def main() -> int:
    args = build_parser().parse_args()
    return run(device=args.device, dry_run=args.dry_run, mode=args.mode, once=args.once)


if __name__ == "__main__":
    raise SystemExit(main())
