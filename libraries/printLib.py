import os


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DEF = ''


def cprint(text, color, end='\n', bold=False):
    if bold:
        color += colors.BOLD
    print(color + text + colors.ENDC, end=end)


def tabulate(text, tabs=1):
    text = text.splitlines()
    for i in range(len(text)):
        text[i] = "\t" * tabs + " " + text[i]
    return os.linesep.join(text)
