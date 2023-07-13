import sys
import numpy as np
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QMessageBox, QHBoxLayout, QVBoxLayout
from PySide2.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
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

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # set App name
        self.setWindowTitle("Function Plotter")

        # set App icon
        self.setWindowIcon(QIcon("icon.png"))

        # layout 1
        self.label_EnterEquation = QLabel("Enter equation")
        self.lineEdit_equation = QLineEdit()

        self.hlayout1 = QHBoxLayout()
        self.hlayout1.addWidget(self.label_EnterEquation)
        self.hlayout1.addWidget(self.lineEdit_equation)


        # layout 2
        self.label_EnterMinValue = QLabel("Enter min value")
        self.lineEdit_minValue = QLineEdit()

        self.hlayout2 = QHBoxLayout()
        self.hlayout2.addWidget(self.label_EnterMinValue)
        self.hlayout2.addWidget(self.lineEdit_minValue)


        # layout 3
        self.label_EnterMaxValue = QLabel("Enter max value")
        self.lineEdit_maxValue = QLineEdit()

        self.hlayout3 = QHBoxLayout()
        self.hlayout3.addWidget(self.label_EnterMaxValue)
        self. hlayout3.addWidget(self.lineEdit_maxValue)


        # layout 4
        self.button_plot = QPushButton("Plot")
        self.button_plot.clicked.connect(self.plotting)

        self.hlayout4 = QHBoxLayout()
        self.hlayout4.addWidget(self.button_plot)


        # layout 5
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.hlayout5 = QHBoxLayout()
        self.hlayout5.addWidget(self.canvas)


        # layouts
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.hlayout1)
        self.layout.addLayout(self.hlayout2)
        self.layout.addLayout(self.hlayout3)
        self.layout.addLayout(self.hlayout4)
        self.layout.addLayout(self.hlayout5)

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
        this function is used to replace the following
         ^ with **
         sin with np.sin
         cos with np.cos
         tan with np.tan
    """
    def processInput(self,equation):
        equation = equation.replace('^', '**')
        equation = equation.replace('sin', 'np.sin')
        equation = equation.replace('cos', 'np.cos')
        equation = equation.replace('tan', 'np.tan')
        return equation


    """
    this function is used to disolay error to user
    """
    def displayError(self,message):
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.setWindowTitle("Error")
        msg_box.exec_()


    """
        this function is used to validate user input
    """
    def inputValidation(self,minValue, maxValue, function_str):
        # check minValue
        if minValue == '':
            return ErrorState.EMPTY_MIN_VALUE
        else:
            try:
                minValue = float(minValue)
            except ValueError:
                return ErrorState.INVALID_MIN_VALUE

        # check maxValue
        if maxValue == '':
            return ErrorState.EMPTY_MAX_VALUE
        else:
            try:
                maxValue = float(maxValue)
            except ValueError:
                return ErrorState.INVALID_MAX_VALUE

        # check maxValue and minValue
        if minValue >= maxValue:
            return ErrorState.MIN_VALUE_ISNOT_LESS_THAN_MAX_VALUE

        # check function
        try:
            x = np.linspace(float(minValue), float(maxValue), 1000)
            y = eval(function_str)
            return ErrorState.OK
        except:
            return ErrorState.INVALID_FUNCTION


    """
        this function is used to read data then process it then validate it then plot the figure
    """
    def plotting(self):
        # read data
        minValue, maxValue, equation = self.inputRead()

        # process data
        equation = self.processInput(equation)

        # check data
        if self.inputValidation(minValue, maxValue, equation) == ErrorState.EMPTY_MIN_VALUE:
            self.displayError("Please enter minimum x")
        elif self.inputValidation(minValue, maxValue, equation) == ErrorState.EMPTY_MAX_VALUE:
            self.displayError("Please enter Maximum x")
        elif self.inputValidation(minValue, maxValue, equation) == ErrorState.INVALID_MIN_VALUE:
            self.displayError("Minimum x value must be a number")
            self.lineEdit_minValue.clear()
        elif self.inputValidation(minValue, maxValue, equation) == ErrorState.INVALID_MAX_VALUE:
            self.displayError("Maximum x value must be a number")
            self.lineEdit_maxValue.clear()
        elif self.inputValidation(minValue, maxValue, equation) == ErrorState.MIN_VALUE_ISNOT_LESS_THAN_MAX_VALUE:
            self.displayError("Maximum x value must be greater than Minimum x value")
            self.lineEdit_minValue.clear()
            self.lineEdit_maxValue.clear()
        elif self.inputValidation(minValue, maxValue, equation) == ErrorState.INVALID_FUNCTION:
            self.displayError("Invalid function")
            self.lineEdit_equation.clear()
        else:
            x = np.linspace(float(minValue), float(maxValue), 1000)
            y = eval(equation)
            self.figure.clear()

            # Add a plot to the figure
            ax = self.figure.add_subplot(111)
            ax.set(title="Function Plotting", xlabel=r'$x$', ylabel=r'$f(x)$')
            ax.plot(x, y)
            self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())