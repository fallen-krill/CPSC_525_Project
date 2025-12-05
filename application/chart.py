from PySide6.QtWidgets import (
    QGesture, QGestureEvent, QMessageBox
)
from PySide6.QtCore import (
    Qt, QEvent, QPointF, QRectF
)
from PySide6.QtCharts import (
    QChart, QChartView, QLineSeries, QScatterSeries, QValueAxis
)
from PySide6.QtGui import (
    QMouseEvent, QKeyEvent, QColor
)
from project import Page
from function_tree import Function_tree, ParsingError

class Chart(QChart):
    def __init__(self):

        super().__init__()

        #self.grabGesture(Qt.PanGesture)
        #self.grabGesture(Qt.PinchGesture)

        #The default colors used by QXYSeries when none are specified, copied here for convenience
        self.colors = [
            QColor(),
            QColor(),
            QColor(),
            QColor(),
            QColor()
        ]
        self.colors[0].setRgbF(0.125490, 0.623529, 0.874510, 1.000000)
        self.colors[1].setRgbF(0.600000, 0.792157, 0.325490, 1.000000)
        self.colors[2].setRgbF(0.964706, 0.650980, 0.145098, 1.000000)
        self.colors[3].setRgbF(0.427451, 0.372549, 0.835294, 1.000000)
        self.colors[4].setRgbF(0.749020, 0.349020, 0.243137, 1.000000)

        self.func_list = []         #holds equations
        self.series_list =  [[]]    #holds series shown on chart

        #min/max values for both x and y axes
        self.y_min = -10.0
        self.y_max = 10.0
        self.x_min = -10.0
        self.x_max = 10.0

        self.legend().hide()

        #lines at x=0 and y=0
        self.y_line = QLineSeries()
        self.x_line = QLineSeries()

        self.axis_col = QColor()
        self.axis_col.setRgbF(0.55,0.55,0.55,1.0)

        self.update_axis_lines()

        self.addSeries(self.y_line)
        self.addSeries(self.x_line)

    def update_axis_lines(self):
        """Updates lines at x=0 and y=0"""
        #Clear points
        self.y_line.clear()
        self.x_line.clear()

        #Set lines to start and end at the edge of the chart
        self.y_line.append(0.0, self.y_min)
        self.y_line.append(0.0, self.y_max)
        self.x_line.append(self.x_min, 0.0)
        self.x_line.append(self.x_max, 0.0)

        #set line color, thickness does not matter
        self.y_line.setColor(self.axis_col)
        self.x_line.setColor(self.axis_col)

    def load_line(self, page: Page, index: int):
        """Loads result of (precomputed) function tree onto the chart and to series_list at given index"""
        if not page.function_trees[index].is_valid():
            return

        #calculate series, add to chart
        try:
            #Function tree is passed, so evaluate it
            series = self.evaluate(page.function_trees[index], self.x_min, self.y_min, self.x_max, self.y_max)
            
            #add series to chart and set axes
            for s in series:
                #get color of the series, based off on of the default colors used by QXYSeries/QLineSeries
                s.setColor(self.colors[index % 5])

                #set width of pen, directly changing the QLineSeries would not work as intended
                pen = s.pen()
                pen.setWidthF(2.0) 
                s.setPen(pen)

                self.addSeries(s)

            #set x/y axis range so series can render as intended
            self.createDefaultAxes()

            y_axis = self.axisY()
            x_axis = self.axisX()

            y_axis.setRange(self.y_min, self.y_max)
            x_axis.setRange(self.x_min, self.x_max)

            #record equation and series
            self.func_list[index] = page.equations[index]
            self.series_list[index] = series

        except ParsingError as ve:
            QMessageBox.warning(self.parent(), "Math Error", str(ve))

    def add_line(self):
        """Append entry to series_list"""
        self.func_list.append("")
        self.series_list.append([])

    def remove_line(self, index: int, removing_entry: bool = False):
        """Removes series from the chart, and its series_list if removing_entry is set"""
        #Remove series from chart if it has been initialized
        if len(self.series_list[index]) != 0:
            for s in self.series_list[index]:
                self.removeSeries(s)

        #Only pop index from series_list if removing_entry was set
        if (removing_entry):
            self.func_list.pop(index)
            self.series_list.pop(index)

            
    def evaluate(self, func_tree: Function_tree, min_x=-10, min_y=-10, max_x=10, max_y=10):
        """Evaluates func_tree at 1001 points along the x-axis and returns list of points. May raise ValueError"""
        series_arr = []
        series = QLineSeries()
        points = []

        #calculate 1000 points within range
        step = (max_x - min_x)/1000.00
        for i in range(1001):
            x = min_x + i*step
            y = func_tree.evaluate(x)

            if y != None:
                #Check that asymptote was passed first
                if (len(points) > 0):
                    #We can tell if an asymptote was passed if this number is very high and is negative
                    pol = y * points[len(points)-1].y()
                    if (abs(pol) > (self.y_max - self.y_min) and pol < 0):
                        series.append(points)
                        series_arr.append(series)

                        series = QLineSeries()
                        points = []

                points.append(QPointF(x, y))

            #Value returned was None, meaning it attempted to evaluate at undefined value
            elif (len(points) > 0):
                series.append(points)
                series_arr.append(series)

                series = QLineSeries()
                points = []
        
        series.append(points)
        series_arr.append(series)

        return series_arr
    
    def regraph(self, x_min=-10.0, x_max=10.0, y_min=-10.0, y_max=10.0):
        """Reloads all functions currently on the graph. Called with user input in ChartView."""
        
        #set min/max of each axis
        self.y_min = y_min
        self.y_max = y_max
        self.x_min = x_min
        self.x_max = x_max

        self.update_axis_lines()

        #reload each function
        for i in range(len(self.func_list)):
            
            #evaluate function tree again with new range
            equation = self.func_list[i]
            func_tree = Function_tree(equation)
            if not func_tree.is_valid():
                continue # skip invalid functions
            
            series = self.evaluate(func_tree, x_min, y_min, x_max, y_max)

            color = QColor()

            #remove series and get its color
            if (len(self.series_list[i]) != 0):
                for s in self.series_list[i]:
                    self.removeSeries(s)

                color = self.series_list[i][0].color()

            #add series and set its color
            for s in series:
                s.setColor(color)

                pen = s.pen()
                pen.setWidthF(2.0)
                s.setPen(pen)
                
                self.addSeries(s)

            #replace recorded series
            self.series_list[i] = series

        #set x/y axis range so series can render as intended
        self.createDefaultAxes()

        y_axis = self.axisY()
        x_axis = self.axisX()

        y_axis.setRange(self.y_min, self.y_max)
        x_axis.setRange(self.x_min, self.x_max)
        

class ChartView(QChartView):
    def __init__(self, chart):
        super().__init__(chart)

        self.qchart = chart
    
    def keyPressEvent(self, event: QKeyEvent):
        """Handles key input"""
        key = event.key()
        #self.chart().setAnimationOptions(QChart.SeriesAnimations)

        x_min = self.qchart.axisX().min()
        x_max = self.qchart.axisX().max()
        y_min = self.qchart.axisY().min()
        y_max = self.qchart.axisY().max()

        match(key):
            #Zoom in
            case Qt.Key_Equal:
                self.chart().zoomIn()
                x_min = self.qchart.axisX().min()
                x_max = self.qchart.axisX().max()
                y_min = self.qchart.axisY().min()
                y_max = self.qchart.axisY().max()
            #Zoom out
            case Qt.Key_Minus:
                self.chart().zoomOut()
                x_min = self.qchart.axisX().min()
                x_max = self.qchart.axisX().max()
                y_min = self.qchart.axisY().min()
                y_max = self.qchart.axisY().max()
            #Reset zoom to [-10,10] on x/y axis
            case Qt.Key_0:
                self.chart().zoomReset()
                x_min = -10.0
                x_max = 10.0
                y_min = -10.0
                y_max = 10.0
            #Scroll up
            case Qt.Key_Up:
                self.chart().scroll(0, 10)
                y_min = self.qchart.axisY().min()
                y_max = self.qchart.axisY().max()
            #Scroll down
            case Qt.Key_Down:
                self.chart().scroll(0, -10)
                y_min = self.qchart.axisY().min()
                y_max = self.qchart.axisY().max()
            #Scroll left
            case Qt.Key_Left:
                self.chart().scroll(-10, 0)
                x_min = self.qchart.axisX().min()
                x_max = self.qchart.axisX().max()
            #Scroll right
            case Qt.Key_Right:
                self.chart().scroll(10, 0)
                x_min = self.qchart.axisX().min()
                x_max = self.qchart.axisX().max()
            case _:
                pass

        self.qchart.regraph(x_min, x_max, y_min, y_max)
