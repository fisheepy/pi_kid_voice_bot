from pi_kid_voice_bot.main import build_parser, run


def test_parser_defaults() -> None:
    args = build_parser().parse_args([])
    assert args.device == "raspberry-pi"
    assert args.dry_run is False


def test_run_dry_run(capsys) -> None:
    code = run(device="pi-test", dry_run=True)
    output = capsys.readouterr().out

    assert code == 0
    assert "pi-test" in output
    assert "Dry run enabled" in output


def test_run_noop_loop_message(capsys) -> None:
    code = run(device="pi-test", dry_run=False)
    output = capsys.readouterr().out

    assert code == 0
    assert "Voice loop is not implemented yet" in output
