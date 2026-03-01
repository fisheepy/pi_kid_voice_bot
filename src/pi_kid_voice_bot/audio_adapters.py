"""Optional microphone/speaker adapters backed by third-party libraries."""

from __future__ import annotations


class DependencyNotAvailableError(RuntimeError):
    """Raised when optional voice dependencies are missing."""


def _raise_missing(package: str) -> None:
    raise DependencyNotAvailableError(
        f"Missing optional dependency '{package}'. Install with: pip install -e .[voice]"
    )


class MicrophoneSpeechToText:
    """Speech-to-text adapter using speech_recognition and Google recognizer."""

    def __init__(self, language: str = "zh-CN") -> None:
        try:
            import speech_recognition as sr  # type: ignore
        except ModuleNotFoundError as exc:
            _raise_missing("speechrecognition")
            raise exc  # unreachable but satisfies type checkers

        self._sr = sr
        self._recognizer = sr.Recognizer()
        self._language = language

    def listen(self) -> str:
        with self._sr.Microphone() as source:
            print("请说话...", flush=True)
            audio = self._recognizer.listen(source)

        try:
            return self._recognizer.recognize_google(audio, language=self._language)
        except self._sr.UnknownValueError:
            return ""


class PyttsxTextToSpeech:
    """Text-to-speech adapter using pyttsx3."""

    def __init__(self, rate: int = 170) -> None:
        try:
            import pyttsx3  # type: ignore
        except ModuleNotFoundError as exc:
            _raise_missing("pyttsx3")
            raise exc

        self._engine = pyttsx3.init()
        self._engine.setProperty("rate", rate)

    def speak(self, text: str) -> None:
        self._engine.say(text)
        self._engine.runAndWait()
