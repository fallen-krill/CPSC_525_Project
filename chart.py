from PySide6.QtWidgets import (
    QGesture, QGestureEvent
)
from PySide6.QtCore import (
    Qt, QEvent, QPointF, QRectF
)
from PySide6.QtCharts import (
    QChart, QChartView, QLineSeries, QScatterSeries
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

        #List holding series shown on chart
        self.func_list = [""] #not used
        self.series_list =  [[]]

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

    #not used, still here just in case
    def modify_line(self, equation: str, index: int):
        pass

    def evaluate(self, func_tree: Function_tree):
        """Evaluates func_tree at 1001 points along the x-axis"""
        #todo: allow custom x-axis ranges to be used
        series_arr = []
        series = QLineSeries()
        points = []

        col = series.color()

        #calculate 1001 points within range
        for x in range (-500, 501):
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

            #print(f"{x},{y}")
        
        series.append(points)
        series_arr.append(series)

        return series_arr

class ChartView(QChartView):
    def __init__(self, chart):
        super().__init__(chart)
        
        self.setRubberBand(QChartView.RectangleRubberBand)

        self._isTouching = False
        self.x_limit = 10
        self.y_limit = 10

    def viewportEvent(self, event: QEvent):

        if event == QMouseEvent.TouchBegin:
            self._isTouching = True
        
        return super().viewportEvent(event)

    #all except keypressevent are from https://doc.qt.io/qtforpython-6/examples/example_charts_zoomlinechart.html#example-charts-zoomlinechart
    #they are here for testing
    #todo:
    #   -dragging mouse will move graph
    #   -scroll wheel should zoom in/out
    def mousePressEvent(self, event: QMouseEvent):

        if self._isTouching:
            return

        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):

        if self._isTouching:
            return

        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):

        if self._isTouching:
            self._isTouching = False

        self.chart().setAnimationOptions(QChart.SeriesAnimations)

        return super().mouseReleaseEvent(event)
    
    def keyPressEvent(self, event: QKeyEvent):

        key = event.key()
        match(key):
            case Qt.Key_Equal:
                self.chart().zoomIn()
            case Qt.Key_Minus:
                self.chart().zoomOut()
            #try zoom in qrectf
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
