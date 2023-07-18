# Function Plotter
- This task is for Master Micro Company.
- Language: Python
- Development environment: PyCharm
- Project type: Desktop Application
## Aim
plots arbitrary user-entered function. 
## Procedure Details
1. Write a Python GUI program that plots an arbitrary user-entered function.
2. Take a function of x from the user, e.g., 5*x^3 + 2*x.
3. Take min and max values of x from the user.
4. The following operators must be supported: + - / * ^.
5. Apply appropriate input validation to the user input.
6. Display messages to the user to explain any wrong input.

## Extra Features
1. support sin , cos, tan, sqrt and e
2. user can enter constant instead of expression of x
3. user can enter function in any one of this forms
    - y = expression
    - expression
4. add features provided by NavigationToolbar2QT like
    - saving the plot to a file
    - panning and zooming the plot
    - resetting the view
## Demonstration
[here](https://drive.google.com/file/d/1NpscHyk2DUu0jgxtbNaKNMkCAH-PVyGW/view?usp=sharing)

## Requirements
* App Requirements 
```python
pip install PySide2
pip install numpy
pip install matplotlib
```
* Testing Requirements
```python
pip install pytest
pip install pytest-qt
```

## Usage
* Using exe file
```
- go to Demostration Section
- click on here
- download file
```
* Run [Plotter.py](Plotter.py) file.
```python
python Plotter.py
```
* In case of testing, run [test.py](test.py) file.
```python
pytest test.py
```
