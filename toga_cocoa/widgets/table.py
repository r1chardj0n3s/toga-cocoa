from ..libs import *
from .base import Widget


class TogaTable(NSTableView):

    # TableDataSource methods
    @objc_method
    def numberOfRowsInTableView_(self, table) -> int:
        return len(self.__dict__['interface']._data)

    @objc_method
    def tableView_objectValueForTableColumn_row_(self, table, column, row: int):
        column_index = int(column.identifier)
        return self.__dict__['interface']._data[row][column_index]

    # TableDelegate methods
    @objc_method
    def tableViewSelectionDidChange_(self, notification) -> None:
        print ("selection changed")


class Table(Widget):
    def __init__(self, headings, style=None):
        super(Table, self).__init__(style=style)
        self.headings = headings

        self._data = []

        self.startup()

    def startup(self):
        # Create a table view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self._impl = NSScrollView.alloc().init()
        self._impl.setHasVerticalScroller_(True)
        self._impl.setHasHorizontalScroller_(True)
        self._impl.setAutohidesScrollers_(False)
        self._impl.setBorderType_(NSBezelBorder)

        # Disable all autolayout functionality on the outer widget
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

        self._table = TogaTable.alloc().init()
        self._table.__dict__['interface'] = self
        self._table.setColumnAutoresizingStyle_(NSTableViewUniformColumnAutoresizingStyle)

        # Use autolayout for the inner widget.
        self._table.setTranslatesAutoresizingMaskIntoConstraints_(True)

        # Create columns for the table
        self._columns = [
            NSTableColumn.alloc().initWithIdentifier_('%d' % i)
            for i, heading in enumerate(self.headings)
        ]

        for heading, column in zip(self.headings, self._columns):
            self._table.addTableColumn_(column)
            cell = column.dataCell
            cell.setEditable_(False)
            cell.setSelectable_(False)
            column.headerCell.stringValue = heading

        self._table.setDelegate_(self._table)
        self._table.setDataSource_(self._table)

        # Embed the table view in the scroll view
        self._impl.setDocumentView_(self._table)

    def insert(self, index, *data):
        if len(data) != len(self.headings):
            raise Exception('Data size does not match number of headings')

        if index is None:
            self._data.append(data)
        else:
            self._data.insert(index, data)
