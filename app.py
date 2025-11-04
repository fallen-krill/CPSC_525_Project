import sys
from PySide6.QtCore import (
    QPoint, QRect, Slot
)
from PySide6.QtGui import (
    QPixmap, QTransform
)
from PySide6.QtWidgets import (
    QWidget, QMainWindow, QApplication, QHBoxLayout, QSplitter, QTableWidget, 
    QTableWidgetItem, QHeaderView, QGraphicsView, QGraphicsScene
    )

class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.table = QTableWidget(2, 1, self)
        self.table.setHorizontalHeaderLabels(["Equation"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.scene = QGraphicsScene()
        self.img = QPixmap("image.JPG")

        self.graph = QGraphicsView(self.scene)
        rect = self.graph.viewport().geometry()
        self.img = self.img.scaledToHeight(rect.height())
        self.img = self.img.scaledToWidth(rect.width())
        self.scene.addPixmap(self.img)

        # splitter layout
        self.splitter = QSplitter(self)
        self.splitter.addWidget(self.table)
        self.splitter.addWidget(self.graph)
        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, False)
        self.splitter.setSizes([100,300])

        # overall layout
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.splitter)

        self.table.itemChanged.connect(self.add_equation)

    @Slot()
    def add_equation(self, item: QTableWidgetItem):
        last_row = self.table.rowCount() - 1
        if (item.row() == last_row):
            self.table.insertRow(last_row + 1)

class MainWindow(QMainWindow):
    def __init__(self, widget):
        super().__init__()
        self.setWindowTitle("Name")
        self.setCentralWidget(widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    window = MainWindow(widget)
    window.resize(1000,600)
    window.show()

    sys.exit(app.exec())