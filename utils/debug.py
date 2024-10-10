DEBUG = False

def debug_print(*args, **kwargs):
    """Prints messages only if is_print_enabled is True."""
    if DEBUG:
        print(*args, **kwargs)