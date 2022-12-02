from libraries import printLib as pb

import sys

from commands import testCmd


def main():
    args = sys.argv
    if len(args) <= 1:
        pb.cprint("You have to provide a command that is a part of CATS.", pb.colors.FAIL, bold=True)
        pb.cprint("Usage:", pb.colors.OKBLUE, bold=True, end=" ")
        print("cats.py <command> <command arguments>")
        return
    command = args[1]
    args = args[2:]
    if command == "test":
        testCmd.main(args)


if __name__ == "__main__":
    main()
