from pompy.cli import build_large_timer_lines, build_phase_states, build_session_plan, get_args


def test_default_args() -> None:
    args = get_args([])

    assert args.minutes == 25
    assert args.label is None
    assert args.short_break == 5
    assert args.long_break == 15
    assert args.cycles == 1
    assert args.transition_seconds == 2.0
    assert args.transition_wait_key is False
    assert args.bell is True
    assert args.digit_style == "block"


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


def test_phase_states_track_work_and_break_counters() -> None:
    plan = build_session_plan(25, 5, 15, 5)
    states = build_phase_states(plan)

    assert states[0] == ("Work", 25, 1, 5, 0, 4)
    assert states[1] == ("Break", 5, 1, 5, 1, 4)
    assert states[7] == ("Long break", 15, 4, 5, 4, 4)
    assert states[8] == ("Work", 25, 5, 5, 4, 4)


def test_transition_options_parse() -> None:
    args = get_args(["--transition-seconds", "3.5", "--transition-wait-key", "--no-bell"])

    assert args.transition_seconds == 3.5
    assert args.transition_wait_key is True
    assert args.bell is False


def test_short_flags_parse() -> None:
    args = get_args(["-b", "7", "-B", "20", "-c", "3", "-t", "4", "-w"])

    assert args.short_break == 7
    assert args.long_break == 20
    assert args.cycles == 3
    assert args.transition_seconds == 4.0
    assert args.transition_wait_key is True
    assert args.bell is True


def test_digit_style_options_parse() -> None:
    args = get_args(["--digit-style", "segment"])
    assert args.digit_style == "segment"

    args = get_args(["--digit-style", "outline"])
    assert args.digit_style == "outline"

    args = get_args(["-d", "minimal"])
    assert args.digit_style == "minimal"


def test_bell_toggle_parse() -> None:
    args = get_args(["--no-bell"])
    assert args.bell is False

    args = get_args(["--no-bell", "--bell"])
    assert args.bell is True


def test_large_digit_width_is_stable_for_minimal() -> None:
    widths = []
    for timer_text in ["00:00", "11:11", "59:59", "08:40"]:
        lines = build_large_timer_lines(timer_text, "minimal")
        widths.append(max(len(line) for line in lines))

    assert len(set(widths)) == 1


def test_large_digit_width_is_stable_for_all_styles() -> None:
    for style in ["block", "outline", "segment", "minimal"]:
        w1 = max(len(line) for line in build_large_timer_lines("00:00", style))
        w2 = max(len(line) for line in build_large_timer_lines("11:11", style))
        w3 = max(len(line) for line in build_large_timer_lines("59:59", style))
        assert w1 == w2 == w3
