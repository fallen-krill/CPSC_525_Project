import math
import sys
from PySide6.QtCore import (
    QPoint, QPointF, QRect, Slot, Qt, QSize
)
from PySide6.QtGui import (
    QPixmap, QTransform, QAction, QColor
)
from PySide6.QtWidgets import (
    QWidget, QMainWindow, QApplication, QHBoxLayout, QVBoxLayout, QSplitter, 
    QTableWidget, QTableWidgetItem, QHeaderView, QGraphicsView, QGraphicsScene, 
    QMenuBar, QFileDialog, QTabWidget, QDialog, QLabel, QLineEdit, QDialogButtonBox,
    QListWidget, QListWidgetItem, QPushButton, QStyledItemDelegate
    )

from PySide6.QtCharts import (
    QChart, QChartView, QLineSeries
    )

from chart import (
    Chart, ChartView
    )
from function_tree import (
    Function_tree
)

class PageRenameDialog(QDialog):
    def __init__(self, name: str):
        super().__init__(modal=True)
        self.text = QLabel("Edit page name.", self)
        self.text_input = QLineEdit(self, text=name)
        self.buttons = QDialogButtonBox(Qt.Orientation.Horizontal, self)
        self.buttons.addButton("Ok", QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttons.addButton("Cancel", QDialogButtonBox.ButtonRole.RejectRole)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.text_input)
        self.layout.addWidget(self.buttons)

class EquationEditorWidget(QWidget):
    def __init__(self, chart):
        super().__init__()

        # table for equations
        self.table = QTableWidget(1, 1, self)
        self.table.setHorizontalHeaderLabels(["Equation"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_layout = QVBoxLayout()
        self.table_layout.addWidget(self.table)

        # buttons for adding/removing equations
        self.add_equation = QPushButton("+", self)
        self.add_equation.setToolTip("Add Equation")
        self.remove_equation = QPushButton("-", self)
        self.remove_equation.setToolTip("Remove Selected Equation")
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.add_equation)
        self.button_layout.addWidget(self.remove_equation)

        # editor layout
        self.layout = QVBoxLayout(self)
        self.layout.addLayout(self.table_layout)
        self.layout.addLayout(self.button_layout)

        self.table.itemChanged.connect(self.item_changed)
        self.add_equation.clicked.connect(self.add_clicked)
        self.remove_equation.clicked.connect(self.remove_clicked)

        #chart and function tree list
        self.chart = chart
        self.series_list = [""] 

    @Slot()
    def item_changed(self, item: QTableWidgetItem):
        last_row = self.table.rowCount() - 1
        text_valid = len(item.text().strip()) > 0
        if (item.row() == last_row and text_valid):
            self.table.insertRow(last_row + 1)
            self.series_list.append("")

        if (self.series_list[item.row()] != ""):
            prev_function = self.series_list[item.row()]
            self.chart.remove_line(prev_function)

        #todo: need error handling
        func_tree = Function_tree(item.text())

        series = self.evaluate(func_tree)
        self.chart.add_line(series)
        self.series_list[item.row()] = series

    @Slot()
    def add_clicked(self):
        self.table.insertRow(self.table.rowCount())
        self.series_list.append("")

    @Slot()
    def remove_clicked(self):
        self.chart.remove_line(self.chart.series()[self.table.currentRow()])
        self.series_list.remove(self.chart.series()[self.table.currentRow()])

        self.table.removeRow(self.table.currentRow())

    #temporary helper function
    #todo: this should be handled in chart.py
    def evaluate(self, func_tree):
        series = QLineSeries()
        points = [
            QPointF(x/10, func_tree.evaluate(x/10))
            for x in range(-50, 50)
            ]
        series.append(points)

        return series


class WorkspaceWidget(QWidget):
    def __init__(self):
        super().__init__()

        chart = Chart()

        # equation editor
        self.equation_editor = EquationEditorWidget(chart)

        # graphics scene
        #self.scene = QGraphicsScene()
        #self.scene.setBackgroundBrush(QColor('blue')) # coloured to show where scene is
        #self.img = None

        # graphics view
        #self.graph = QGraphicsView(self.scene)
        self.graph = ChartView(chart)

        #todo: figure out what to do with the legend
        #todo: add (0,0) axis lines
        chart.createDefaultAxes()

        # splitter layout
        self.splitter = QSplitter(self)
        self.splitter.addWidget(self.equation_editor)
        self.splitter.addWidget(self.graph)
        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, False)
        self.splitter.setSizes([100,300])

        # overall layout
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.splitter)



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

class TabContainerWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.tabs = QTabWidget(self)
        self.tabs.addTab(WorkspaceWidget(), f"Page {self.tabs.count()+1}")
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(True)
        self.tabs.setTabsClosable(True)

        self.tabs.tabCloseRequested.connect(self.close_page)
        self.tabs.tabBarDoubleClicked.connect(self.tab_double_clicked)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.tabs)

    @Slot()
    def close_page(self, index: int):
        self.tabs.removeTab(index)

    @Slot()
    def tab_double_clicked(self, index: int):
        if index == -1:
            return
        
        rename_dialog = PageRenameDialog(self.tabs.tabText(index))
        if rename_dialog.exec():
            self.tabs.setTabText(index, rename_dialog.text_input.text().strip())

    @Slot()
    def add_page(self):
        self.tabs.addTab(WorkspaceWidget(), f"Page {self.tabs.count()+1}")
        self.tabs.setCurrentIndex(self.tabs.count()-1)

class MainWindow(QMainWindow):
    def __init__(self, widget: TabContainerWidget):
        super().__init__()
        self.setWindowTitle("Name")

        # creating menu actions
        openAction = QAction("Open...", self)
        openAction.triggered.connect(self.open_file)

        saveAction = QAction("Save", self)
        saveAction.triggered.connect(self.save_file)

        newPageAction = QAction("New Page", self)
        newPageAction.triggered.connect(widget.add_page)

        # creating menu bar
        menu = self.menuBar()

        fileMenu = menu.addMenu("File")
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(newPageAction)

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
    widget = TabContainerWidget()
    window = MainWindow(widget)
    window.resize(1000,600)

    window.grabGesture(Qt.PanGesture)
    window.grabGesture(Qt.PinchGesture)

    window.show()

    sys.exit(app.exec())