import os
import print_lib as pb
import sys
from commands import test_cmd
from Command import Command
import settings_lib

commands = {
    "test": Command("test", "Test your code using a set of given inputs and expected outputs.",
                    "cats.py test <file name no ext> [arguments]", ["t"], test_cmd.main, test_cmd.options),
}


def main():
    launchLocation = os.getcwd()
    programFolder = os.path.dirname(os.path.realpath(__file__))
    settingsFileLocation = os.path.join(programFolder, "settings.json")
    settings = settings_lib.Settings.loadSettings(commands, settingsFileLocation)
    args = sys.argv
    if len(args) <= 1:
        pb.cprint("You have to provide a command that is a part of CATS.", pb.colors.FAIL, bold=True)
        pb.cprint("Usage:", pb.colors.OKBLUE, bold=True, end=" ")
        print("cats.py <command> <command arguments>")
        return
    aliasGiven = args[1]
    args = args[2:]

    command = Command.getCommand(aliasGiven, commands)
    if command is None:
        pb.cprint("Invalid command: " + aliasGiven, pb.colors.FAIL)
        return
    commands[command].run(args, settings, launchLocation)

if __name__ == "__main__":
    main()
