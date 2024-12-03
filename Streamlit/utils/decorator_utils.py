from functools import wraps
from exceptions import NotFoundException


def check_data_variables(*required_keys):
    def decorator(func):
        @wraps(func)
        def wrapper(self, data, *args, **kwargs):
            missing_keys = [key for key in required_keys if data.get(key) is None]
            if missing_keys:
                raise NotFoundException(f"{', '.join(missing_keys)} not found.")
            return func(self, data, *args, **kwargs)

        return wrapper

    return decorator