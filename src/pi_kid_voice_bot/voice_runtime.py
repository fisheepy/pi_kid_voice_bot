"""Voice runtime components for Pi Kid Voice Bot."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class SpeechToText(Protocol):
    def listen(self) -> str:
        """Record and transcribe one utterance."""


class TextToSpeech(Protocol):
    def speak(self, text: str) -> None:
        """Speak text output."""


class RuleEngine(Protocol):
    def reply(self, text: str) -> str:
        """Return bot response for a given input."""


@dataclass(slots=True)
class TurnResult:
    user_text: str
    bot_text: str


@dataclass(slots=True)
class VoiceBotRuntime:
    """Single-turn voice pipeline runtime."""

    stt: SpeechToText
    tts: TextToSpeech
    engine: RuleEngine

    def run_turn(self) -> TurnResult:
        user_text = self.stt.listen()
        response = self.engine.reply(user_text)
        self.tts.speak(response)
        return TurnResult(user_text=user_text, bot_text=response)

    def run_once(self) -> str:
        return self.run_turn().bot_text


@dataclass(slots=True)
class EchoRuleEngine:
    """Simple deterministic response engine for baseline integration."""

    prefix: str = "我听到你说"

    def reply(self, text: str) -> str:
        normalized = text.strip()
        if not normalized:
            return "我没听清楚，你可以再说一遍吗？"
        return f"{self.prefix}：{normalized}"


class KeyboardSpeechToText:
    """Fallback STT adapter using terminal input instead of microphone."""

    def listen(self) -> str:
        return input("你：").strip()


class ConsoleTextToSpeech:
    """Fallback TTS adapter that prints bot output."""

    def speak(self, text: str) -> None:
        print(f"机器人：{text}")
