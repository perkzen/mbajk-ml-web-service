from time import perf_counter
from functools import wraps
from typing import Callable, Any


def execution_timer(name: str = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time: float = perf_counter()
            result: Any = func(*args, **kwargs)
            end_time: float = perf_counter()

            log_name = name if name else func.__name__

            execution_time: int = int((end_time - start_time) * 1000)

            print(f'[{log_name}] - took {execution_time}ms to execute')
            return result

        return wrapper

    return decorator
