import os
import sys
from commands import test_cmd
from Command import Command
import settings_lib
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


class CATSException(Exception):
    pass


class NoCommandSpecified(CATSException):
    def __init__(self):
        cprint("You have to provide a command that is a part of CATS.", COLORS.FAIL, bold=True)
        cprint("Usage:", COLORS.BLUE, bold=True, end=" ")
        print("cats.py <command> <command arguments>")


class InvalidCommand(CATSException):
    def __init__(self, command):
        cprint("Invalid command: " + command, COLORS.FAIL)


commands = {
    "test": Command("test", "Test your code using a set of given inputs and expected outputs.",
                    "cats.py test <file name no ext> [arguments]", ["t"], test_cmd.main, test_cmd.options),
}


def runCommand(command, args, settings, location):
    commands[command].run(args, settings[command], location)


def commandIsInvalid(command):
    return command is None or command not in commands


def main():
    launchLocation = os.getcwd()
    programFolder = os.path.dirname(os.path.realpath(__file__))
    settingsFileLocation = os.path.join(programFolder, "settings.json")
    settings = settings_lib.Settings.loadSettings(commands, settingsFileLocation)

    args = sys.argv[1:]

    if len(args) < 1:
        raise NoCommandSpecified()

    aliasGiven = args[0]
    args = args[1:]

    command = Command.getCommand(aliasGiven, commands)

    if commandIsInvalid(command):
        raise InvalidCommand(aliasGiven)

    runCommand(command, args, settings, launchLocation)


if __name__ == "__main__":
    main()
