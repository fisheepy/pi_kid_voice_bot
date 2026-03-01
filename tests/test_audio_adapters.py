import types

from pi_kid_voice_bot.audio_adapters import AudioRuntimeError, MicrophoneSpeechToText


class DummyRequestError(Exception):
    pass


class DummyUnknownValueError(Exception):
    pass


class DummyRecognizer:
    def __init__(self, to_raise: Exception | None = None) -> None:
        self.to_raise = to_raise

    def listen(self, source):
        return "audio"

    def recognize_google(self, audio, language: str) -> str:
        if self.to_raise is not None:
            raise self.to_raise
        return "你好"


class DummyMicrophone:
    def __enter__(self):
        return object()

    def __exit__(self, exc_type, exc, tb):
        return None


def _build_fake_sr_module(to_raise: Exception | None = None):
    fake = types.SimpleNamespace()
    fake.RequestError = DummyRequestError
    fake.UnknownValueError = DummyUnknownValueError
    fake.Recognizer = lambda: DummyRecognizer(to_raise=to_raise)
    fake.Microphone = DummyMicrophone
    return fake


def test_microphone_stt_request_error_returns_empty(monkeypatch) -> None:
    fake_sr = _build_fake_sr_module(to_raise=DummyRequestError("net"))
    monkeypatch.setattr("pi_kid_voice_bot.audio_adapters._import_or_raise", lambda *_: fake_sr)

    stt = MicrophoneSpeechToText()
    assert stt.listen() == ""


def test_microphone_stt_unknown_value_returns_empty(monkeypatch) -> None:
    fake_sr = _build_fake_sr_module(to_raise=DummyUnknownValueError("unknown"))
    monkeypatch.setattr("pi_kid_voice_bot.audio_adapters._import_or_raise", lambda *_: fake_sr)

    stt = MicrophoneSpeechToText()
    assert stt.listen() == ""


def test_microphone_stt_flac_missing_raises_runtime_error(monkeypatch) -> None:
    fake_sr = _build_fake_sr_module(to_raise=OSError("flac missing"))
    monkeypatch.setattr("pi_kid_voice_bot.audio_adapters._import_or_raise", lambda *_: fake_sr)

    stt = MicrophoneSpeechToText()

    try:
        stt.listen()
        raise AssertionError("Expected AudioRuntimeError")
    except AudioRuntimeError as exc:
        assert "flac" in str(exc).lower()
