import os
import sys
from commands import test_cmd, build_cmd, run_cmd
from Command import Command
import settings_lib
import os
from cats_tools import cprint, COLORS


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
                    "cats.py test <file name no ext> [arguments]", ["t", "test"], test_cmd.main, test_cmd.options),
    "build": Command("build", "Buil file using g++ compiler", "cats.py build <file name no ext> [arguments]",
                     ["b", "build"], build_cmd.main, build_cmd.options),
    "run": Command("run", "Run file specified, possibly using test inputs",
                   "cats.py run <file name no ext> [arguments]",
                   ["r", "run"], run_cmd.main, run_cmd.options)
}


def runCommand(command, args, settings, location):
    if command not in settings:
        settings[command] = {}
    commands[command].run(args, settings[commands[command].getName()], location)


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
