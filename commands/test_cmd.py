from run import TestSet
from run import TestResult
import themis_submitter
from option_lib import Option, getOption
import sys
import os
import webbrowser
from cats_tools import *


def pathify(path):
    return '"' + path + '"'


def help(options):
    cprint("Welcome to Chupson's Amazing Testing System (CATS)!", COLORS.VIOLET, bold=True)
    print("This program is designed to make testing and submitting code to themis easier. The usecase"
          "is pretty limited, so in case it's ever used by someone else, please keep in mind that there's a"
          "high chance that it won't work for you.")
    cprint("Usage:", COLORS.BLUE, bold=True, end=" ")
    cprint("cats.py <file> [options]", COLORS.DEF)
    cprint("\nOptions:", COLORS.BLUE, bold=True)
    cprint("If no options are specified, the program will run according to the settings file", COLORS.DEF, bold=True)
    for option in options:
        print(options[option])


options = {
    "build": Option("build", "Build the file (g++ compiler for c++ files)", ["-b", "--build"], True),
    "submit": Option("submit", "Submit the file to themis. You need to set your username, password and group"
                               "in the settings file.", ["-s", "--submit"], True),
    "test": Option("test", "Run only the test specified instead of all test available", ["-t", "--test"], False,
                   valueType=str),
    "verbose": Option("verbose", "Print input, output, and expected output for all failed tests", ["-v", "--verbose"],
                      True),
    "help": Option("help", "Print this help message", ["-h", "--help"], False),
}

constantSettings = {
    "maxOutputLenInTests": 10,
    "verbosePrintInput": True,
    "verbosePrintOutput": True,
    "verbosePrintExpected": True,
    "quitAfterFailedBuild": True,
}


def main(args, settings, location):
    if isArg(args[0]) and getOption(args[0], options) == "help":
        help(options)
        return

    allTestsPassed = True
    validOptionsFound = False

    optionArguments, file = getOptionsAndFileName(args, options)
    setOptions(optionArguments, options,
               settings)  # sets the options' values to those provided by the arguments, and the default
    # values if no arguments were provided

    fileNameNoExtension = file
    filePathNoExtension = os.path.join(location, fileNameNoExtension)
    fileNameExe = file + ".exe"
    filePathExe = os.path.join(location, fileNameExe)
    fileNameCpp = file + ".cpp"
    filePathCpp = os.path.join(location, fileNameCpp)

    if options["help"].getValue() == True:
        help(options)
        return

    if options["build"].getValue() == True:  # if the build option is active, build the file
        exitCode = buildFile(filePathNoExtension, filePathCpp)
        if exitCode != 0:
            return

    if options["test"].getValue() == False:
        allTestsPassed = runTests(filePathExe, fileNameCpp, fileNameNoExtension)

    if options["test"].getValue() is not False:
        runSpecificTest(filePathExe, fileNameCpp, fileNameNoExtension, options["test"].getValue())

    if options["submit"].getValue() == True:
        if allTestsPassed:  # if all tests passed, or none test were run, submit the file
            themis_submitter.sumbit(themis_submitter.auth(settings["themisUser"], settings["themisPass"])
                                    , settings["themisGroup"],
                                    os.path.basename(fileNameNoExtension),
                                    filePathExe.split(".exe")[0] + ".cpp")
        else:
            print("Not submitting because not all tests passed.")


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args, None, os.getcwd())
