import pytest
from PySide2.QtWidgets import QApplication
from Plotter import MainWindow, ErrorState
import numpy as np

@pytest.fixture(scope="session", autouse=True)
def setup_qt():
    app = QApplication([])
    yield
    app.quit()

@pytest.fixture
def main_window(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    return window


# test minValueValidation function
@pytest.mark.parametrize("value, valid", [
    ('10', ErrorState.OK),
    ('-5', ErrorState.OK),
    ('-5', ErrorState.OK),
    ('0', ErrorState.OK),
    ('4.5', ErrorState.OK),
    ('0.22', ErrorState.OK),
    ('', ErrorState.EMPTY_MIN_VALUE),
    ('da', ErrorState.INVALID_MIN_VALUE),
    ('$%', ErrorState.INVALID_MIN_VALUE),
    ('57%', ErrorState.INVALID_MIN_VALUE),
    ('agssg', ErrorState.INVALID_MIN_VALUE)
])
def test_minValueValidation(main_window, qtbot, value, valid):
    assert main_window.minValueValidation(value) == valid


# test maxValueValidation function
@pytest.mark.parametrize("value, valid", [
    ('10', ErrorState.OK),
    ('-5', ErrorState.OK),
    ('-5', ErrorState.OK),
    ('0', ErrorState.OK),
    ('4.5', ErrorState.OK),
    ('0.22', ErrorState.OK),
    ('', ErrorState.EMPTY_MAX_VALUE),
    ('da', ErrorState.INVALID_MAX_VALUE),
    ('$%', ErrorState.INVALID_MAX_VALUE),
    ('57%', ErrorState.INVALID_MAX_VALUE),
    ('agssg', ErrorState.INVALID_MAX_VALUE)
])
def test_maxValueValidation(main_window, qtbot, value, valid):
    assert main_window.maxValueValidation(value) == valid


# test processInput function
@pytest.mark.parametrize("value, valid", [
    ('x^2 + sin(x) + cos(x) + tan(x)', 'x**2 + np.sin(x) + np.cos(x) + np.tan(x)'),
    ('sin(x) + cos(x) + tan(x)', 'np.sin(x) + np.cos(x) + np.tan(x)'),
    ('x^3', 'x**3'),
    ('x^2 + 3x + 2', 'x**2 + 3x + 2'),
    ('sqrt(x) + 4', 'np.sqrt(x) + 4'),
    ('e^x', 'np.e**x'),
    ('y = x', 'x'),
    ('y= x + 4', 'x + 4'),
    ('y= sin(x) + 1', 'np.sin(x) + 1'),
])
def test_processInput(main_window, qtbot, value, valid):
    assert main_window.processInput(value) == valid


# test inputValidation function
@pytest.mark.parametrize("minValue, maxValue, equation, valid", [
    ('-5', '5', '4', ErrorState.OK),
    ('-10', '10', 'x**2 + np.sin(x) + np.cos(x) + np.tan(x)', ErrorState.OK),
    ('-10', '10', 'x**3', ErrorState.OK),
    ('-10', '10', 'x**2 + 3x + 2', ErrorState.INVALID_FUNCTION),
    #('-10', '10', 'x/0', ErrorState.INVALID_FUNCTION),
    ('10', '5', 'x**2 + np.sin(x) + np.cos(x) + np.tan(x)', ErrorState.MIN_VALUE_ISNOT_LESS_THAN_MAX_VALUE),
    ('', '10', 'x**2 + np.sin(x) + np.cos(x) + np.tan(x)', ErrorState.EMPTY_MIN_VALUE),
    ('-10', '', 'x**2 + np.sin(x) + np.cos(x) + np.tan(x)', ErrorState.EMPTY_MAX_VALUE),
    ('', '', 'x**2 + np.sin(x) + np.cos(x) + np.tan(x)', ErrorState.EMPTY_MIN_VALUE)
])
def test_inputValidation(main_window, qtbot,minValue, maxValue, equation, valid):
    assert main_window.inputValidation(minValue, maxValue, equation) == valid