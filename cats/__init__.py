#!python3

import os
import sys
from cats.commands import test, build, run, gentest
from cats.Command import Command
from cats import settings_lib
from cats.cats_tools import cprint, COLORS, tabulate
from cats import options_parser


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


def help(options: options_parser.OptionsParser, settings, location):
    option_parser_obj = options
    args = option_parser_obj.get_arguments()
    queried_command = args[0] if len(args) > 0 else "help"
    queried_command = Command.getCommand(queried_command, commands)
    queried_command: Command = commands[queried_command]

    cprint("This is a help message for CATS -- Competitive Algorithm Tool Set", COLORS.VIOLET, bold=True)
    cprint("Usage: ", COLORS.DEF, bold=True)
    print(tabulate(queried_command.usage))
    if len(queried_command.options) > 0:
        cprint("Options: ", COLORS.DEF, bold=True)
    for option in queried_command.options:
        option = queried_command.options[option]
        option_print = f'{option.name} - {option.description} (default: {option.defaultValue})'
        print(tabulate(option_print))

    if queried_command.name == "help":
        cprint("Available commands: ", COLORS.DEF, bold=True)
        for command in commands:
            print(tabulate(f'{command} -- {commands[command].description}'))


commands = {
    "test": Command("test", "Test your code using a set of given inputs and expected outputs.",
                    "cats.py test <file name no ext> [options]", ["t", "test"], test.main, test.options),
    "build": Command("build", "Buil file using g++ compiler", "cats.py build <file name no ext> [options]",
                     ["b", "build"], build.main, build.options),
    "run": Command("run", "Run file specified, possibly using test inputs",
                   "cats.py run <file name no ext> [options]",
                   ["r", "run"], run.main, run.options),
    "gentest": Command("gentest", "Generates test using the specified generator",
                       "cats.py gentest <file name no ext> [options]",
                       ["g", "gentest"], gentest.main, gentest.options),
    "help": Command("help", "Prints this help message or help message for another command",
                    "cats.py help <name of command>", ["h", "help"], help, dict())
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

    options = options_parser.OptionsParser(options, commands[command],
                                           settings[commands[command].name] if commands[command].name in settings
                                           else dict())

    runCommand(command, options, settings, launchLocation)


if __name__ == "__main__":
    main()
