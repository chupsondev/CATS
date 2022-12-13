from libraries import print_lib as pb
import sys
from commands import test_cmd
from commands.Command import Command

commands = {
    "test": Command("test", "Test your code using a set of given inputs and expected outputs.",
                    "cats.py test <file name no ext> [arguments]", ["t"]),
    "build": Command("build", "Build your file (C++ - g++)", "cats.py build <file name no ext> [arguments]", ["b"]),
    "run": Command("run", "Run your file. Can be run for input given in test files.",
                   "cats.py run <file name no ext> [arguments]", ["r"]),
    "submit": Command("submit",
                      "Submit your file to themis. You need to set your username, password and group in the settings file.",
                      "cats.py submit <file name no ext> [arguments]", ["s"]),
    "open": Command("open", "Open the problem page on themis based on file name.",
                    "cats.py open <file name no ext> [arguments]", ["o"]),
}


def main():
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


if __name__ == "__main__":
    main()
