#!python3

import os
import sys
from commands import test, build, run, gentest
from Command import Command
import settings_lib
import os
from cats_tools import cprint, COLORS
import options_parser


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
                    "cats.py test <file name no ext> [arguments]", ["t", "test"], test.main, test.options),
    "build": Command("build", "Buil file using g++ compiler", "cats.py build <file name no ext> [arguments]",
                     ["b", "build"], build.main, build.options),
    "run": Command("run", "Run file specified, possibly using test inputs",
                   "cats.py run <file name no ext> [arguments]",
                   ["r", "run"], run.main, run.options),
    "gentest": Command("gentest", "Generates test using the specified generator",
                       "cats.py gentest <file name no ext> [arguments]",
                       ["g", "gentest"], gentest.main, gentest.options),
}


def runCommand(command, options, settings, location):
    if command not in settings:
        settings[command] = {}
    commands[command].run(options, settings, location)


def commandIsInvalid(command):
    return command is None or command not in commands


def main():
    launchLocation = os.getcwd()
    programFolder = os.path.dirname(os.path.realpath(__file__))
    settingsFileLocation = os.path.join(programFolder, "settings.json")
    settings = settings_lib.Settings.loadSettings(commands, settingsFileLocation)

    options = sys.argv[1:]

    if len(options) < 1:
        raise NoCommandSpecified()

    aliasGiven = options[0]
    options = options[1:]

    command = Command.getCommand(aliasGiven, commands)

    if commandIsInvalid(command):
        raise InvalidCommand(aliasGiven)

    options = options_parser.OptionsParser(options, commands[command], settings[commands[command].name])

    runCommand(command, options, settings, launchLocation)


if __name__ == "__main__":
    main()
