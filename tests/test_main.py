from pi_kid_voice_bot.main import build_parser, run


def test_parser_defaults() -> None:
    args = build_parser().parse_args([])
    assert args.device == "raspberry-pi"
    assert args.dry_run is False
    assert args.mode == "keyboard"
    assert args.engine == "echo"
    assert args.once is False


def test_run_dry_run(capsys) -> None:
    code = run(device="pi-test", dry_run=True)
    output = capsys.readouterr().out

    assert code == 0
    assert "pi-test" in output
    assert "Dry run enabled" in output


def test_run_once_uses_runtime(monkeypatch, capsys) -> None:
    calls: list[str] = []

    class DummyRuntime:
        def run_turn(self):
            calls.append("run_turn")
            return None

    monkeypatch.setattr(
        "pi_kid_voice_bot.main.build_runtime",
        lambda mode, engine, openai_model, system_prompt: DummyRuntime(),
    )

    code = run(device="pi-test", dry_run=False, mode="keyboard", engine="echo", once=True)
    output = capsys.readouterr().out

    assert code == 0
    assert calls == ["run_turn"]
    assert "Voice runtime started in 'keyboard' mode with 'echo' engine." in output


def test_run_once_returns_nonzero_on_runtime_error(monkeypatch, capsys) -> None:
    class FailingRuntime:
        def run_turn(self):
            raise RuntimeError("boom")

    monkeypatch.setattr(
        "pi_kid_voice_bot.main.build_runtime",
        lambda mode, engine, openai_model, system_prompt: FailingRuntime(),
    )

    code = run(device="pi-test", dry_run=False, mode="keyboard", once=True)
    output = capsys.readouterr().out

    assert code == 1
    assert "[error] Runtime failed in once mode" in output


def test_run_returns_nonzero_on_runtime_init_error(monkeypatch, capsys) -> None:
    def _raise(mode: str, engine: str, openai_model: str, system_prompt: str):
        raise RuntimeError("init failed")

    monkeypatch.setattr("pi_kid_voice_bot.main.build_runtime", _raise)

    code = run(device="pi-test", dry_run=False, mode="microphone", once=True)
    output = capsys.readouterr().out

    assert code == 1
    assert "[error] Failed to initialize runtime" in output
