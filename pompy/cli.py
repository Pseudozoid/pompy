import argparse
import curses
import time

from pompy import __version__

def get_args():
    parser = argparse.ArgumentParser(
        prog="pompy",
        description="Pomodoro timer for your terminal.",
    )
    parser.add_argument(
        "minutes",
        nargs="?",
        type=int,
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
        type=int,
        help="Pomodoro length in minutes.",
    )
    parser.add_argument(
        "-l",
        "--label",
        dest="label_flag",
        help="Optional label shown under the timer.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"pompy {__version__}",
    )

    args = parser.parse_args()
    minutes = args.minutes_flag if args.minutes_flag is not None else args.minutes
    label = args.label_flag if args.label_flag is not None else " ".join(args.label) or None

    if minutes <= 0:
        parser.error("minutes must be a positive integer")

    return minutes, label

def show_message(stdscr, message):
    stdscr.clear()
    rows, cols = stdscr.getmaxyx()
    y = rows // 2
    x = (cols - len(message)) // 2
    stdscr.addstr(y, x, message, curses.color_pair(4))
    stdscr.refresh()

    stdscr.nodelay(False)
    stdscr.getch()

def draw_box(stdscr, top, left, width, height):
    # horizontal borders
    for i in range(width):
        stdscr.addch(top, left + i, '-')
        stdscr.addch(top + height - 1, left + i, '-')

    # vertical borders
    for i in range(height):
        stdscr.addch(top + i, left, '|')
        stdscr.addch(top + i, left + width - 1, '|')

def pomodoro(stdscr, time_limit, label):
    curses.start_color()
    curses.use_default_colors()
    stdscr.bkgd(' ', curses.color_pair(0))
    curses.curs_set(0)
    stdscr.nodelay(True)

    curses.init_pair(1, curses.COLOR_CYAN, -1)   
    curses.init_pair(2, curses.COLOR_WHITE, -1)  
    curses.init_pair(3, curses.COLOR_YELLOW, -1) 
    curses.init_pair(4, curses.COLOR_GREEN, -1)  

    total_seconds = time_limit * 60
    paused = False
    quit_early = False
    last_second = int(time.monotonic())

    try:
        while total_seconds > 0:
            key = stdscr.getch()

            if key == ord('q'):
                quit_early = True
                break

            if key == ord(' '):
                paused = not paused

            now = time.monotonic()
            if not paused and int(now) != last_second:
                total_seconds -= 1
                last_second = int(now)

            minutes = total_seconds // 60
            seconds = total_seconds % 60
            text = f"{minutes:02d}:{seconds:02d}"

            stdscr.clear()
            rows, cols = stdscr.getmaxyx()

            y = rows // 2
            x = (cols - len(text)) // 2

            box_width = len(text) + 6
            box_height = 7
            top = y - box_height // 2
            left = (cols - box_width) // 2

            draw_box(stdscr, top, left, box_width, box_height)
            if paused:
                timer_attr = curses.color_pair(1) | curses.A_DIM
            else:
                timer_attr = curses.color_pair(1) | curses.A_BOLD

            stdscr.addstr(y, x, text, timer_attr)

            if label:
                stdscr.addstr(
                    y + 2,
                    (cols - len(label)) // 2,
                    label,
                    curses.A_DIM
                )

            if paused:
                pause_text = "PAUSED (space to resume, q to quit)"
                stdscr.addstr(
                    y + 4,
                    (cols - len(pause_text)) // 2,
                    pause_text,
                    curses.color_pair(3) | curses.A_DIM
                )

            stdscr.refresh()
            time.sleep(0.1)

        if quit_early:
            show_message(stdscr, "Quit. Take a breath.")
        else:
            show_message(stdscr, "Time's up!")

    except KeyboardInterrupt:
        show_message(stdscr, "Pomodoro interrupted. Take a breath.")

def main():
    time_limit, label = get_args()
    curses.wrapper(pomodoro, time_limit, label)
