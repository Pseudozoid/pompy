import argparse
import curses
import time
from typing import List, Optional, Sequence, Tuple

from pompy import __version__

SessionPlan = List[Tuple[str, int]]


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def get_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="pompy",
        description="Pomodoro timer for your terminal.",
    )
    parser.add_argument(
        "minutes",
        nargs="?",
        type=positive_int,
        default=25,
        help="Pomodoro length in minutes (default: 25).",
    )
    parser.add_argument(
        "label",
        nargs="*",
        help="Optional label shown under the timer.",
    )
    parser.add_argument(
        "-m",
        "--minutes",
        dest="minutes_flag",
        type=positive_int,
        help="Pomodoro length in minutes.",
    )
    parser.add_argument(
        "-l",
        "--label",
        dest="label_flag",
        help="Optional label shown under the timer.",
    )
    parser.add_argument(
        "--break",
        dest="short_break",
        type=positive_int,
        default=5,
        help="Short break length in minutes (default: 5).",
    )
    parser.add_argument(
        "--long-break",
        dest="long_break",
        type=positive_int,
        default=15,
        help="Long break length in minutes (default: 15).",
    )
    parser.add_argument(
        "--cycles",
        type=positive_int,
        default=1,
        help="Number of work sessions to run (default: 1).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"pompy {__version__}",
    )

    args = parser.parse_args(argv)
    minutes = args.minutes_flag if args.minutes_flag is not None else args.minutes
    label = args.label_flag if args.label_flag is not None else " ".join(args.label) or None

    args.minutes = minutes
    args.label = label

    return args


def build_session_plan(
    work_minutes: int,
    short_break: int,
    long_break: int,
    cycles: int,
) -> SessionPlan:
    plan: SessionPlan = []

    for cycle in range(1, cycles + 1):
        plan.append(("Work", work_minutes))
        if cycle < cycles:
            if cycle % 4 == 0:
                plan.append(("Long break", long_break))
            else:
                plan.append(("Break", short_break))

    return plan


def safe_addstr(stdscr, y: int, x: int, text: str, attr: int = 0) -> None:
    try:
        stdscr.addstr(y, x, text, attr)
    except curses.error:
        pass


def draw_phase(
    stdscr,
    total_seconds: int,
    label: Optional[str],
    phase_name: str,
    phase_index: int,
    total_phases: int,
    paused: bool,
) -> None:
    is_break = phase_name != "Work"
    is_long_break = phase_name == "Long break"

    minutes = total_seconds // 60
    seconds = total_seconds % 60
    text = f"{minutes:02d}:{seconds:02d}"

    stdscr.clear()
    rows, cols = stdscr.getmaxyx()
    y = rows // 2
    x = max(0, (cols - len(text)) // 2)

    box_width = len(text) + 6
    box_height = 7
    top = y - box_height // 2
    left = (cols - box_width) // 2

    status = f"{phase_name} ({phase_index}/{total_phases})"
    if is_long_break:
        status_attr = curses.color_pair(6) | curses.A_BOLD
    elif is_break:
        status_attr = curses.color_pair(5) | curses.A_BOLD
    else:
        status_attr = curses.color_pair(2) | curses.A_BOLD

    safe_addstr(
        stdscr,
        max(0, y - 3),
        max(0, (cols - len(status)) // 2),
        status,
        status_attr,
    )

    box_attr = status_attr
    if rows > box_height and cols > box_width and top >= 0 and left >= 0:
        draw_box(stdscr, top, left, box_width, box_height, box_attr)

    if is_long_break:
        timer_color = curses.color_pair(6)
    elif is_break:
        timer_color = curses.color_pair(5)
    else:
        timer_color = curses.color_pair(1)
    if paused:
        timer_attr = timer_color | curses.A_DIM
    else:
        timer_attr = timer_color | curses.A_BOLD
    safe_addstr(stdscr, y, x, text, timer_attr)

    if is_long_break:
        phase_label = "LONG BREAK"
        phase_label_attr = curses.color_pair(6) | curses.A_BOLD
    elif is_break:
        phase_label = "BREAK"
        phase_label_attr = curses.color_pair(5) | curses.A_BOLD
    else:
        phase_label = label
        phase_label_attr = curses.A_DIM

    if phase_label:
        safe_addstr(
            stdscr,
            min(rows - 1, y + 2),
            max(0, (cols - len(phase_label)) // 2),
            phase_label,
            phase_label_attr,
        )

    if paused:
        pause_text = "PAUSED (space to resume, q to quit)"
        safe_addstr(
            stdscr,
            min(rows - 1, y + 4),
            max(0, (cols - len(pause_text)) // 2),
            pause_text,
            curses.color_pair(3) | curses.A_DIM,
        )

    stdscr.refresh()


def run_phase(
    stdscr,
    phase_name: str,
    minutes: int,
    label: Optional[str],
    phase_index: int,
    total_phases: int,
) -> bool:
    total_seconds = minutes * 60
    paused = False
    last_second = int(time.monotonic())

    while total_seconds > 0:
        key = stdscr.getch()

        if key == ord('q'):
            return True

        if key == ord(' '):
            paused = not paused

        now = time.monotonic()
        if not paused and int(now) != last_second:
            total_seconds -= 1
            last_second = int(now)

        phase_label = label if phase_name == "Work" else None
        draw_phase(
            stdscr,
            total_seconds,
            phase_label,
            phase_name,
            phase_index,
            total_phases,
            paused,
        )
        time.sleep(0.1)

    return False


def show_message(stdscr, message):
    stdscr.clear()
    rows, cols = stdscr.getmaxyx()
    y = rows // 2
    x = (cols - len(message)) // 2
    stdscr.addstr(y, x, message, curses.color_pair(4))
    stdscr.refresh()

    stdscr.nodelay(False)
    stdscr.getch()

def draw_box(stdscr, top, left, width, height, attr=0):
    # horizontal borders
    for i in range(width):
        stdscr.addch(top, left + i, '-', attr)
        stdscr.addch(top + height - 1, left + i, '-', attr)

    # vertical borders
    for i in range(height):
        stdscr.addch(top + i, left, '|', attr)
        stdscr.addch(top + i, left + width - 1, '|', attr)

def run_session(stdscr, plan: SessionPlan, label: Optional[str]) -> None:
    curses.start_color()
    curses.use_default_colors()
    stdscr.bkgd(' ', curses.color_pair(0))
    curses.curs_set(0)
    stdscr.nodelay(True)

    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_WHITE, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)
    curses.init_pair(4, curses.COLOR_GREEN, -1)
    curses.init_pair(5, curses.COLOR_BLUE, -1)
    curses.init_pair(6, curses.COLOR_MAGENTA, -1)

    try:
        for phase_index, (phase_name, minutes) in enumerate(plan, start=1):
            quit_early = run_phase(
                stdscr,
                phase_name,
                minutes,
                label,
                phase_index,
                len(plan),
            )
            if quit_early:
                show_message(stdscr, "Quit. Take a breath.")
                return

        show_message(stdscr, "Session complete!")

    except KeyboardInterrupt:
        show_message(stdscr, "Pomodoro interrupted. Take a breath.")

def main():
    args = get_args()
    plan = build_session_plan(
        work_minutes=args.minutes,
        short_break=args.short_break,
        long_break=args.long_break,
        cycles=args.cycles,
    )
    curses.wrapper(run_session, plan, args.label)
