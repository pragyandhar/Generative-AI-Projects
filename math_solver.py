'''math_solver.py'''
# IMPORT
from sympy import Symbol, solve

from langchain.tools import tool

# TOOL CREATION
@tool
def solve_math(question: str):
    """
    Solve a math expression or equation.
    e.g., "2x + 3 = 7"
    """
    # assume a single variable x
    x = Symbol('x')
    try:
        # if expression contains '=', split and solve
        if "=" in question:
            left, right = question.split("=")
            return str(solve(left.strip() + "-(" + right.strip() + ")", x))
        else:
            # if no equality, just evaluate
            return str(eval(question))
    except Exception as e:
        return f"Error: {e}"