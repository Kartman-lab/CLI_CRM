from functools import wraps
import sentry_sdk

def sentry_wrap(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise
    return wrapper