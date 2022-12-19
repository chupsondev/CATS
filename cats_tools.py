import os


class COLORS:
    VIOLET = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DEF = ''


def cprint(text, color, end='\n', bold=False):
    if bold:
        color += COLORS.BOLD
    print(color + text + COLORS.ENDC, end=end)


def tabulate(text, tabs=1):
    text = text.splitlines()
    for i in range(len(text)):
        text[i] = "\t" * tabs + " " + text[i]
    return os.linesep.join(text)


def isPath(path):
    return "\\" in path or "/" in path


def isRealPath(path):
    return os.path.exists(path)


def buildFile(filePath, filePathCpp):
    print("Building " + os.path.basename(filePathCpp) + "...")
    exitCode = os.system("g++ -o " + pathify(filePath) + " " + pathify(filePathCpp))
    if exitCode != 0:
        cprint("Build failed.", COLORS.FAIL)
        return exitCode
    print("Done.")
    return exitCode


def pathify(path):
    return '"' + path + '"'
