# Function Plotter
- This project is for Master Micro Company.
- Language: Python
- Development environment: PyCharm
- Project type: Desktop Application
## Aim
plots arbitrary user-entered function 
## Procedure Details
1. Write a Python GUI program that plots an arbitrary user-entered function.
2. Take a function of x from the user, e.g., 5*x^3 + 2*x.
3. Take min and max values of x from the user.
4. The following operators must be supported: + - / * ^ sin cos tan.
5. Apply appropriate input validation to the user input.
6. Display messages to the user to explain any wrong input.
## Output

## Demonstration
[here](https://drive.google.com/file/d/10SFa9VwcOm5OibtIMCH5IV0c51rp6eFK/view?usp=sharing)

## Requirments
* App Requirments 
```python
pip install PySide2
pip install numpy
pip install matplotlib
```
* Testing Requirments
```python
pip install pytest
pip install pytest-qt
```

## Usage
* Run [app.py](app.py) file.
```python
python app.py
```
* In case of testing, run [test_app.py](test_app.py) file.
```python
pytest test_app.py
```
