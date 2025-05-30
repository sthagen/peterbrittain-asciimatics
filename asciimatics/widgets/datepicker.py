"""This module defines a datepicker widget"""
from __future__ import annotations
from datetime import date, datetime
from typing import Callable, Optional
from asciimatics.exceptions import InvalidFields
from asciimatics.widgets.basepicker import _BasePicker
from asciimatics.widgets.label import Label
from asciimatics.widgets.layout import Layout
from asciimatics.widgets.listbox import ListBox
from asciimatics.widgets.temppopup import _TempPopup


class _DatePickerPopup(_TempPopup):
    """
    An internal Frame for editing the currently selected date.
    """

    def __init__(self, parent: "DatePicker", year_range: Optional[range] = None):
        """
        :param parent: The widget that spawned this pop-up.
        :param year_range: Optional range to limit the year selection to.
        """
        # Create the lists for each entry.
        now = parent.value if parent.value else date.today()
        if year_range is None:
            year_range = range(now.year - 50, now.year + 50)
        self._days = ListBox(3, [(f"{x:02}", x) for x in range(1, 32)],
                             centre=True,
                             validator=self._check_date)
        self._months = ListBox(3, [(now.replace(day=1, month=x).strftime("%b"), x) for x in range(1, 13)],
                               centre=True,
                               on_change=self._refresh_day)
        self._years = ListBox(3, [(f"{x:04}", x) for x in year_range],
                              centre=True,
                              on_change=self._refresh_day)

        # Construct the Frame
        assert parent.frame
        location = parent.get_location()
        super().__init__(parent.frame.screen, parent, location[0] - 1, location[1] - 2, 13, 5)

        # Build the widget to display the time selection.
        layout = Layout([2, 1, 3, 1, 4], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._days, 0)
        layout.add_widget(Label("\n/", height=3), 1)
        layout.add_widget(self._months, 2)
        layout.add_widget(Label("\n/", height=3), 3)
        layout.add_widget(self._years, 4)
        self.fix()

        # Set up the correct time.
        self._years.value = parent.value.year
        self._months.value = parent.value.month
        self._days.value = parent.value.day

    def _check_date(self, value: int):
        try:
            date(self._years.value, self._months.value, value)
            return True
        except (TypeError, ValueError):
            return False

    def _refresh_day(self):
        self._days.value = self._days.value

    def _on_close(self, cancelled: bool):
        try:
            if not cancelled:
                self._parent.value = self._parent.value.replace(day=self._days.value,
                                                                month=self._months.value,
                                                                year=self._years.value)
        except ValueError as e:
            raise InvalidFields([self._days.value]) from e


class DatePicker(_BasePicker):
    """
    A DatePicker widget allows you to pick a date from a compact, temporary, pop-up Frame.
    """

    __slots__ = ["_year_range"]

    def __init__(self,
                 label: Optional[str] = None,
                 name: Optional[str] = None,
                 year_range: Optional[range] = None,
                 on_change: Optional[Callable] = None,
                 **kwargs):
        """
        :param label: An optional label for the widget.
        :param name: The name for the widget.
        :param on_change: Optional function to call when the selected time changes.

        Also see the common keyword arguments in :py:obj:`.Widget`.
        """
        super().__init__(_DatePickerPopup, label=label, name=name, on_change=on_change, **kwargs)
        self._value = datetime.now().date()
        self._year_range = year_range

    def update(self, frame_no: int):
        self._draw_label()

        # This widget only ever needs display the current selection - the separate Frame does all
        # the clever stuff when it has the focus.
        assert self._frame
        (colour, attr, background) = self._pick_colours("edit_text")
        self._frame.canvas.print_at(self._value.strftime("%d/%b/%Y"),
                                    self._x + self._offset,
                                    self._y,
                                    colour,
                                    attr,
                                    background)
