from pi_kid_voice_bot.main import build_parser, run


def test_parser_defaults() -> None:
    args = build_parser().parse_args([])
    assert args.device == "raspberry-pi"
    assert args.dry_run is False
    assert args.mode == "keyboard"
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
        def run_once(self) -> str:
            calls.append("run_once")
            return "ok"

    monkeypatch.setattr("pi_kid_voice_bot.main.build_runtime", lambda mode: DummyRuntime())

    code = run(device="pi-test", dry_run=False, mode="keyboard", once=True)
    output = capsys.readouterr().out

    assert code == 0
    assert calls == ["run_once"]
    assert "Voice runtime started in 'keyboard' mode." in output
