import time
from pydantic import PrivateAttr, BaseModel
from functools import wraps
from typing import Any, Callable

## FIRST PART

class MyClass(BaseModel):
    _a: int = PrivateAttr(default=1)
    
    @property
    def a(self) -> int:
        return self._a
    
    @a.setter
    def a(self, a: int) -> None:
        if not isinstance(a, int):
            raise TypeError(f"Specified value should be int, found {a.__class__.__name__}")
        self.a = a

def log_args(function: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(function)
    def wrapped_function(*args: Any, **kwargs: Any) -> Any:
        print(f"Calling {function.__name__}(*{args}, **{kwargs})")
        result = function(*args, **kwargs)
        return result
    return wrapped_function

@log_args
def simple_sum(*summands: int) -> int:
    return sum(summands)

## SECOND PART

def timer(function: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(function)
    def wrapped_function(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = function(*args, **kwargs)
        elapsed_time = time.perf_counter() - start
        print(f"Elapsed time for function {function.__name__}: {elapsed_time:.6f} s")
        return result
    return wrapped_function

@timer
def factorial(number: int) -> int:
    if number in (0, 1):
        return 1
    else:
        result = 1
        for n in range(2, number + 1):
            result *= n
        return result