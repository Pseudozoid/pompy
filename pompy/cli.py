import argparse
import curses
import time
from typing import Dict, List, Optional, Sequence, Tuple

from pompy import __version__

SessionPlan = List[Tuple[str, int]]

BLOCK_DIGITS = {
    "0": [
        " ### ",
        "#   #",
        "#   #",
        "#   #",
        " ### ",
    ],
    "1": [
        "  #  ",
        " ##  ",
        "  #  ",
        "  #  ",
        " ### ",
    ],
    "2": [
        " ### ",
        "#   #",
        "   # ",
        "  #  ",
        "#####",
    ],
    "3": [
        "#### ",
        "    #",
        " ### ",
        "    #",
        "#### ",
    ],
    "4": [
        "#   #",
        "#   #",
        "#####",
        "    #",
        "    #",
    ],
    "5": [
        "#####",
        "#    ",
        "#### ",
        "    #",
        "#### ",
    ],
    "6": [
        " ### ",
        "#    ",
        "#### ",
        "#   #",
        " ### ",
    ],
    "7": [
        "#####",
        "    #",
        "   # ",
        "  #  ",
        "  #  ",
    ],
    "8": [
        " ### ",
        "#   #",
        " ### ",
        "#   #",
        " ### ",
    ],
    "9": [
        " ### ",
        "#   #",
        " ####",
        "    #",
        " ### ",
    ],
    ":": [
        "  ",
        " #",
        "  ",
        " #",
        "  ",
    ],
}

SEGMENT_DIGITS = {
    "0": [
        " --- ",
        "|   |",
        "|   |",
        "|   |",
        " --- ",
    ],
    "1": [
        "  |  ",
        "  |  ",
        "  |  ",
        "  |  ",
        "  |  ",
    ],
    "2": [
        " --- ",
        "    |",
        " --- ",
        "|    ",
        " --- ",
    ],
    "3": [
        " --- ",
        "    |",
        " --- ",
        "    |",
        " --- ",
    ],
    "4": [
        "|   |",
        "|   |",
        " --- ",
        "    |",
        "    |",
    ],
    "5": [
        " --- ",
        "|    ",
        " --- ",
        "    |",
        " --- ",
    ],
    "6": [
        " --- ",
        "|    ",
        " --- ",
        "|   |",
        " --- ",
    ],
    "7": [
        " --- ",
        "    |",
        "    |",
        "    |",
        "    |",
    ],
    "8": [
        " --- ",
        "|   |",
        " --- ",
        "|   |",
        " --- ",
    ],
    "9": [
        " --- ",
        "|   |",
        " --- ",
        "    |",
        " --- ",
    ],
    ":": [
        "     ",
        "  .  ",
        "     ",
        "  .  ",
        "     ",
    ],
}

OUTLINE_DIGITS = {
    "0": [
        " /-\\ ",
        "|   |",
        "|   |",
        "|   |",
        " \\-/ ",
    ],
    "1": [
        "  /| ",
        " / | ",
        "   | ",
        "   | ",
        "  _|_",
    ],
    "2": [
        " /--\\",
        "    /",
        "  _/ ",
        " /   ",
        "/___ ",
    ],
    "3": [
        " /--\\",
        "    /",
        "  -< ",
        "    \\",
        " \\--/",
    ],
    "4": [
        " /  /",
        "/  / ",
        "|__|_",
        "   / ",
        "  /  ",
    ],
    "5": [
        " ____",
        "|    ",
        "|--\\ ",
        "    |",
        " \\--/",
    ],
    "6": [
        " /--\\",
        "|    ",
        "|--\\ ",
        "|   |",
        " \\--/",
    ],
    "7": [
        "____/",
        "   / ",
        "  /  ",
        " /   ",
        "/    ",
    ],
    "8": [
        " /--\\",
        "|   |",
        " >--<",
        "|   |",
        " \\--/",
    ],
    "9": [
        " /--\\",
        "|   |",
        " \\--|",
        "    |",
        " \\--/",
    ],
    ":": [
        "   ",
        " o ",
        "   ",
        " o ",
        "   ",
    ],
}

MINIMAL_DIGITS = {
    "0": [
        " _ ",
        "| |",
        "| |",
        "|_|",
        "   ",
    ],
    "1": [
        "   ",
        "  |",
        "  |",
        "  |",
        "   ",
    ],
    "2": [
        " _ ",
        " _|",
        "|_ ",
        "   ",
        "   ",
    ],
    "3": [
        " _ ",
        " _|",
        " _|",
        "   ",
        "   ",
    ],
    "4": [
        "   ",
        "|_|",
        "  |",
        "   ",
        "   ",
    ],
    "5": [
        " _ ",
        "|_ ",
        " _|",
        "   ",
        "   ",
    ],
    "6": [
        " _ ",
        "|_ ",
        "|_|",
        "   ",
        "   ",
    ],
    "7": [
        " _ ",
        "  |",
        "  |",
        "   ",
        "   ",
    ],
    "8": [
        " _ ",
        "|_|",
        "|_|",
        "   ",
        "   ",
    ],
    "9": [
        " _ ",
        "|_|",
        " _|",
        "   ",
        "   ",
    ],
    ":": [
        " ",
        ".",
        " ",
        ".",
        " ",
    ],
}

DIGIT_STYLES: Dict[str, Dict[str, List[str]]] = {
    "block": BLOCK_DIGITS,
    "outline": OUTLINE_DIGITS,
    "segment": SEGMENT_DIGITS,
    "minimal": MINIMAL_DIGITS,
}


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def positive_float(value: str) -> float:
    parsed = float(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive number")
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
        "-b",
        "--break",
        dest="short_break",
        type=positive_int,
        default=5,
        help="Short break length in minutes (default: 5).",
    )
    parser.add_argument(
        "-B",
        "--long-break",
        dest="long_break",
        type=positive_int,
        default=15,
        help="Long break length in minutes (default: 15).",
    )
    parser.add_argument(
        "-c",
        "--cycles",
        type=positive_int,
        default=1,
        help="Number of work sessions to run (default: 1).",
    )
    parser.add_argument(
        "-t",
        "--transition-seconds",
        type=positive_float,
        default=2.0,
        help="Transition screen duration in seconds (default: 2.0).",
    )
    parser.add_argument(
        "-w",
        "--transition-wait-key",
        action="store_true",
        help="Wait for a key press on transition screens before the next phase.",
    )
    parser.add_argument(
        "-d",
        "--digit-style",
        choices=sorted(DIGIT_STYLES.keys()),
        default="block",
        help="Large timer digit style (default: block).",
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


def format_mmss(total_seconds: int) -> str:
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"


def draw_progress_bar(width: int, ratio: float) -> str:
    inner_width = max(10, width - 2)
    clamped = max(0.0, min(1.0, ratio))
    filled = int(inner_width * clamped)
    return "[" + ("#" * filled) + ("-" * (inner_width - filled)) + "]"


def build_large_timer_lines(text: str, digit_style: str) -> List[str]:
    digit_map = DIGIT_STYLES[digit_style]
    lines = ["", "", "", "", ""]
    for char_index, char in enumerate(text):
        glyph = digit_map.get(char)
        if glyph is None:
            continue
        spacer = " " if char_index > 0 else ""
        for row in range(5):
            lines[row] += spacer + glyph[row]
    return lines


def draw_phase(
    stdscr,
    phase_total_seconds: int,
    total_seconds: int,
    label: Optional[str],
    phase_name: str,
    work_index: int,
    total_work_sessions: int,
    break_index: int,
    total_break_sessions: int,
    paused: bool,
    digit_style: str,
) -> None:
    is_break = phase_name != "Work"
    is_long_break = phase_name == "Long break"

    text = format_mmss(total_seconds)
    large_lines = build_large_timer_lines(text, digit_style)
    large_width = max(len(line) for line in large_lines)

    stdscr.clear()
    rows, cols = stdscr.getmaxyx()
    compact_mode = rows < 16 or cols < 52
    can_use_large_digits = not compact_mode and rows >= 22 and cols >= large_width + 12

    y = rows // 2
    x = max(0, (cols - len(text)) // 2)
    timer_top = y
    timer_height = 1

    if can_use_large_digits:
        timer_height = 5
        timer_top = max(6, (rows // 2) - 3)

    if can_use_large_digits:
        box_width = large_width + 6
        box_height = timer_height + 4
    else:
        box_width = len(text) + 6
        box_height = 7

    box_center_y = timer_top + (timer_height // 2)
    top = box_center_y - box_height // 2
    left = (cols - box_width) // 2

    if is_break:
        status = f"{phase_name} ({break_index}/{total_break_sessions})"
    else:
        status = f"{phase_name} ({work_index}/{total_work_sessions})"
    if is_long_break:
        status_attr = curses.color_pair(6) | curses.A_BOLD
    elif is_break:
        status_attr = curses.color_pair(5) | curses.A_BOLD
    else:
        status_attr = curses.color_pair(2) | curses.A_BOLD

    safe_addstr(
        stdscr,
        3,
        max(0, (cols - len(status)) // 2),
        status,
        status_attr,
    )

    box_attr = status_attr
    if not compact_mode and rows > box_height and cols > box_width and top >= 0 and left >= 0:
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
    if can_use_large_digits:
        large_x = max(0, (cols - large_width) // 2)
        for row_index, line in enumerate(large_lines):
            safe_addstr(stdscr, timer_top + row_index, large_x, line, timer_attr)
    else:
        safe_addstr(stdscr, y, x, text, timer_attr)

    ratio = (phase_total_seconds - total_seconds) / max(1, phase_total_seconds)
    progress_bar = draw_progress_bar(min(40, cols - 6), ratio)
    progress_line = progress_bar

    progress_center_x = cols // 2
    if 0 <= left and box_width <= cols:
        progress_center_x = left + (box_width // 2)
    progress_col = max(0, progress_center_x - (len(progress_line) // 2))

    if compact_mode:
        safe_addstr(
            stdscr,
            min(rows - 2, y + 3),
            progress_col,
            progress_line,
            curses.A_DIM,
        )
    else:
        progress_row = min(rows - 3, timer_top + timer_height + 3)
        safe_addstr(
            stdscr,
            progress_row,
            progress_col,
            progress_line,
            curses.A_DIM,
        )

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
        if compact_mode:
            label_row = min(rows - 1, y + 1)
        else:
            label_row = min(rows - 1, timer_top + timer_height + 1)
        safe_addstr(
            stdscr,
            label_row,
            max(0, (cols - len(phase_label)) // 2),
            phase_label,
            phase_label_attr,
        )

    if paused:
        pause_text = "PAUSED (space to resume, q to quit)"
        if compact_mode:
            pause_row = min(rows - 1, y + 3)
        else:
            pause_row = min(rows - 2, timer_top + timer_height + 4)
        safe_addstr(
            stdscr,
            pause_row,
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
    work_index: int,
    total_work_sessions: int,
    break_index: int,
    total_break_sessions: int,
    digit_style: str,
) -> bool:
    total_seconds = minutes * 60
    phase_total_seconds = total_seconds
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
            phase_total_seconds,
            total_seconds,
            phase_label,
            phase_name,
            work_index,
            total_work_sessions,
            break_index,
            total_break_sessions,
            paused,
            digit_style,
        )
        time.sleep(0.1)

    return False


def show_transition(
    stdscr,
    phase_name: str,
    minutes: int,
    phase_index: int,
    total_phases: int,
    transition_seconds: float,
    wait_for_key: bool,
) -> bool:
    stdscr.clear()
    rows, cols = stdscr.getmaxyx()

    title = f"Up next: {phase_name}"
    detail = f"{format_mmss(minutes * 60)} ({phase_index}/{total_phases})"
    if wait_for_key:
        hint = "Press any key to begin (q to quit)"
    else:
        hint = "Get ready..."

    safe_addstr(stdscr, rows // 2 - 1, max(0, (cols - len(title)) // 2), title, curses.A_BOLD)
    safe_addstr(stdscr, rows // 2, max(0, (cols - len(detail)) // 2), detail, curses.A_DIM)
    safe_addstr(stdscr, rows // 2 + 2, max(0, (cols - len(hint)) // 2), hint, curses.A_DIM)
    stdscr.refresh()

    if wait_for_key:
        stdscr.nodelay(False)
        key = stdscr.getch()
        stdscr.nodelay(True)
        return key == ord('q')

    start = time.monotonic()
    while time.monotonic() - start < transition_seconds:
        key = stdscr.getch()
        if key == ord('q'):
            return True
        time.sleep(0.05)

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
    # corners
    stdscr.addch(top, left, '+', attr)
    stdscr.addch(top, left + width - 1, '+', attr)
    stdscr.addch(top + height - 1, left, '+', attr)
    stdscr.addch(top + height - 1, left + width - 1, '+', attr)

    # horizontal edges
    for i in range(1, width - 1):
        stdscr.addch(top, left + i, '-', attr)
        stdscr.addch(top + height - 1, left + i, '-', attr)

    # vertical edges
    for i in range(1, height - 1):
        stdscr.addch(top + i, left, '|', attr)
        stdscr.addch(top + i, left + width - 1, '|', attr)

def run_session(stdscr, plan: SessionPlan, label: Optional[str], args: argparse.Namespace) -> None:
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

    total_work_sessions = sum(1 for phase_name, _ in plan if phase_name == "Work")
    total_break_sessions = sum(1 for phase_name, _ in plan if phase_name != "Work")
    work_counter = 0
    break_counter = 0

    try:
        for phase_index, (phase_name, minutes) in enumerate(plan, start=1):
            if phase_index > 1:
                quit_early = show_transition(
                    stdscr,
                    phase_name,
                    minutes,
                    phase_index,
                    len(plan),
                    transition_seconds=args.transition_seconds,
                    wait_for_key=args.transition_wait_key,
                )
                if quit_early:
                    show_message(stdscr, "Quit. Take a breath.")
                    return

            if phase_name == "Work":
                work_counter += 1
                current_work = work_counter
                current_break = break_counter
            else:
                break_counter += 1
                current_work = work_counter
                current_break = break_counter

            quit_early = run_phase(
                stdscr,
                phase_name,
                minutes,
                label,
                current_work,
                total_work_sessions,
                current_break,
                total_break_sessions,
                args.digit_style,
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
    curses.wrapper(run_session, plan, args.label, args)
