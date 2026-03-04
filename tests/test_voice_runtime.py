from pi_kid_voice_bot.voice_runtime import EchoRuleEngine, VoiceBotRuntime


class DummyStt:
    def __init__(self, text: str) -> None:
        self.text = text

    def listen(self) -> str:
        return self.text


class DummyTts:
    def __init__(self) -> None:
        self.spoken: list[str] = []

    def speak(self, text: str) -> None:
        self.spoken.append(text)


def test_echo_rule_engine_non_empty() -> None:
    engine = EchoRuleEngine(prefix="收到")
    assert engine.reply("你好") == "收到：你好"


def test_echo_rule_engine_empty() -> None:
    engine = EchoRuleEngine()
    assert engine.reply("   ") == "我没听清楚，你可以再说一遍吗？"


def test_runtime_runs_pipeline() -> None:
    tts = DummyTts()
    runtime = VoiceBotRuntime(stt=DummyStt("小朋友你好"), tts=tts, engine=EchoRuleEngine())

    turn = runtime.run_turn()

    assert turn.user_text == "小朋友你好"
    assert turn.bot_text == "我听到你说：小朋友你好"
    assert tts.spoken == ["我听到你说：小朋友你好"]
