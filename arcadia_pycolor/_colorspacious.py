import warnings

with warnings.catch_warnings():
    # colorspacious uses invalid escape sequences in docstrings (e.g. `\Delta`).
    # On Python 3.12+ these emit SyntaxWarning at compile time; on 3.10-3.11 they
    # emit DeprecationWarning. A module filter does not match compile-time warnings.
    warnings.filterwarnings("ignore", message="invalid escape sequence")
    from colorspacious import cspace_convert, cspace_converter  # type: ignore

__all__ = ["cspace_convert", "cspace_converter"]
