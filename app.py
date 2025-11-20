import math
import sys
from project import Page, Project
from serialize import load, save
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
    def __init__(self, page: Page, chart: Chart):
        super().__init__()
        self.page = page

        # table for equations
        self.table = QTableWidget(0, 1, self)
        self.table.setHorizontalHeaderLabels(["Equation"])
        # self.table.setItem(0,0,QTableWidgetItem("thththt"))

        #chart and function tree list
        self.chart = chart

        for i, equation in enumerate(self.page.equations):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(equation))

            self.chart.add_line()
            self.chart.load_line(equation, i)
            
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_layout = QVBoxLayout()
        self.table_layout.addWidget(self.table)

        # buttons for adding/removing equations
        self.add_equation_button = QPushButton("+", self)
        self.add_equation_button.setToolTip("Add Equation")
        self.remove_equation_button = QPushButton("-", self)
        self.remove_equation_button.setToolTip("Remove Selected Equation")
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.add_equation_button)
        self.button_layout.addWidget(self.remove_equation_button)

        # editor layout
        self.layout = QVBoxLayout(self)
        self.layout.addLayout(self.table_layout)
        self.layout.addLayout(self.button_layout)

        self.table.itemChanged.connect(self.item_changed)
        self.add_equation_button.clicked.connect(self.add_clicked)
        self.remove_equation_button.clicked.connect(self.remove_clicked)

    def add_equation(self, index: int):
        self.table.insertRow(index)
        self.page.add_equation()

    def remove_equation(self, index: int):
        self.table.removeRow(index)
        self.page.remove_equation(index)

    @Slot()
    def item_changed(self, item: QTableWidgetItem):
        last_row = self.table.rowCount() - 1
        text = item.text().strip()
        text_valid = len(text) > 0

        if text_valid:
            if item.row() == last_row:
                self.add_equation(last_row + 1)
                self.chart.add_line()
            self.page.equations[item.row()] = text

        else:
            self.chart.remove_line(item.row())

        if (self.chart.series_list[item.row()] != ""):
            self.chart.remove_line(item.row())

        self.chart.load_line(item.text(), item.row())

    @Slot()
    def add_clicked(self):
        self.chart.add_line()
        self.add_equation(self.table.rowCount())

    @Slot()
    def remove_clicked(self):
        self.chart.remove_line(self.table.currentRow(), True)
        self.remove_equation(self.table.currentRow())


class WorkspaceWidget(QWidget):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page

        chart = Chart()

        # equation editor
        self.equation_editor = EquationEditorWidget(page, chart)

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
    def __init__(self, project: Project):
        super().__init__()
        self.project = project

        self.tabs = QTabWidget(self)
        for page in self.project.pages:
            self.tabs.addTab(WorkspaceWidget(page), page.name)
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
        self.project.remove_page(index)

    @Slot()
    def tab_double_clicked(self, index: int):
        if index == -1:
            return
        
        rename_dialog = PageRenameDialog(self.tabs.tabText(index))
        if rename_dialog.exec():
            name = rename_dialog.text_input.text().strip()
            self.tabs.setTabText(index, name)
            self.tabs.widget(index).page.name = name

    @Slot()
    def add_page(self):
        page = self.project.add_page()
        self.tabs.addTab(WorkspaceWidget(page), page.name)
        self.tabs.setCurrentIndex(self.tabs.count()-1)

class MainWindow(QMainWindow):
    def __init__(self, widget: TabContainerWidget, project: Project):
        super().__init__()
        self.project = project
        self.setWindowTitle("Name")

        # creating menu actions
        self.newFileAction = QAction("New Project", self)
        self.newFileAction.triggered.connect(self.new_file)

        self.openAction = QAction("Open...", self)
        self.openAction.triggered.connect(self.open_file)

        self.saveAction = QAction("Save", self)
        self.saveAction.triggered.connect(self.save_file)

        self.newPageAction = QAction("New Page", self)
        self.newPageAction.triggered.connect(widget.add_page)

        # creating menu bar
        menu = self.menuBar()

        fileMenu = menu.addMenu("File")
        fileMenu.addAction(self.newFileAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.newPageAction)

        self.mainContent = widget
        self.setCentralWidget(widget)

    def change_project(self, new_project: Project):
        self.project = new_project
        self.mainContent = TabContainerWidget(self.project)
        self.newPageAction.triggered.connect(self.mainContent.add_page)
        self.setCentralWidget(self.mainContent)

    @Slot()
    def new_file(self):
        new_project = Project()
        new_project.add_page()
        self.change_project(new_project)

    @Slot()
    def open_file(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter("Graph Projects (*.pkl)")
        # dialog.setDirectory()
        fileName = ""
        if dialog.exec():
            fileName = dialog.selectedFiles()[0]

        self.change_project(load(fileName))

    @Slot()
    def save_file(self):
        fileName = QFileDialog.getSaveFileName()
        save(fileName[0], self.project)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    default_project = Project()
    default_project.add_page()
    widget = TabContainerWidget(default_project)
    window = MainWindow(widget, default_project)
    window.resize(1000,600)

    window.grabGesture(Qt.PanGesture)
    window.grabGesture(Qt.PinchGesture)

    window.show()

    sys.exit(app.exec())
