import functools
import click
from .scripts import check_json_file, get_role


def token_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not check_json_file():
            click.secho("You need to connect first!", fg="red")
            return
        return f(*args, **kwargs)

    return decorated_function


def role_required(allowed_role):
    def method_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_role = get_role()

            if current_role != allowed_role:
                click.secho(
                    f"You are not allow to do this action, only {allowed_role} department can do this!",
                    fg="red",
                )
                return False
            return func(*args, **kwargs)

        return wrapper

    return method_decorator
