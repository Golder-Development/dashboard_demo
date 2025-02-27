import utils.logger as logger


def log_function_call(func):
    """Decorator to log function calls, arguments, and return values."""

    def wrapper(*args, **kwargs):
        logger.info(f"Calling {func.__name__} with args={args}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} executed successfully")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
            raise e

    return wrapper
