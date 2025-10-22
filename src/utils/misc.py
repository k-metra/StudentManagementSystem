import sys

def clear_input_buffer():
    """Clear any remaining input in the buffer to prevent interference from keyboard events"""
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        # For non-Windows systems
        import termios, tty
        sys.stdin.flush()

def enter_to_continue():
    input("Press enter to continue.")