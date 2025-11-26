# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

# from https://doc.qt.io/qtforpython-6/examples/example_widgets_widgetsgallery.html#example-widgets-widgetsgallery
# will not be included in final submission
from __future__ import annotations

"""PySide6 port of the widgets/gallery example from Qt v5.15"""

import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from demowidget import WidgetGallery

freak = None

class freakshow():
    def open(self):
        self.gallery = WidgetGallery()
        self.gallery.show()

def cool():
    global freak
    freak = freakshow()
    freak.open()

if __name__ == "__main__":
    hi = QApplication(sys.argv)
    #freak = freakshow()
    #freak.open()
    cool()
    sys.exit(hi.exec())