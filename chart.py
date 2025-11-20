from PySide6.QtWidgets import QGesture, QGestureEvent
from PySide6.QtCore import Qt, QEvent, QPointF
from PySide6.QtCharts import QChart, QChartView, QLineSeries
from PySide6.QtGui import QMouseEvent, QKeyEvent
from function_tree import Function_tree

class Chart(QChart):
    def __init__(self):
        #todo: make chart widget that can show on the app.py main widget replacing the temp image thing
        #todo: need to iterate through eq. editor
            #delete or add line as equations are removed or added

        super().__init__()

        self.grabGesture(Qt.PanGesture)
        self.grabGesture(Qt.PinchGesture)

        self.func_list = [""] #not used
        self.series_list = [""]

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
            self.addSeries(series)
            self.createDefaultAxes()
            self.series_list[index] = series
        except ValueError as ve:
            print("ValueError exception:", ve)

    def add_line(self):
        """Append entry to series_list"""
        self.series_list.append("")

    def remove_line(self, index: int, removing_entry: bool = False):
        """Removes series from the chart, and its series_list if removing_entry is set"""
        #Remove series from chart if it has been initialized
        if self.series_list[index] != "":
            self.removeSeries(self.series_list[index])

        #Only pop index from series_list if removing_entry was set
        if (removing_entry):
            self.series_list.pop(index)

    #not used, still here just in case
    def modify_line(self, equation: str, index: int):
        pass

    def evaluate(self, func_tree: Function_tree):
        """Evaluates func_tree at 1000 points along x-axis"""
        #todo: allow custom x-axis ranges to be used
        #todo: fix division at 0
        series = QLineSeries()
        points = []
        #calculate 1000 points within range
        for x in range (-500, 500):
            y = func_tree.evaluate(x/100)
            if y != None:
                points.append(QPointF(x/100, y))
        
        series.append(points)
        return series


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
