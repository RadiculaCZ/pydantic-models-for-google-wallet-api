from collections.abc import Callable


def discovery_schema(*names: str) -> Callable[[type], type]:
    """
    Attach one or more Google API discovery schema names to a model class.

    Names may be exact schema names (for example ``JwtInsertResponse``) or
    glob-style patterns (for example ``*AddMessageResponse``).
    """

    def decorator(cls: type) -> type:
        setattr(cls, "__discovery_schemas__", tuple(names))
        return cls

    return decorator
