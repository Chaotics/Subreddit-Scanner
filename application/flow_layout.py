from PyQt5.QtWidgets import QLayout, QLayoutItem, QStyle, QSizePolicy, QPushButton
from PyQt5.QtCore import QRect, QSize, QPoint, Qt


class FlowLayout(QLayout):
    def __init__(self, margin=0, horizontal_spacing=-1, vertical_spacing=-1):
        super(FlowLayout, self).__init__()
        self._items = []
        self._horizontal_spacing = horizontal_spacing
        self._vertical_spacing = vertical_spacing
        self.setContentsMargins(margin, margin, margin, margin)

    def get_horizontal_spacing(self):
        return self._horizontal_spacing if self._horizontal_spacing >= 0 else self.smart_spacing(
            QStyle.PM_LayoutHorizontalSpacing)

    def get_vertical_spacing(self):
        return self._vertical_spacing if self._vertical_spacing >= 0 else self.smart_spacing(
            QStyle.PM_LayoutVerticalSpacing)

    def count(self):
        return len(self._items)

    def addItem(self, item: QLayoutItem):
        self._items.append(item)

    def itemAt(self, index: int):
        if 0 <= index < len(self._items):
            return self._items[index]

    def takeAt(self, index: int):
        if 0 <= index < len(self._items):
            return self._items.pop(index)

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self.do_layout(QRect(0, 0, width, 0), True)

    def setGeometry(self, rect: QRect):
        super(FlowLayout, self).setGeometry(rect)
        self.do_layout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())

        left, top, right, bottom = self.getContentsMargins()
        size += QSize(left + right, top + bottom)
        return size

    def do_layout(self, rect: QRect, test_only: bool):
        left, top, right, bottom = self.getContentsMargins()
        effective_rect = rect.adjusted(+left, +top, -right, -bottom)
        x = effective_rect.x()
        y = effective_rect.y()
        line_height = 0
        max_line_width = 0
        curr_line_width = 0
        num_of_lines = 0
        for item in self._items:
            widget = item.widget()
            space_x = self._horizontal_spacing
            if space_x == -1:
                space_x = widget.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal)
            space_y = self._vertical_spacing
            if space_y == -1:
                space_y = widget.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical)
            next_x = x + item.sizeHint().width() + space_x

            if next_x - space_x > effective_rect.right() and line_height > 0:
                x = effective_rect.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0
                max_line_width = max(curr_line_width, max_line_width)
                curr_line_width = 0
                num_of_lines += 1

            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
            curr_line_width += item.sizeHint().width()
            x = next_x
            line_height = max(line_height, item.sizeHint().height())
        max_line_width = max(curr_line_width, max_line_width)
        if not test_only and rect.width() != 0:
            x_offset = ((rect.width() - left - right) - max_line_width - (self.get_horizontal_spacing() * (len(self._items) - 1))) / 2
            y_offset = ((rect.height() - top - bottom) - (num_of_lines * (line_height + self.get_vertical_spacing()) - self.get_vertical_spacing())) / 2
            for item in self._items:
                widget = item.widget()
                x = widget.x() + x_offset
                y = widget.y() + y_offset
                item.setGeometry(QRect(QPoint(int(x), int(y)), item.sizeHint()))
        return y + line_height - rect.y() + bottom

    def smart_spacing(self, pm):
        parent = self.parent()
        if parent is None:
            return -1
        elif parent.isWidgetType():
            return parent.style().pixelMetric(pm, None, parent)
        else:
            return parent.spacing()
