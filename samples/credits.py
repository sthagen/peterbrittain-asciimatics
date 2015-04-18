from asciimatics.effects import Scroll, Mirage, Wipe, Cycle, Matrix, \
    BannerText, Stars, Print
from asciimatics.renderers import FigletText, ImageFile, SpeechBubble
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.sprites import Sam
from asciimatics.paths import Path
import curses
import math


def ascii_credits():
    """
    Asciimatics credits!
    """
    curses.wrapper(_credits)


def _credits(win):
    screen = Screen(win)

    scenes = []
    centre = (screen.width / 2, screen.height / 2)
    curve_path = []
    for i in range(0, 11):
        curve_path.append(
            (centre[0] + (screen.width / 3 * math.sin(i * math.pi / 5)),
             centre[1] - (screen.height / 3 * math.cos(i * math.pi / 5))))
    path = Path()
    path.jump_to(-20, centre[1] - screen.height / 3)
    path.move_straight_to(centre[0], centre[1] - screen.height / 3, 10),
    path.wait(30)
    path.move_round_to(curve_path, 80)
    path.wait(30)
    path.move_straight_to(7, 4, 10)
    path.wait(300)

    effects = [
        Sam(screen, path),
        Print(screen,
              SpeechBubble("WELCOME TO ASCIIMATICS", "L"),
              x=centre[0] + 12, y=(centre[1] - screen.height / 3) - 4,
              colour=curses.COLOR_CYAN,
              clear=True,
              start_frame=20,
              stop_frame=50),
        Print(screen,
              SpeechBubble("Wheeeeeee!"),
              y=centre[1],
              colour=curses.COLOR_CYAN,
              clear=True,
              start_frame=100,
              stop_frame=250),
        Print(screen,
              SpeechBubble("A world of possibilities awaits you...", "L"),
              x=18, y=0,
              colour=curses.COLOR_CYAN,
              clear=True,
              start_frame=350,
              stop_frame=400),
        Print(screen, ImageFile("globe.gif"), 0,
              start_frame=400),
    ]
    scenes.append(Scene(effects, 600))

    effects = [
        Matrix(screen, stop_frame=200),
        Mirage(
            screen,
            FigletText("Asciimatics"),
            screen.height / 2 - 3,
            curses.COLOR_GREEN,
            start_frame=100,
            stop_frame=200),
        Wipe(screen, start_frame=150),
        Cycle(
            screen,
            FigletText("Asciimatics"),
            screen.height / 2 - 3,
            start_frame=200)
    ]
    scenes.append(Scene(effects, 250, clear=False))

    effects = [
        BannerText(
            screen,
            FigletText(
                "Reliving the 80s in glorious ASCII text...", font='slant'),
            screen.height / 2 - 3,
            curses.COLOR_GREEN)
    ]
    scenes.append(Scene(effects))

    effects = [
        Mirage(
            screen,
            FigletText("Conceived and"),
            screen.height,
            curses.COLOR_GREEN),
        Mirage(
            screen,
            FigletText("written by:"),
            screen.height + 8,
            curses.COLOR_GREEN),
        Mirage(
            screen,
            FigletText("Peter Brittain"),
            screen.height + 16,
            curses.COLOR_GREEN),
        Scroll(screen, 3)
    ]
    scenes.append(Scene(effects, (screen.height + 24) * 3))

    effects = [
        Cycle(
            screen,
            FigletText("ASCIIMATICS", font='big'),
            screen.height / 2 - 8),
        Cycle(
            screen,
            FigletText("ROCKS!", font='big'),
            screen.height / 2 + 3),
        Stars(screen, 200)
    ]
    scenes.append(Scene(effects, 200))

    screen.play(scenes)


if __name__ == "__main__":
    ascii_credits()