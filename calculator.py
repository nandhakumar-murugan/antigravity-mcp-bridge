def add(a: float, b: float) -> float:
    """Returns the sum of a and b."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Returns the difference of a and b."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Returns the product of a and b."""
    return a * b


def divide(a: float, b: float) -> float:
    """Returns the quotient of a and b. Raises ValueError on division by zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


def power(a: float, b: float) -> float:
    """Returns a raised to the power of b."""
    return a ** b
