import cv2
import math
import os
import curses
import sys

import time
import argparse


def str2bool(v) -> bool:
    """
    Converts a string to a boolean for argparse
    """
    # https://stackoverflow.com/a/43357954/14370720
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


try:
    term_size = os.get_terminal_size()  # get terminal size
except OSError as e:
    print("Could Not Get Terminal. Make Sure You're Using A Terminal Emulator And Not A Socket (ex: vim)")
    # when using vim to run commands, it's not really a terminal so os.get_terminal_size won't work
    quit(1)

parser = argparse.ArgumentParser()
parser.add_argument("--width", type=int, required=False,
                    default=term_size.columns, help="the width of the output window")
parser.add_argument("--height", type=int, required=False,
                    default=term_size.lines, help="the height of the output window")
parser.add_argument("--usecolor", type=str2bool, required=False, default=False,
                    help="if enabled, color is added based on grayscale values (default False)")
parser.add_argument("--showfps", type=str2bool, required=False,
                    default=True, help="if enabled, shows FPS on top left (default: True)")
args = parser.parse_args()

"""
if args.width > term_size.columns - 1:  # manual width must be <= width of terminal
    print(
        f"Height Must Be Less Than Or Equal To {term_size.columns - 1} (terminal width)")
    quit(1)
if args.height > term_size.lines - 1:  # manual height must be <= height of terminal
    print(
        f"Height Must Be Less Than Or Equal To {term_size.lines - 1} (terminal height)")
    quit(1)

"""
# used to map grayscale to chars
ramp = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "
ramp_size = len(ramp)

vid = cv2.VideoCapture(0)  # camera input

screen = curses.initscr()
curses.curs_set(0)
curses.start_color()
# setting up "heatmap" (only used if --usecolor true)
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)


def heatmap(grayscale) -> int:
    """
    converts a grayscale pixel to 0-7 for the heatmap
    """
    return round(grayscale / 32)


def pix_to_ascii(pix) -> str:
    """
    Converts a grayscale pixel to a character for the ramp
    """
    #ch = ramp[math.ceil(((ramp_size - 1) * pix) / 255)]
    ch = 'a'
    return "\033[38;2;{};{};{}m{}".format(*pix, ch)
    #return "\033[38;2;255;82;197m" + ch


def display_mat(mat) -> None:

    #screen.addstr(0, 0, "*"*500)
    buffer = []
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            buffer.append(pix_to_ascii(mat[i][j]))
            #screen.addstr(i, j,
            #              pix_to_ascii(mat[i][j])
            #              )
    #screen.addstr(0, 0, "".join(buffer))
    print("\033[2J" + "\033[100000A\033[100000D" + "".join(buffer))
                          


last = time.time()
current = time.time()
import time
while True:
    ret, frame = vid.read()

    if not ret:
        print("ERR: Failed To Get Frame From Camera (Make sure a camera is available)")
        break

    mat = cv2.flip(  # take the camera input, make it grayscale, scale it down, and mirror it
        cv2.resize(
            #cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (args.width, args.height)
            frame, (args.width, args.height)
        ), 1)

    screen.nodelay(1)
    c = screen.getch()
    if c == 3:  # Ctrl+C
        quit()
    else:
        curses.flushinp()

    #screen.clear()
    # display the current frame using the ramp + heatmap (if enabled)
    display_mat(mat)

    last = current
    current = time.time()
    try:
        # calculate fps for top left of screen
        fps = "%.1f" % (1 / (current - last))
    except ZeroDivisionError:
        fps = "inf"  # some frames may take < 1 ms causing div by 0 error
    if args.showfps:
        print("\033[100000A\033[100000D" + "".join(fps))
        pass
        #screen.addstr(0, 0, fps)
    #screen.refresh()


vid.release()
cv2.destroyAllWindows()
