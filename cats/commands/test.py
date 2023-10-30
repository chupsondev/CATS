from cats.run import Tests
from cats.run import TestResult
from cats import themis
from cats.option_lib import Option, getOption
import sys
import os
import webbrowser
from cats.cats_tools import *
from cats import options_parser


def pathify(path):
    return '"' + path + '"'



options = {
    "build": Option("build", "Build the file (g++ compiler for c++ files)", ["-b", "--build"], True),
    "submit": Option("submit", "Submit the file to themis. You need to set your username, password and group"
                               "in the settings file.", ["-s", "--submit"], True),
    "test": Option("test", "Run only the test specified instead of all test available", ["-t", "--test"], False,
                   valueType=str),
    "verbose": Option("verbose", "Print input, output, and expected output for all failed tests", ["-v", "--verbose"],
                      True),
}

constantSettings = {
    "maxOutputLenInTests": 10,
    "verbosePrintInput": True,
    "verbosePrintOutput": True,
    "verbosePrintExpected": True,
    "quitAfterFailedBuild": True,
}


def main(current_options: options_parser.OptionsParser, settings, location):
    try:
        themis_group: str = settings["themisGroup"]
        themis_user: str = settings["themisUser"]
        themis_pass: str = settings["themisPass"]
    except KeyError:
        pass
    settings = settings["test"]
    options = current_options.get_options()

    allTestsPassed = True
    validOptionsFound = False
    
    file = current_options.get_arguments()[0]

    tested_solution = SolutionFile(file)
    fileNameNoExtension = tested_solution.name
    filePathNoExtension = tested_solution.get_path_without_ext()
    fileNameExe = tested_solution.name + ".exe"
    filePathExe = tested_solution.get_path_without_ext() + ".exe"
    fileNameCpp = tested_solution.name
    filePathCpp = tested_solution.path



    if options["build"].getValue() == True:  # if the build option is active, build the file
        exitCode = buildFile(filePathNoExtension, filePathCpp)
        if exitCode != 0:
            return

    tests = Tests(filePathNoExtension + ".exe")
    tests.set_tests(location)

    if options["test"].getValue() == False:
        allTestsPassed = tests.run_tests()
        tests.print_results()

    if options["test"].getValue() is not False:
        allTestsPassed = tests.run_test(options["test"].getValue())
        tests.print_results()

    if options["submit"].getValue() == True:
        if allTestsPassed:  # if all tests passed, or none test were run, submit the file
            themis_client = themis.Themis(themis_user, themis_pass)
            print("Submitting...\n")
            themis_client.submit(themis_group, tested_solution.name, tested_solution.path) \
                .print_result()
        else:
            print("Not submitting because not all tests passed.")


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args, None, os.getcwd())
