from collections.abc import Callable


def discovery_schema[T](*names: str) -> Callable[[T], T]:
    """
    Attach one or more Google API discovery schema names to a model class.

    Names may be exact schema names (for example ``JwtInsertResponse``) or
    glob-style patterns (for example ``*AddMessageResponse``).
    """

    def decorator(cls: T) -> T:
        setattr(cls, "__discovery_schemas__", tuple(names))
        return cls

    return decorator
