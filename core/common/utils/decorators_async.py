import functools
import logging
import traceback
from typing import Callable

from utils.exceptions import Error

logger = logging.getLogger("buildmart")


def async_log_pre_post(func: Callable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        return result

    return wrapper


def exception_handler(func: Callable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Error:
            raise
        except ValueError as exc:
            raise Error(status_code=400, error=str(exc)) from exc
        except Exception as exc:
            logger.error("Exception in %s: %s", func.__name__, traceback.format_exc())
            raise Error(status_code=500, error=str(exc)) from exc

    return wrapper
