import functools
import logging
import traceback
from typing import Callable

from utils.exceptions import Error

logger = logging.getLogger("buildmart")


def async_log_pre_post(func: Callable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        logger.debug(">>> %s start", func.__name__)
        result = await func(*args, **kwargs)
        logger.debug(">>> %s end", func.__name__)
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
            raise Error(
                status_code=500,
                error="There is a technical issue, please contact support team",
            ) from exc

    return wrapper
