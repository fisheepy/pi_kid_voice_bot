"""Entrypoint for Pi Kid Voice Bot."""

from __future__ import annotations

import argparse
import datetime as dt


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Pi Kid Voice Bot")
    parser.add_argument("--device", default="raspberry-pi", help="Device identifier")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only print startup info without running bot loop",
    )
    return parser


def run(device: str, dry_run: bool = False) -> int:
    now = dt.datetime.now().isoformat(timespec="seconds")
    print(f"[{now}] Pi Kid Voice Bot starting on device: {device}")

    if dry_run:
        print("Dry run enabled. Exiting without starting voice loop.")
        return 0

    print("Voice loop is not implemented yet. Please add STT/TTS modules.")
    return 0


def main() -> int:
    args = build_parser().parse_args()
    return run(device=args.device, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
