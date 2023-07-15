import sys
import numpy as np
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QMessageBox, QHBoxLayout, QVBoxLayout
from PySide2.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

from matplotlib.figure import Figure
from enum import Enum


"""
    this class used to indicate errors in user input
"""
class ErrorState(Enum):
    OK = 0
    INVALID_FUNCTION = 1
    INVALID_MIN_VALUE = 2
    EMPTY_MIN_VALUE = 3
    INVALID_MAX_VALUE = 4
    EMPTY_MAX_VALUE = 5
    MIN_VALUE_ISNOT_LESS_THAN_MAX_VALUE = 6
    EMPTY_FUNCTION = 7

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # set App name
        self.setWindowTitle("Function Plotter")

        # set App icon
        self.setWindowIcon(QIcon("icon.png"))

        ################### components #######################
        self.label_EnterEquation = QLabel("Equation")
        self.lineEdit_equation = QLineEdit()

        self.label_EnterMinValue = QLabel("Min   x   ")
        self.lineEdit_minValue = QLineEdit()

        self.label_EnterMaxValue = QLabel("Max   x  ")
        self.lineEdit_maxValue = QLineEdit()

        self.button_plot = QPushButton("Plot")
        self.button_plot.clicked.connect(self.plotting)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolBar = NavigationToolbar2QT(self.canvas)
        self.toolBar.setVisible(False)


        ################## layouts ###########################
        # layout 1
        self.hlayout1 = QHBoxLayout()
        self.hlayout1.addWidget(self.label_EnterEquation)
        self.hlayout1.addWidget(self.lineEdit_equation)

        # layout 2
        self.hlayout2 = QHBoxLayout()
        self.hlayout2.addWidget(self.label_EnterMinValue)
        self.hlayout2.addWidget(self.lineEdit_minValue)

        # layout 3
        self.hlayout3 = QHBoxLayout()
        self.hlayout3.addWidget(self.label_EnterMaxValue)
        self. hlayout3.addWidget(self.lineEdit_maxValue)

        # layout 4
        self.hlayout4 = QHBoxLayout()
        self.hlayout4.addWidget(self.button_plot)

        # layout 5
        self.hlayout5 = QVBoxLayout()
        self.hlayout5.addWidget(self.toolBar)

        # layout 6
        self.hlayout6 = QHBoxLayout()
        self.hlayout6.addWidget(self.canvas)

        #  main layout
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.hlayout1)
        self.layout.addLayout(self.hlayout2)
        self.layout.addLayout(self.hlayout3)
        self.layout.addLayout(self.hlayout4)
        self.layout.addLayout(self.hlayout5)
        self.layout.addLayout(self.hlayout6)
        self.setLayout(self.layout)


    """
    this function is used to read data from user
    """
    def inputRead(self):
        minValue = self.lineEdit_minValue.text()
        maxValue = self.lineEdit_maxValue.text()
        equation = self.lineEdit_equation.text()
        return minValue, maxValue, equation


    """
        this function is used to preform replacements, handle constant functions and handle writing equation as y = 
           like
               ^ with **
               sin with np.sin
               cos with np.cos
               tan with np.tan
               sqrt with np.sqrt
          like 
               y = 1
               y = 5 
          like 
               y = x
               y = 4*x + 1
    """
    def processInput(self,equation):
        # preform replacements
        equation = equation.replace('^', '**')
        equation = equation.replace('sin', 'np.sin')
        equation = equation.replace('cos', 'np.cos')
        equation = equation.replace('tan', 'np.tan')
        equation = equation.replace('sqrt', 'np.sqrt')
        equation = equation.replace('e', str(np.e))

        # handle constant functions
        if "x" not in equation:
            equation = f"{equation}+0*x"

        # handle writing equation  as y =
        if equation.startswith('y =') or equation.startswith('y='):
            equation = equation[3:]

        return equation


    """
    this function is used to display error to user
    """
    def displayError(self,message):
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.setWindowTitle("Error")
        msg_box.exec_()


    """
           this function is used to validate minValue entered by user
    """
    def minValueValidation(self,minValue):
        if minValue == '':
            return ErrorState.EMPTY_MIN_VALUE
        else:
            try:
                minValue = float(minValue)
                return ErrorState.OK
            except ValueError:
                return ErrorState.INVALID_MIN_VALUE


    """
          this function is used to validate maxValue entered by user
    """
    def maxValueValidation(self, maxValue):
        if maxValue == '':
            return ErrorState.EMPTY_MAX_VALUE
        else:
            try:
                maxValue = float(maxValue)
                return ErrorState.OK
            except ValueError:
                return ErrorState.INVALID_MAX_VALUE


    """
        this function is used to validate user input
    """
    def inputValidation(self,minValue, maxValue, function_str):
        # check function
        if function_str == '+0*x':
            return ErrorState.EMPTY_FUNCTION
        else:
            try:
                x = np.linspace(-10, 10, 1000)
                y = eval(function_str)
            except:
                return ErrorState.INVALID_FUNCTION

        # check minValue
        isValid = self.minValueValidation(minValue)
        if isValid != ErrorState.OK:
            return isValid

        # check maxValue
        isValid = self.maxValueValidation(maxValue)
        if isValid != ErrorState.OK:
            return isValid

        # check maxValue and minValue
        if float(minValue) >= float(maxValue):
            return ErrorState.MIN_VALUE_ISNOT_LESS_THAN_MAX_VALUE

        return ErrorState.OK


    """
        this function is used to read data then process it then validate it then plot the figure
    """
    def plotting(self):
        # read data
        minValue, maxValue, equation = self.inputRead()

        # process data
        equation = self.processInput(equation)

        # check data
        isValid = self.inputValidation(minValue, maxValue, equation)
        if isValid == ErrorState.EMPTY_FUNCTION:
            self.displayError("please enter function")
        elif isValid == ErrorState.INVALID_FUNCTION:
            self.displayError("Invalid function")
            self.lineEdit_equation.clear()
        elif isValid == ErrorState.EMPTY_MIN_VALUE:
            self.displayError("Please enter min x")
        elif isValid == ErrorState.INVALID_MIN_VALUE:
            self.displayError("min x value must be a number")
            self.lineEdit_minValue.clear()
        elif isValid == ErrorState.EMPTY_MAX_VALUE:
            self.displayError("Please enter max x")
        elif isValid == ErrorState.INVALID_MAX_VALUE:
            self.displayError("max x value must be a number")
            self.lineEdit_maxValue.clear()
        elif isValid == ErrorState.MIN_VALUE_ISNOT_LESS_THAN_MAX_VALUE:
            self.displayError("max x value must be greater than min x value")
            self.lineEdit_minValue.clear()
            self.lineEdit_maxValue.clear()
        elif isValid == ErrorState.OK:
            # plotting
            self.toolBar.setVisible(True)
            x = np.linspace(float(minValue), float(maxValue), 1000)
            y = eval(equation)
            self.figure.clear()
            mask = ~(np.isnan(y) | np.isinf(y))
            # Add a plot to the figure
            ax = self.figure.add_subplot(111)
            ax.set(title="Function Plotting", xlabel=r'$x$', ylabel=r'$f(x)$')
            ax.plot(x[mask], y[mask])       # ax.plot(x, y)
            self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())