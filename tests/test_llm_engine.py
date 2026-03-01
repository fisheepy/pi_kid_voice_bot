import types

from pi_kid_voice_bot.llm_engine import ChatGPTRuleEngine, LLMDependencyError


class DummyResponses:
    def create(self, **kwargs):
        return types.SimpleNamespace(output_text="你好呀")


class DummyOpenAIClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.responses = DummyResponses()


class DummyOpenAIModule:
    OpenAI = DummyOpenAIClient


def test_chatgpt_engine_requires_api_key(monkeypatch) -> None:
    monkeypatch.setattr("pi_kid_voice_bot.llm_engine.importlib.util.find_spec", lambda name: object())
    monkeypatch.setattr("pi_kid_voice_bot.llm_engine.importlib.import_module", lambda name: DummyOpenAIModule)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    try:
        ChatGPTRuleEngine()
        raise AssertionError("Expected LLMDependencyError")
    except LLMDependencyError as exc:
        assert "OPENAI_API_KEY" in str(exc)


def test_chatgpt_engine_reply(monkeypatch) -> None:
    monkeypatch.setattr("pi_kid_voice_bot.llm_engine.importlib.util.find_spec", lambda name: object())
    monkeypatch.setattr("pi_kid_voice_bot.llm_engine.importlib.import_module", lambda name: DummyOpenAIModule)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    engine = ChatGPTRuleEngine(model="gpt-4o-mini")
    assert engine.reply("你好") == "你好呀"
