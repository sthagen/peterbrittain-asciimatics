#!/usr/bin/env python3

from __future__ import division
import sys
from pyfiglet import Figlet

from asciimatics.effects import Scroll, Mirage, Wipe, Cycle, Matrix, \
    BannerText, Stars, Print
from asciimatics.particles import DropScreen
from asciimatics.renderers import FigletText, SpeechBubble, Rainbow, Fire
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError


def _credits(screen):
    scenes = []

    text = Figlet(font="banner", width=200).renderText("ASCIIMATICS")
    width = max([len(x) for x in text.split("\n")])

    effects = [
        Print(screen,
              Fire(screen.height, 80, text, 0.4, 40, screen.colours),
              0,
              speed=1,
              transparent=False),
        Print(screen,
              FigletText("ASCIIMATICS", "banner"),
              screen.height - 9, x=(screen.width - width) // 2 + 1,
              colour=Screen.COLOUR_BLACK,
              bg=Screen.COLOUR_BLACK,
              speed=1),
        Print(screen,
              FigletText("ASCIIMATICS", "banner"),
              screen.height - 9,
              colour=Screen.COLOUR_WHITE,
              bg=Screen.COLOUR_WHITE,
              speed=1),
    ]
    scenes.append(Scene(effects, 100))

    effects = [
        Matrix(screen, stop_frame=200),
        Mirage(
            screen,
            FigletText("Asciimatics"),
            screen.height // 2 - 3,
            Screen.COLOUR_GREEN,
            start_frame=100,
            stop_frame=200),
        Wipe(screen, start_frame=150),
        Cycle(
            screen,
            FigletText("Asciimatics"),
            screen.height // 2 - 3,
            start_frame=200)
    ]
    scenes.append(Scene(effects, 250, clear=False))

    effects = [
        BannerText(
            screen,
            Rainbow(screen, FigletText(
                "Reliving the 80s in glorious ASCII text...", font='slant')),
            screen.height // 2 - 3,
            Screen.COLOUR_GREEN)
    ]
    scenes.append(Scene(effects))

    effects = [
        Scroll(screen, 3),
        Mirage(
            screen,
            FigletText("Conceived and"),
            screen.height,
            Screen.COLOUR_GREEN),
        Mirage(
            screen,
            FigletText("written by:"),
            screen.height + 8,
            Screen.COLOUR_GREEN),
        Mirage(
            screen,
            FigletText("Peter Brittain"),
            screen.height + 16,
            Screen.COLOUR_GREEN)
    ]
    scenes.append(Scene(effects, (screen.height + 24) * 3))

    colours = [Screen.COLOUR_RED, Screen.COLOUR_GREEN,]
    contributors = [
        "Cory Benfield",
        "Bryce Guinta",
        "Aman Orazaev",
        "Daniel Kerr",
        "Dylan Janeke",
        "ianadeem",
        "Scott Mudge",
        "Luke Murphy",
        "mronkain",
        "Dougal Sutherland",
        "Kirtan Sakariya",
        "Jesse Lieberg",
        "Erik Doffagne",
        "Noah Ginsburg",
        "Davidy22",
        "Christopher Trudeau",
    ]

    effects = [
        Scroll(screen, 3),
        Mirage(
            screen,
            FigletText("With help from:"),
            screen.height,
            Screen.COLOUR_GREEN,
        )
    ]

    pos = 8
    for i, name in enumerate(contributors):
        effects.append(
            Mirage(
                screen,
                FigletText(name),
                screen.height + pos,
                colours[i % len(colours)],
            )
        )

        pos += 8
    scenes.append(Scene(effects, (screen.height + pos) * 3))

    effects = [
        Cycle(
            screen,
            FigletText("ASCIIMATICS", font='big'),
            screen.height // 2 - 8,
            stop_frame=100),
        Cycle(
            screen,
            FigletText("ROCKS!", font='big'),
            screen.height // 2 + 3,
            stop_frame=100),
        Stars(screen, (screen.width + screen.height) // 2, stop_frame=100),
        DropScreen(screen, 200, start_frame=100)
    ]
    scenes.append(Scene(effects, 300))

    effects = [
        Print(screen,
              SpeechBubble("Press 'X' to exit."), screen.height // 2 - 1, attr=Screen.A_BOLD)
    ]
    scenes.append(Scene(effects, -1))

    screen.play(scenes, stop_on_resize=True)


if __name__ == "__main__":
    while True:
        try:
            Screen.wrapper(_credits)
            sys.exit(0)
        except ResizeScreenError:
            pass
