"""This module implements the listbox widget"""
from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, List, Optional, Tuple, Union
from asciimatics.strings import ColouredText
from asciimatics.widgets.utilities import _enforce_width_ext
from asciimatics.widgets.baselistbox import _BaseListBox
if TYPE_CHECKING:
    from asciimatics.parsers import Parser


class ListBox(_BaseListBox):
    """
    A ListBox is a widget that displays a list from which the user can select one option.
    """

    def __init__(self,
                 height: int,
                 options: List[Union[Tuple[str, int], Any]],
                 centre: bool = False,
                 label: Optional[str] = None,
                 name: Optional[str] = None,
                 add_scroll_bar: bool = False,
                 parser: Optional[Parser] = None,
                 on_change: Optional[Callable] = None,
                 on_select: Optional[Callable] = None,
                 validator: Optional[Callable] = None):
        """
        :param height: The required number of input lines for this ListBox.
        :param options: The options for each row in the widget.
        :param centre: Whether to centre the selected line in the list.
        :param label: An optional label for the widget.
        :param name: The name for the ListBox.
        :param parser: Optional parser to colour text.
        :param on_change: Optional function to call when selection changes.
        :param on_select: Optional function to call when the user actually selects an entry from
        :param validator: Optional function to validate selection for this widget.

        The `options` are a list of tuples, where the first value is the string to be displayed
        to the user and the second is an interval value to identify the entry to the program.
        For example:

            options=[("First option", 1), ("Second option", 2)]
        """
        super().__init__(height,
                         options,
                         label=label,
                         name=name,
                         parser=parser,
                         on_change=on_change,
                         on_select=on_select,
                         validator=validator)
        self._centre = centre
        self._add_scroll_bar = add_scroll_bar

    def update(self, frame_no: int):
        self._draw_label()

        # Prepare to calculate new visible limits if needed.
        height = self._h
        width = self._w - self._offset

        # Clear out the existing box content
        assert self._frame
        (colour, attr, background) = self._frame.palette["field"]
        for i in range(height):
            self._frame.canvas.print_at(" " * self.width,
                                        self._x + self._offset,
                                        self._y + i,
                                        colour,
                                        attr,
                                        background)

        # Don't bother with anything else if there are no options to render.
        if len(self._options) <= 0:
            return

        # Decide whether we need to show or hide the scroll bar and adjust width accordingly.
        if self._add_scroll_bar:
            self._add_or_remove_scrollbar(width, height, 0)
        if self._scroll_bar:
            width -= 1

        # Render visible portion of the text.
        y_offset = 0
        if self._centre:
            # Always make selected text the centre - not very compatible with scroll bars, but
            # there's not much else I can do here.
            self._start_line = self._line - (height // 2)
        start_line = self._start_line
        if self._start_line < 0:
            y_offset = -self._start_line
            start_line = 0
        for i, (text, _) in enumerate(self._options):
            if start_line <= i < start_line + height - y_offset:
                colour, attr, background = self._pick_colours("field", i == self._line)
                paint_text = text
                if self.string_len(str(text)) > width:
                    paint_text, truncated = _enforce_width_ext(
                        text[self._start_char:], width, self._frame.canvas.unicode_aware)
                    if truncated:
                        paint_text = paint_text[:-3] + "..."
                paint_text += " " * (width - self.string_len(str(paint_text)))
                self._frame.canvas.paint(
                    str(paint_text),
                    self._x + self._offset,
                    self._y + y_offset + i - start_line,
                    colour,
                    attr,
                    background,
                    colour_map=paint_text.colour_map if hasattr(paint_text, "colour_map") else None)

        # And finally draw any scroll bar.
        if self._scroll_bar:
            self._scroll_bar.update()

    def _find_option(self, search_value: str) -> Optional[int]:
        for text, value in self._options:
            if text.startswith(search_value):
                return value
        return None

    def _max_len(self) -> int:
        """
        Max length of any entry in the options.
        """
        return max(len(x[0]) for x in self._options)

    def _parse_option(self, option: str) -> ColouredText:
        """
        Parse a single option for ColouredText.

        :param option: the option to parse
        :returns: the option parsed and converted to ColouredText.
        """
        assert self._parser
        try:
            return ColouredText(option.raw_text, self._parser)  # type: ignore
        except AttributeError:
            return ColouredText(option, self._parser)

    @property
    def options(self):
        """
        The list of options available for user selection

        This is a list of tuples (<human readable string>, <internal value>).
        """
        return self._options

    @options.setter
    def options(self, new_value):
        # Set net list of options and then force an update to the current value to align with the new options.
        self._options = self._parse_options(new_value)
        self.value = self._value
