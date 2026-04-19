from pompy.cli import build_session_plan, get_args


def test_default_args() -> None:
    args = get_args([])

    assert args.minutes == 25
    assert args.label is None
    assert args.short_break == 5
    assert args.long_break == 15
    assert args.cycles == 1
    assert args.transition_seconds == 2.0
    assert args.transition_wait_key is False


def test_positional_values() -> None:
    args = get_args(["30", "deep", "work"])

    assert args.minutes == 30
    assert args.label == "deep work"


def test_flag_values_override_positionals() -> None:
    args = get_args(["20", "focus", "--minutes", "35", "--label", "override"])

    assert args.minutes == 35
    assert args.label == "override"


def test_invalid_minutes_exits() -> None:
    try:
        get_args(["0"])
        assert False, "Expected argparse to raise SystemExit for invalid minutes"
    except SystemExit:
        pass


def test_single_cycle_plan_has_only_work() -> None:
    assert build_session_plan(25, 5, 15, 1) == [("Work", 25)]


def test_break_cycle_plan_uses_long_break_every_fourth_cycle() -> None:
    plan = build_session_plan(25, 5, 15, 5)

    assert plan == [
        ("Work", 25),
        ("Break", 5),
        ("Work", 25),
        ("Break", 5),
        ("Work", 25),
        ("Break", 5),
        ("Work", 25),
        ("Long break", 15),
        ("Work", 25),
    ]


def test_transition_options_parse() -> None:
    args = get_args(["--transition-seconds", "3.5", "--transition-wait-key"])

    assert args.transition_seconds == 3.5
    assert args.transition_wait_key is True
