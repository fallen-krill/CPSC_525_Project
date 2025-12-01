from PySide6.QtWidgets import (
    QGesture, QGestureEvent
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
from function_tree import Function_tree

class Chart(QChart):
    def __init__(self):

        super().__init__()

        self.grabGesture(Qt.PanGesture)
        self.grabGesture(Qt.PinchGesture)

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

        self.func_list = []         #holds equations (NOT USED yet)
        self.series_list =  [[]]    #holds series shown on chart

        self.y_min = -10.0
        self.y_max = 10.0
        self.x_min = -10.0
        self.x_max = 10.0

        self.legend().hide()

    def sceneEvent(self, event: QEvent):
        
        if event.type() == QEvent.Gesture:
            return self.gestureEvent(event)
        
        return super().sceneEvent(event)
    
    def gestureEvent(self, event: QGestureEvent):

        if gesture := event.gesture(Qt.PanGesture):
            print("panning")
            pan = gesture
            self.scroll(-pan.delta().x(), pan.delta().y())

        if gesture := event.gesture(Qt.PinchGesture):
            print("pinching")
            pinch = gesture
            if pinch.changeFlags() & QGesture.QPinchGesture.ScaleFactorChanged:
                self.zoom(pinch.scaleFactor())

        return True

    def load_line(self, equation: str, index: int):
        """Loads result of equation onto the chart and to series_list at given index"""
        #calculate series, add to chart
        try:
            #get function tree from equation, and evaluate it
            func_tree = Function_tree(equation)
            series = self.evaluate(func_tree)
            
            #add series to chart and set axes
            for s in series:
                s.setColor(self.colors[index % 5])

                pen = s.pen()
                pen.setWidthF(2.0)
                s.setPen(pen)

                self.addSeries(s)

            self.createDefaultAxes()

            y_axis = self.axisY()
            x_axis = self.axisX()

            y_axis.setRange(self.y_min, self.y_max)
            x_axis.setRange(self.x_min, self.x_max)

            self.series_list[index] = series

        except ValueError as ve:
            print("ValueError exception:", ve)

    def add_line(self):
        """Append entry to series_list"""
        self.series_list.append([])

    def remove_line(self, index: int, removing_entry: bool = False):
        """Removes series from the chart, and its series_list if removing_entry is set"""
        #Remove series from chart if it has been initialized
        if len(self.series_list[index]) != 0:
            for s in self.series_list[index]:
                self.removeSeries(s)

        #Only pop index from series_list if removing_entry was set
        if (removing_entry):
            self.series_list.pop(index)
            
    def evaluate(self, func_tree: Function_tree):
        """Evaluates func_tree at 1001 points along the x-axis"""
        series_arr = []
        series = QLineSeries()
        points = []

        #calculate 1001 points within range
        #step = (self.max_x - self.min_x) / 1001.0
        for x in range (-1000, 1001):
            #x = self.min_x + (step * i)
            y = func_tree.evaluate(x/100)

            if y != None:
                #Check that asymptote was passed first
                if (len(points) > 0):
                    #We can tell if an asymptote was passed if this number is very high and is negative
                    pol = y * points[len(points)-1].y()
                    if (abs(pol) > 10000.0 and pol < 0):
                        series.append(points)
                        series_arr.append(series)

                        series = QLineSeries()
                        points = []

                points.append(QPointF(x/100, y))

            #Value returned was None, meaning it attempted to evaluate at undefined value
            elif (len(points) > 0):
                series.append(points)
                series_arr.append(series)

                series = QLineSeries()
                points = []
        
        series.append(points)
        series_arr.append(series)

        return series_arr

class ChartView(QChartView):
    def __init__(self, chart):
        super().__init__(chart)

        self.qchart = chart
    
    def keyPressEvent(self, event: QKeyEvent):

        key = event.key()
        self.chart().setAnimationOptions(QChart.SeriesAnimations)
        match(key):
            #need to set max/min axis values on chart, re-evaluate accordingly
            case Qt.Key_Equal:
                self.chart().zoomIn()
            case Qt.Key_Minus:
                self.chart().zoomOut()
            case Qt.Key_0:
                self.chart().zoomReset()
            case Qt.Key_Up:
                self.chart().scroll(0, 10)
            case Qt.Key_Down:
                self.chart().scroll(0, -10)
            case Qt.Key_Left:
                self.chart().scroll(-10, 0)
            case Qt.Key_Right:
                self.chart().scroll(10, 0)
            case _:
                pass
