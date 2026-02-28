"""
Retry decorator with exponential backoff for handling transient API failures.

Usage:
    @retry_with_backoff(max_retries=3, base_delay=1)
    def my_api_call():
        # API call that might fail
        pass
"""

import time
import functools
from typing import Callable, TypeVar, Any
from logger import get_logger

logger = get_logger(__name__)

# Type variable for generic function signature
F = TypeVar('F', bound=Callable[..., Any])


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    exponential_base: float = 2.0,
    exceptions: tuple = (Exception,)
) -> Callable[[F], F]:
    """
    Decorator that retries a function with exponential backoff on failure.

    Args:
        max_retries: Maximum number of retry attempts (default: 3)
        base_delay: Initial delay in seconds between retries (default: 1.0)
        exponential_base: Base for exponential backoff calculation (default: 2.0)
        exceptions: Tuple of exception types to catch and retry (default: all exceptions)

    Returns:
        Decorated function with retry logic

    Example:
        @retry_with_backoff(max_retries=3, base_delay=1)
        def call_api():
            response = requests.get("https://api.example.com")
            return response.json()
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt == max_retries:
                        logger.error(
                            f"{func.__name__} failed after {max_retries + 1} attempts: {e}"
                        )
                        raise

                    # Calculate delay with exponential backoff
                    delay = base_delay * (exponential_base ** attempt)
                    logger.warning(
                        f"{func.__name__} failed (attempt {attempt + 1}/{max_retries + 1}): {e}. "
                        f"Retrying in {delay:.1f}s..."
                    )
                    time.sleep(delay)

            # This should never be reached, but satisfies type checker
            if last_exception:
                raise last_exception

        return wrapper  # type: ignore
    return decorator
