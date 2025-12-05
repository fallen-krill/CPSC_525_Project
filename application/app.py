import math
import sys
from project import Page, Project
from serialize import serialize, deserialize
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
    QListWidget, QListWidgetItem, QPushButton, QStyledItemDelegate, QMessageBox
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
        self.text = QLabel("Graphing Calculator", self)
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

        #chart and function tree list
        self.chart = chart

        for i in range(len(self.page.equations)):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(self.page.equations[i]))

            self.chart.add_line()
            self.chart.load_line(self.page, i)
            
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

        # connect slots
        self.table.itemChanged.connect(self.item_changed)
        self.add_equation_button.clicked.connect(self.add_clicked)
        self.remove_equation_button.clicked.connect(self.remove_clicked)

    def add_equation(self, index: int):
        self.table.insertRow(index)
        self.page.add_equation()

    def remove_equation(self, index: int):
        """This is not the same data structure as the one in chart.py."""
        self.table.removeRow(index)
        self.page.remove_equation(index)

    @Slot()
    def item_changed(self, item: QTableWidgetItem):
        last_row = self.table.rowCount() - 1
        text = item.text().strip()

        if item.row() == last_row:
            self.add_equation(last_row + 1)
            self.chart.add_line()
        self.page.equations[item.row()] = text
        self.page.function_trees[item.row()] = Function_tree(text)

        if len(text) == 0 or self.chart.series_list[item.row()] != "":
            # text empty or value changed
            self.chart.remove_line(item.row())

        self.chart.load_line(self.page, item.row())

    @Slot()
    def add_clicked(self):
        self.chart.add_line()
        self.add_equation(self.table.rowCount())

    @Slot()
    def remove_clicked(self):
        self.chart.remove_line(self.table.currentRow(), True)
        self.remove_equation(self.table.currentRow())


class WorkspaceWidget(QWidget):
    """Holds equation editor and graph in a splitter."""
    def __init__(self, page: Page):
        super().__init__()
        self.page = page

        chart = Chart()

        # equation editor
        self.equation_editor = EquationEditorWidget(page, chart)

        # graphics view
        self.graph = ChartView(chart)

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


class TabContainerWidget(QWidget):
    def __init__(self, project: Project):
        super().__init__()
        self.project = project

        self.tabs = QTabWidget(self)
        # tabs correspond to pages in the project datastructure
        for page in self.project.pages:
            self.tabs.addTab(WorkspaceWidget(page), page.name)
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(True)
        self.tabs.setTabsClosable(True)

        # connect slots
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
        
        # rename the selected tab
        rename_dialog = PageRenameDialog(self.tabs.tabText(index))
        if rename_dialog.exec():
            name = rename_dialog.text_input.text().strip()
            self.tabs.setTabText(index, name)
            self.tabs.widget(index).page.name = name

    @Slot()
    def add_page(self):
        """Add another page to this project."""
        page = self.project.add_page()
        self.tabs.addTab(WorkspaceWidget(page), page.name)
        self.tabs.setCurrentIndex(self.tabs.count()-1)


class MainWindow(QMainWindow):
    def __init__(self, widget: TabContainerWidget, project: Project):
        super().__init__()
        self.project = project
        self.setWindowTitle("Graphing Calculator")

        # creating menu actions
        self.newFileAction = QAction("New Project", self)
        self.newFileAction.triggered.connect(self.new_file)

        self.openAction = QAction("Open...", self)
        self.openAction.triggered.connect(self.open_file)

        self.saveAction = QAction("Save", self)
        self.saveAction.triggered.connect(self.save_file)

        self.newPageAction = QAction("New Page", self)
        self.newPageAction.triggered.connect(widget.add_page)

        self.closeAction = QAction("Close Window", self)

        self.closeAction.triggered.connect(self.close_app)
        
        # creating menu bar
        menu = self.menuBar()

        fileMenu = menu.addMenu("File")
        fileMenu.addAction(self.newFileAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.newPageAction)
        fileMenu.addAction(self.closeAction)

        self.mainContent = widget
        self.setCentralWidget(widget)

    def change_project(self, new_project: Project):
        """Abandon this project and start a new one."""
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
        fileName = ""
        if dialog.exec():
            fileName = dialog.selectedFiles()[0]

        # if no file selected
        if fileName == "":
            return

        try:
            # The bug is in serialize.py and the fix is there
            self.change_project(deserialize(fileName))

        except UnicodeDecodeError:
            QMessageBox.warning(self, "File Error", f"The file \"{fileName}\" uses an invalid encoding.")
        except Exception as e:
            #failed to load file data
            QMessageBox.warning(self, "File Error", f"The file \"{fileName}\" could not be opened.")

    @Slot()
    def save_file(self):
        fileName = QFileDialog.getSaveFileName()[0]
        
        # The bug is in serialize.py the fix is there
        try:
            serialize(fileName, self.project)
        except OSError:
            QMessageBox.warning(self, "Cannot write file.", f"The file \"{fileName}\" could not be saved.")

    @Slot()
    def close_app(self):
        sys.exit(0)


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
