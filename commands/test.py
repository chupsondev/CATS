from run import Tests
from run import TestResult
import themis
from option_lib import Option, getOption
import sys
import os
import webbrowser
from cats_tools import *
import options_parser

INFINITY = 99999999

def pathify(path):
    return '"' + path + '"'



options = {
    "build": Option("build", "Build the file (g++ compiler for c++ files)", ["-b", "--build"], True),
    "submit": Option("submit", "Submit the file to themis. You need to set your username, password and group"
                               "in the settings file.", ["-s", "--submit"], True),
    "test": Option("test", "Run only the test specified instead of all test available", ["-t", "--test"], False,
                   valueType=str),
    "verbose": Option("verbose", "Print all information available", ["-v", "--verbose"],
                      False),
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
        themis_group: str = settings["themisgroup"]
        themis_user: str = settings["themisuser"]
        themis_pass: str = settings["themispass"]
    except KeyError:
        themis_group: str = ""
        themis_user: str = ""
        themis_pass: str = ""

    settings = settings["test"]
    options = current_options.get_options()

    allTestsPassed = True
    validOptionsFound = False
    
    file = current_options.get_arguments()[0]

    # okay so before i do this i want to apologise to myself and anyone else who might be reading this code
    # what follows is the result of me being to lazy to do this thing in a better way
    # i only need this functionality for a very specific use-case that neither me nor anyone else will probably
    # ever encounter again

    build_cargo: bool = False
    if len(file.split(".")) >= 2 and file.split(".")[1] == "cargo":
        build_cargo = True
        filePathNoExtension = os.path.join(os.getcwd(), "target/debug/")
        filePathNoExtension = os.path.join(filePathNoExtension, file.split(".")[0])
        filePathCpp = filePathNoExtension

    else:
        tested_solution = SolutionFile(file)
        fileNameNoExtension = tested_solution.name
        filePathNoExtension = tested_solution.get_path_without_ext()
        fileNameExe = tested_solution.name + ".exe"
        filePathExe = tested_solution.get_path_without_ext() + ".exe"
        fileNameCpp = tested_solution.name
        filePathCpp = tested_solution.path




    if options["build"].getValue() == True:  # if the build option is active, build the file
        exitCode = buildFile(filePathNoExtension, filePathCpp, build_cargo)
        if exitCode != 0:
            return

    suffix = "" if build_cargo else ".exe"
    tests = Tests(filePathNoExtension + suffix, full_verbosity=options["verbose"].getValue(),
                  max_num_unshortened_lines=INFINITY if options["verbose"].getValue() else 15)
    tests.set_tests(location)

    if options["test"].getValue() == False:
        allTestsPassed = tests.run_tests()

    if options["test"].getValue() is not False:
        allTestsPassed = tests.run_test(options["test"].getValue())

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
