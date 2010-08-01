import sys, tty, termios

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def getch_arrow():
    esc = '\x1b'
    a = getch()
    if a == esc:
        b = getch()
        if b == '[':
            c = getch()
            return {
                'A': 'up',
                'B': 'down',
                'C': 'right',
                'D': 'left',
            }.get(c, a)
    return a
