import sys
from PySide6.QtCore import (
    QPoint, QRect, Slot
)
from PySide6.QtGui import (
    QPixmap, QTransform, QAction, QColor
)
from PySide6.QtWidgets import (
    QWidget, QMainWindow, QApplication, QHBoxLayout, QSplitter, QTableWidget, 
    QTableWidgetItem, QHeaderView, QGraphicsView, QGraphicsScene, QMenuBar, 
    QFileDialog
    )

class Widget(QWidget):
    def __init__(self):
        super().__init__()

        # table for equations
        self.table = QTableWidget(2, 1, self)
        self.table.setHorizontalHeaderLabels(["Equation"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # graphics scene
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QColor('blue')) # coloured to show where scene is
        self.img = None

        # graphics view
        self.graph = QGraphicsView(self.scene)

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

    # unlikely to be part of final implementation, 
    # temporary for demo purposes
    def set_image(self, image: QPixmap):
        rect = self.graph.viewport().geometry()
        # scaling currently still respects image aspect ratio
        image = image.scaledToHeight(rect.height())
        image = image.scaledToWidth(rect.width())

        if len(self.scene.items()) != 0:
            self.scene.removeItem(self.scene.items()[0])
        self.img = image
        self.scene.addPixmap(self.img)

class MainWindow(QMainWindow):
    def __init__(self, widget):
        super().__init__()
        self.setWindowTitle("Name")

        # creating menu actions
        openAction = QAction("Open...", self)
        openAction.triggered.connect(self.open_file)

        saveAction = QAction("Save", self)
        saveAction.triggered.connect(self.save_file)

        # creating menu bar
        menu = self.menuBar()

        fileMenu = menu.addMenu("File")
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)

        self.mainContent = widget
        self.setCentralWidget(widget)

    # TODO: Implement file saving and loading
    @Slot()
    def open_file(self):
        # currently dummy implementation
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter("Images (*.png, *.jpg)")
        # dialog.setDirectory()
        fileName = ""
        if dialog.exec():
            fileName = dialog.selectedFiles()[0]

        self.mainContent.set_image(QPixmap(fileName))

    @Slot()
    def save_file(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    window = MainWindow(widget)
    window.resize(1000,600)
    window.show()

    sys.exit(app.exec())