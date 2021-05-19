
"""This is the baseclass for list box types"""
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from builtins import chr
from datetime import datetime, timedelta
from abc import ABCMeta, abstractmethod, abstractproperty
from future.utils import with_metaclass
from asciimatics.event import KeyboardEvent, MouseEvent
from asciimatics.screen import Screen
from asciimatics.widgets.widget import Widget
from asciimatics.widgets.scrollbar import _ScrollBar
from re import match as re_match
import os
import unicodedata
from asciimatics.widgets.utilities import _enforce_width
from future.moves.itertools import zip_longest
from asciimatics.utilities import readable_timestamp, readable_mem

class _CustomBaseListBox(with_metaclass(ABCMeta, Widget)):
    """
    An Internal class to contain common function between list box types.
    """

    __slots__ = ["_options", "_titles", "_label", "_line", "_start_line", "_required_height", "_on_change",
                 "_on_select", "_validator", "_search", "_last_search", "_scroll_bar", "_parser"]

    def __init__(self, height, options, titles=None, label=None, name=None, parser=None,
                 on_change=None, on_select=None, validator=None):
        """
        :param height: The required number of input lines for this widget.
        :param options: The options for each row in the widget.
        :param label: An optional label for the widget.
        :param name: The name for the widget.
        :param parser: Optional parser to colour text.
        :param on_change: Optional function to call when selection changes.
        :param on_select: Optional function to call when the user actually selects an entry from
            this list - e.g. by double-clicking or pressing Enter.
        :param validator: Optional function to validate selection for this widget.
        """
        super(_CustomBaseListBox, self).__init__(name)
        self._titles = titles
        self._label = label
        self._parser = parser
        self._options = self._parse_options(options)
        self._line = 0
        self._value = None
        self._start_line = 0
        self._required_height = height
        self._on_change = on_change
        self._on_select = on_select
        self._validator = validator
        self._search = ""
        self._last_search = datetime.now()
        self._scroll_bar = None

    def reset(self):
        pass

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if len(self._options) > 0 and event.key_code in [ord("k"), Screen.KEY_UP]:
                # Move up one line in text - use value to trigger on_select.
                self._line = max(0, self._line - 1)
                self.value = self._options[self._line][1]
            elif len(self._options) > 0 and event.key_code in [ord("j"), Screen.KEY_DOWN]:
                # Move down one line in text - use value to trigger on_select.
                self._line = min(len(self._options) - 1, self._line + 1)
                self.value = self._options[self._line][1]
            elif len(self._options) > 0 and event.key_code == Screen.KEY_PAGE_UP:
                # Move up one page.
                self._line = max(0, self._line - self._h + (1 if self._titles else 0))
                self.value = self._options[self._line][1]
            elif len(self._options) > 0 and event.key_code == Screen.KEY_PAGE_DOWN:
                # Move down one page.
                self._line = min(
                    len(self._options) - 1, self._line + self._h - (1 if self._titles else 0))
                self.value = self._options[self._line][1]
            elif event.key_code in [Screen.ctrl("m"), Screen.ctrl("j"), ord("l")]:
                # Fire select callback.
                if self._on_select:
                    self._on_select()
            elif event.key_code > 0:
                # Treat any other normal press as a search
                now = datetime.now()
                if now - self._last_search >= timedelta(seconds=1):
                    self._search = ""
                self._search += chr(event.key_code)
                self._last_search = now

                # If we find a new match for the search string, update the list selection
                new_value = self._find_option(self._search)
                if new_value is not None:
                    self.value = new_value
            else:
                return event
        elif isinstance(event, MouseEvent):
            # Mouse event - adjust for scroll bar as needed.
            if event.buttons != 0:
                # Check for normal widget.
                if (len(self._options) > 0 and
                        self.is_mouse_over(event, include_label=False,
                                           width_modifier=1 if self._scroll_bar else 0)):
                    # Figure out selected line
                    new_line = event.y - self._y + self._start_line
                    if self._titles:
                        new_line -= 1
                    new_line = min(new_line, len(self._options) - 1)

                    # Update selection and fire select callback if needed.
                    if new_line >= 0:
                        self._line = new_line
                        self.value = self._options[self._line][1]
                        if event.buttons & MouseEvent.DOUBLE_CLICK != 0 and self._on_select:
                            self._on_select()
                    return None

                # Check for scroll bar interactions:
                if self._scroll_bar:
                    if self._scroll_bar.process_event(event):
                        return None

            # Ignore other mouse events.
            return event
        else:
            # Ignore other events
            return event

        # If we got here, we processed the event - swallow it.
        return None

    def _add_or_remove_scrollbar(self, width, height, dy):
        """
        Add or remove a scrollbar from this listbox based on height and available options.

        :param width: Width of the Listbox
        :param height: Height of the Listbox.
        :param dy: Vertical offset from top of widget.
        """
        if self._scroll_bar is None and len(self._options) > height:
            self._scroll_bar = _ScrollBar(
                self._frame.canvas, self._frame.palette, self._x + width - 1, self._y + dy,
                height, self._get_pos, self._set_pos)
        elif self._scroll_bar is not None and len(self._options) <= height:
            self._scroll_bar = None

    def _get_pos(self):
        """
        Get current position for scroll bar.
        """
        if self._h >= len(self._options):
            return 0
        return self._start_line / (len(self._options) - self._h)

    def _set_pos(self, pos):
        """
        Set current position for scroll bar.
        """
        if self._h < len(self._options):
            pos *= len(self._options) - self._h
            pos = int(round(max(0, pos), 0))
            self._start_line = pos

    @abstractmethod
    def _find_option(self, search_value):
        """
        Internal function called by the BaseListBox to do a text search on user input.

        :param search_value: The string value to search for in the list.
        :return: The value of the matching option (or None if nothing matches).
        """

    def required_height(self, offset, width):
        return self._required_height

    @property
    def start_line(self):
        """
        The line that will be drawn at the top of the visible section of this list.
        """
        return self._start_line

    @start_line.setter
    def start_line(self, new_value):
        if 0 <= new_value < len(self._options):
            self._start_line = new_value

    @property
    def value(self):
        """
        The current value for this list box.
        """
        return self._value

    @value.setter
    def value(self, new_value):
        # Only trigger change notification after we've changed selection
        old_value = self._value
        self._value = new_value
        for i, [_, value] in enumerate(self._options):
            if value == new_value:
                self._line = i
                break
        else:
            # No matching value - pick a default.
            if len(self._options) > 0:
                self._line = 0
                self._value = self._options[self._line][1]
            else:
                self._line = -1
                self._value = None
        if self._validator:
            self._is_valid = self._validator(self._value)
        if old_value != self._value and self._on_change:
            self._on_change()

        # Fix up the start line now that we've explicitly set a new value.
        self._start_line = max(
            0, max(self._line - self._h + 1, min(self._start_line, self._line)))

    def _parse_options(self, options):
        """
        Parse a the options list for ColouredText.

        :param options: the options list to parse
        :returns: the options list parsed and converted to ColouredText as needed.
        """
        if self._parser:
            parsed_value = []
            for option in options:
                parsed_value.append((self._parse_option(option[0]), option[1]))
            return parsed_value
        return options

    @abstractmethod
    def _parse_option(self, option):
        """
        Parse a single option for ColouredText.

        :param option: the option to parse
        :returns: the option parsed and converted to ColouredText.
        """

    @abstractproperty
    def options(self):
        """
        The list of options available for user selection.
        """

class CustomMultiColumnListBox(_CustomBaseListBox):
    """
    A MultiColumnListBox is a widget for displaying tabular data.

    It displays a list of related data in columns, from which the user can select a line.
    """

    def __init__(self, height, columns, options, titles=None, label=None,
                 name=None, add_scroll_bar=False, parser=None, on_change=None,
                 on_select=None, space_delimiter=' '):
        """
        :param height: The required number of input lines for this ListBox.
        :param columns: A list of widths and alignments for each column.
        :param options: The options for each row in the widget.
        :param titles: Optional list of titles for each column.  Must match the length of
            `columns`.
        :param label: An optional label for the widget.
        :param name: The name for the ListBox.
        :param add_scroll_bar: Whether to add optional scrollbar for large lists.
        :param parser: Optional parser to colour text.
        :param on_change: Optional function to call when selection changes.
        :param on_select: Optional function to call when the user actually selects an entry from
        :param space_delimiter: Optional parameter to define the delimiter between columns.
            The default value is blank space.

        The `columns` parameter is a list of integers or strings.  If it is an integer, this is
        the absolute width of the column in characters.  If it is a string, it must be of the
        format "[<align>]<width>[%]" where:

        * <align> is the alignment string ("<" = left, ">" = right, "^" = centre)
        * <width> is the width in characters
        * % is an optional qualifier that says the number is a percentage of the width of the
          widget.

        Column widths need to encompass any space required between columns, so for example, if
        your column is 5 characters, allow 6 for an extra space at the end.  It is not possible
        to do this when you have a right-justified column next to a left-justified column, so
        this widget will automatically space them for you.

        An integer value of 0 is interpreted to be use whatever space is left available after the
        rest of the columns have been calculated.  There must be only one of these columns.

        The number of columns is for this widget is determined from the number of entries in the
        `columns` parameter.  The `options` list is then a list of tuples of the form
        ([val1, val2, ... , valn], index).  For example, this data provides 2 rows for a 3 column
        widget:

            options=[(["One", "row", "here"], 1), (["Second", "row", "here"], 2)]

        The options list may be None and then can be set later using the `options` property on
        this widget.
        """
        super(CustomMultiColumnListBox, self).__init__(
            height, options, titles=titles, label=label, name=name, parser=parser,
            on_change=on_change, on_select=on_select)
        self._columns = []
        self._align = []
        self._spacing = []
        self._add_scroll_bar = add_scroll_bar
        self._space_delimiter = space_delimiter
        for i, column in enumerate(columns):
            if isinstance(column, int):
                self._columns.append(column)
                self._align.append("<")
            else:
                match = re_match(r"([<>^]?)(\d+)([%]?)", column)
                self._columns.append(float(match.group(2)) / 100
                                     if match.group(3) else int(match.group(2)))
                self._align.append(match.group(1) if match.group(1) else "<")
            if space_delimiter == ' ':
                self._spacing.append(1 if i > 0 and self._align[i] == "<" and
                                     self._align[i - 1] == ">" else 0)
            else:
                self._spacing.append(1 if i > 0 else 0)

    def _get_width(self, width, max_width):
        """
        Helper function to figure out the actual column width from the various options.

        :param width: The size of column requested
        :param max_width: The maximum width allowed for this widget.
        :return: the integer width of the column in characters
        """
        if isinstance(width, float):
            return int(max_width * width)
        if width == 0:
            width = (max_width - sum(self._spacing) -
                     sum([self._get_width(x, max_width) for x in self._columns if x != 0]))
        return width

    def _print_cell(self, space, text, align, width, x, y, foreground, attr, background):
        # Sort out spacing first.
        if space:
            self._frame.canvas.print_at(self._space_delimiter * space, x, y, foreground, attr, background)

        # Now align text, taking into account double space glyphs.
        paint_text = _enforce_width(text, width, self._frame.canvas.unicode_aware)
        text_size = self.string_len(str(paint_text))
        if text_size < width:
            # Default does no alignment or padding.
            buffer_1 = buffer_2 = ""
            if align == "<":
                buffer_2 = " " * (width - text_size)
            elif align == ">":
                buffer_1 = " " * (width - text_size)
            elif align == "^":
                start_len = int((width - text_size) / 2)
                buffer_1 = " " * start_len
                buffer_2 = " " * (width - text_size - start_len)
            paint_text = paint_text.join([buffer_1, buffer_2])
        self._frame.canvas.paint(
            str(paint_text), x + space, y, foreground, attr, background,
            colour_map=paint_text.colour_map if hasattr(paint_text, "colour_map") else None)

    def update(self, frame_no):
        self._draw_label()

        # Calculate new visible limits if needed.
        height = self._h
        width = self._w
        delta_y = 0

        # Clear out the existing box content
        (colour, attr, background) = self._frame.palette["field"]
        for i in range(height):
            self._frame.canvas.print_at(
                " " * width,
                self._x + self._offset,
                self._y + i + delta_y,
                colour, attr, background)

        # Allow space for titles if needed.
        if self._titles:
            delta_y += 1
            height -= 1

        # Decide whether we need to show or hide the scroll bar and adjust width accordingly.
        if self._add_scroll_bar:
            self._add_or_remove_scrollbar(width, height, delta_y)
        if self._scroll_bar:
            width -= 1

        # Now draw the titles if needed.
        if self._titles:
            row_dx = 0
            colour, attr, background = self._frame.palette["title"]
            for i, [title, align, space] in enumerate(
                    zip(self._titles, self._align, self._spacing)):
                cell_width = self._get_width(self._columns[i], width)
                self._print_cell(
                    space, title, align, cell_width, self._x + self._offset + row_dx, self._y,
                    colour, attr, background)
                row_dx += cell_width + space

        # Don't bother with anything else if there are no options to render.
        if len(self._options) <= 0:
            return

        # Render visible portion of the text.
        self._start_line = max(0, max(self._line - height + 1,
                                      min(self._start_line, self._line)))
        for i, [row, _] in enumerate(self._options):
            if self._start_line <= i < self._start_line + height:
                colour, attr, background = self._pick_colours("field", i == self._line)
                row_dx = 0
                # Try to handle badly formatted data, where row lists don't
                # match the expected number of columns.
                for text, cell_width, align, space in zip_longest(
                        row, self._columns, self._align, self._spacing, fillvalue=""):
                    if cell_width == "":
                        break
                    cell_width = self._get_width(cell_width, width)
                    if len(text) > cell_width:
                        text = text[:cell_width - 3] + "..."
                    self._print_cell(
                        space, text, align, cell_width,
                        self._x + self._offset + row_dx,
                        self._y + i + delta_y - self._start_line,
                        colour, attr, background)
                    row_dx += cell_width + space

        # And finally draw any scroll bar.
        if self._scroll_bar:
            self._scroll_bar.update()

    def _find_option(self, search_value):
        for row, value in self._options:
            # TODO: Should this be aware of a sort column?
            if row[0].startswith(search_value):
                return value
        return None

    def _parse_option(self, option):
        """
        Parse a single option for ColouredText.

        :param option: the option to parse
        :returns: the option parsed and converted to ColouredText.
        """
        option_items = []
        for item in option:
            try:
                value = ColouredText(item.raw_text, self._parser)
            except AttributeError:
                value = ColouredText(item, self._parser)
            option_items.append(value)
        return option_items

    @property
    def options(self):
        """
        The list of options available for user selection

        This is a list of tuples ([<col 1 string>, ..., <col n string>], <internal value>).
        """
        return self._options

    @options.setter
    def options(self, new_value):
        # Set net list of options and then force an update to the current value to align with the new options.
        self._options = self._parse_options(new_value)
        self.value = self._value

class CustomFileBrowser(CustomMultiColumnListBox):
    """
    A FileBrowser is a widget for finding a file on the local disk.
    """

    def __init__(self, height, root, name=None, on_select=None, on_change=None, file_filter=None):
        r"""
        :param height: The desired height for this widget.
        :param root: The starting root directory to display in the widget.
        :param name: The name of this widget.
        :param on_select: Optional function that gets called when user selects a file (by pressing
            enter or double-clicking).
        :param on_change: Optional function that gets called on any movement of the selection.
        :param file_filter: Optional RegEx string that can be passed in to filter the files to be displayed.

        Most people will want to use a filter to finx files with a particular extension.  In this case,
        you must use a regex that matches to the end of the line - e.g. use ".*\.txt$" to find files ending
        with ".txt".  This ensures that you don't accidentally pick up files containing the filter.
        """
        super(CustomFileBrowser, self).__init__(
            height,
            [0, ">8", ">14"],
            [],
            titles=["Filename", "Size", "Last modified"],
            name=name,
            on_select=self._on_selection,
            on_change=on_change)

        # Remember the on_select handler for external notification.  This allows us to wrap the
        # normal on_select notification with a function that will open new sub-directories as
        # needed.
        self._external_notification = on_select
        self._root = root
        self._in_update = False
        self._initialized = False
        self._file_filter = None if file_filter is None else re_compile(file_filter)

    def update(self, frame_no):
        # Defer initial population until we first display the widget in order to avoid race
        # conditions in the Frame that may be using this widget.
        if not self._initialized:
            self._populate_list(self._root)
            self._initialized = True
        super(CustomFileBrowser, self).update(frame_no)

    def _on_selection(self):
        """
        Internal function to handle directory traversal or bubble notifications up to user of the
        Widget as needed.
        """
        if self.value and os.path.isdir(self.value):
            self._populate_list(self.value)
        elif self._external_notification:
            self._external_notification()

    def clone(self, new_widget):
        # Copy the data into the new widget.  Notes:
        # 1) I don't really want to expose these methods, so am living with the protected access.
        # 2) I need to populate the list and then assign the values to ensure that we get the
        #    right selection on re-sizing.
        # pylint: disable=protected-access
        new_widget._populate_list(self._root)
        new_widget._start_line = self._start_line
        new_widget._root = self._root
        new_widget.value = self.value

    def _populate_list(self, value):
        """
        Populate the current multi-column list with the contents of the selected directory.

        :param value: The new value to use.
        """
        # Nothing to do if the value is rubbish.
        if value is None:
            return

        # Stop any recursion - no more returns from here to end of fn please!
        if self._in_update:
            return
        self._in_update = True

        # We need to update the tree view.
        self._root = os.path.abspath(value if os.path.isdir(value) else os.path.dirname(value))

        # The absolute expansion of "/" or "\" is the root of the disk, so is a cross-platform
        # way of spotting when to insert ".." or not.
        tree_view = []
        if len(self._root) > len(os.path.abspath(os.sep)):
            tree_view.append((["|-+ .."], os.path.abspath(os.path.join(self._root, ".."))))

        tree_dirs = []
        tree_files = []
        try:
            files = os.listdir(self._root)
        except OSError:
            # Can fail on Windows due to access permissions
            files = []
        for my_file in files:
            full_path = os.path.join(self._root, my_file)
            try:
                details = os.lstat(full_path)
            except OSError:
                # Can happen on Windows due to access permissions
                details = namedtuple("stat_type", "st_size st_mtime")
                details.st_size = 0
                details.st_mtime = 0
            name = "|-- {}".format(my_file)
            tree = tree_files
            if os.path.isdir(full_path):
                tree = tree_dirs
                if os.path.islink(full_path):
                    # Show links separately for directories
                    real_path = os.path.realpath(full_path)
                    name = "|-+ {} -> {}".format(my_file, real_path)
                else:
                    name = "|-+ {}".format(my_file)
            elif self._file_filter and not self._file_filter.match(my_file):
                # Skip files that don't match the filter (if present)
                continue
            elif os.path.islink(full_path):
                # Check if link target exists and if it does, show statistics of the
                # linked file, otherwise just display the link
                try:
                    real_path = os.path.realpath(full_path)
                except OSError:
                    # Can fail on Linux prof file system.
                    real_path = None
                if real_path and os.path.exists(real_path):
                    details = os.stat(real_path)
                    name = "|-- {} -> {}".format(my_file, real_path)
                else:
                    # Both broken directory and file links fall to this case.
                    # Actually using the files will cause a FileNotFound exception
                    name = "|-- {} -> {}".format(my_file, real_path)

            # Normalize names for MacOS and then add to the list.
            tree.append(([unicodedata.normalize("NFC", name),
                          readable_mem(details.st_size),
                          readable_timestamp(details.st_mtime)], full_path))

        tree_view.extend(sorted(tree_dirs))
        tree_view.extend(sorted(tree_files))

        self.options = tree_view
        self._titles[0] = self._root

        # We're out of the function - unset recursion flag.
        self._in_update = False
