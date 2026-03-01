"""Optional microphone/speaker adapters backed by third-party libraries."""

from __future__ import annotations

import importlib
import importlib.util


class DependencyNotAvailableError(RuntimeError):
    """Raised when optional voice dependencies are missing."""


class AudioRuntimeError(RuntimeError):
    """Raised when runtime audio backends fail to initialize or process audio."""


def _raise_missing(package: str) -> None:
    raise DependencyNotAvailableError(
        f"Missing optional dependency '{package}'. Install with: pip install -e .[voice]"
    )


def _import_or_raise(module_name: str, package_name: str):
    if importlib.util.find_spec(module_name) is None:
        _raise_missing(package_name)
    return importlib.import_module(module_name)


class MicrophoneSpeechToText:
    """Speech-to-text adapter using speech_recognition and Google recognizer."""

    def __init__(self, language: str = "zh-CN") -> None:
        sr = _import_or_raise("speech_recognition", "speechrecognition")
        self._sr = sr
        self._recognizer = sr.Recognizer()
        self._language = language

    def listen(self) -> str:
        try:
            with self._sr.Microphone() as source:
                print("请说话...", flush=True)
                audio = self._recognizer.listen(source)
        except OSError as exc:
            raise AudioRuntimeError(
                "Microphone device is unavailable. Check `arecord -l` and your ALSA default device config."
            ) from exc

        try:
            return self._recognizer.recognize_google(audio, language=self._language)
        except self._sr.UnknownValueError:
            return ""
        except self._sr.RequestError as exc:
            print(f"[warn] STT request failed: {exc}")
            return ""
        except OSError as exc:
            raise AudioRuntimeError(
                "Speech recognition audio conversion failed. Install system dependency: `sudo apt install -y flac`."
            ) from exc


class PyttsxTextToSpeech:
    """Text-to-speech adapter using pyttsx3."""

    def __init__(self, rate: int = 170) -> None:
        pyttsx3 = _import_or_raise("pyttsx3", "pyttsx3")

        try:
            self._engine = pyttsx3.init()
        except Exception as exc:  # pyttsx3 backend exceptions are not strongly typed
            raise AudioRuntimeError(
                "TTS engine initialization failed. Ensure `espeak-ng` is installed and audio output is configured."
            ) from exc

        self._engine.setProperty("rate", rate)

    def speak(self, text: str) -> None:
        try:
            self._engine.say(text)
            self._engine.runAndWait()
        except Exception as exc:
            raise AudioRuntimeError("TTS playback failed during runAndWait().") from exc
