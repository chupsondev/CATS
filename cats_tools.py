import os
import sys

from option_lib import getOption
from enum import Enum


GENERIC_TEST_FOLDER_NAMES = ['tests']

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


SUPPORTED_SOLUTION_EXT = ['.cpp', '.cc']


def cprint(text, color, end='\n', bold=False):
    if bold:
        color += COLORS.BOLD
    print(color + text + COLORS.ENDC, end=end)


def tabulate(text, tabs=1):
    if type(text) is str:
        text = text.splitlines()
    for i in range(len(text)):
        text[i] = "\t" * tabs + " " + text[i]
    return os.linesep.join(text)


def isPath(path):
    return "\\" in path or "/" in path


def isRealPath(path):
    return os.path.exists(path)


def buildFile(filePath, filePathCpp, is_cargo: bool = False):
    print("Building " + os.path.basename(filePathCpp) + "...")
    if is_cargo:
        exitCode = os.system("cargo build")
    else:
        exitCode = os.system("g++ -o " + filePath + ".exe" + " " + filePathCpp)
    if exitCode != 0:
        cprint("Build failed.", COLORS.FAIL)
        return exitCode
    print("Done.")
    return exitCode


def createTests(testFolderPath, numTests):
    maxNumberedTest = 0
    if os.path.exists(testFolderPath):
        testFiles = os.listdir(testFolderPath)
        completeTests = []
        maxNumberedTest = 0
        for file in testFiles:
            fileNoExtension = os.path.splitext(os.path.basename(file))[0]
            if fileNoExtension.isnumeric():
                if int(fileNoExtension) > maxNumberedTest:
                    maxNumberedTest = int(file.split(".")[0])
    else:
        os.mkdir(testFolderPath)
    for i in range(maxNumberedTest + 1, maxNumberedTest + numTests + 1):
        print("Please enter the input for test " + str(i) + ":")
        contents = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            contents.append(line)
        open(os.path.join(testFolderPath, str(i) + ".in"), "w").write("\n".join(contents))

        print("Please enter the output for test " + str(i) + ":")
        contents = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            contents.append(line)

        open(os.path.join(testFolderPath, str(i)) + ".out", "w").write("\n".join(contents))


"""def printTestResults(testResult: TestResult):
    tr = testResult
    if testResult.result is None:
        cprint(tr.emoji + " Test " + str(tr.testName) + " finished. Runtime: " + str(round(tr.runTime, 5)) + " seconds."
               , COLORS.BLUE, bold=True)
        cprint("\tInput:", COLORS.DEF, bold=True)
        print(tabulate(tr.input))
        cprint("\tOutput:", COLORS.DEF, bold=True)
        print(tabulate(tr.actual))
    elif testResult.result:
        cprint(tr.emoji + " Test " + str(tr.testName) + " passed. Runtime: " + str(round(tr.runTime, 5)) + " seconds.",
               COLORS.GREEN, bold=True)
    elif not testResult.result:
        cprint(tr.emoji + " Test " + str(tr.testName) + " failed. Runtime: " + str(round(tr.runTime, 5)) + " seconds.",
               COLORS.FAIL, bold=True)
        cprint("\tInput:", COLORS.DEF, bold=True)
        print(tabulate(tr.input))
        cprint("\tExpected:", COLORS.DEF, bold=True)
        print(tabulate(tr.expected))
        cprint("\tActual:", COLORS.DEF, bold=True)
        print(tabulate(tr.actual))
"""


def runTests(filePath, fileName, fileNameNoExtension):
    if not os.path.exists(fileName):
        cprint("Can't test - file does not exist.", COLORS.WARNING)
        return
    t = TestSet(filePath, fileName, fileNameNoExtension)
    if not t.setTests():
        cprint("Can't test - no valid tests found.", COLORS.WARNING)
        return
    allPassed = True
    for test in t.tests:
        tr = t.tests[test].run()
        printTestResults(tr)
        if not tr.result:
            allPassed = False
    return allPassed


def runSpecificTest(filePath, fileName, fileNameNoExtension, testCode):
    if not os.path.exists(fileName):
        cprint("Can't run test - file does not exist.", COLORS.WARNING)
        return
    t = TestSet(filePath, fileName, fileNameNoExtension)
    if not t.setTests():
        cprint("Can't run test - no valid tests found.", COLORS.WARNING)
        return
    if testCode not in t.tests:
        cprint("Can't run test - test not found.", COLORS.WARNING)
        return
    tr = t.tests[testCode].run()
    printTestResults(tr)


def runTestsWithoutResults(filePathExe):
    fileNameExe = os.path.basename(filePathExe)
    fileNameNoExtension = os.path.splitext(fileNameExe)[0]
    if not os.path.exists(fileNameExe):
        cprint("Can't run with input - file does not exist.", COLORS.WARNING)
        return
    t = TestSet(filePathExe, fileNameExe, fileNameNoExtension)
    try:
        t.setTests()
    except Exception as e:
        print(e)
        return
    for test in t.tests:
        tr = t.tests[test].runWithoutResult()
        printTestResults(tr)


def isArg(arg):
    return arg.startswith("-")


def isValidOption(option):
    return option is not None


def getOptionsAndFileName(args, options):
    validOptions = []
    nonOptionArguments = []

    for arg in args:
        if isArg(arg):
            option = getOption(arg, options)  # get the option that corresponds to the tag
            if not isValidOption(option):
                cprint("Invalid option: " + arg, COLORS.FAIL)
            else:
                optionObject = options[option]
                if optionObject.getType() is not bool:
                    if len(arg.split("=")) > 1:
                        optionObject.setValue(arg.split("=")[1])
                    else:
                        validOptions.append(option)
                else:
                    validOptions.append(option)
        else:
            nonOptionArguments.append(arg)

    file = None if len(nonOptionArguments) == 0 else nonOptionArguments[0]
    return validOptions, file


def setOptionsToDefault(options, settings):
    for option in options:
        optionName = options[option].getName() + "DefaultValue"
        options[option].setValue(settings[optionName])


def setOptions(optionArguments, options, settings):
    if len(optionArguments) == 0:
        setOptionsToDefault(options, settings)
        return
    for option in options:
        if options[option].getType() is bool:
            options[option].setValue(False)
    for optionArgument in optionArguments:
        options[optionArgument].setValue(True)


"""        def runTestsWithoutResults(filePath, fileName, fileNameNoExtension):
            if not os.path.exists(fileName):
                cprint("Can't run with input - file does not exist.", COLORS.WARNING)
                return
            t = TestSet(filePath, fileName, fileNameNoExtension)
            try:
                t.setTests()
            except Exception as e:
                print(e)
                return
            for test in t.tests:
                tr = t.tests[test].runWithoutResult()
                printTestResults(tr)"""


def runExecutable(executablePath):
    fileName = os.path.basename(executablePath)
    if not os.path.exists(executablePath):
        cprint("Can't run executable - file does not exist.", COLORS.WARNING)
        return
    cprint("Running " + fileName + "... ", COLORS.VIOLET, bold=True)
    os.system(executablePath)
    print("\nDone.")


def print_error(error):
    cprint(error, COLORS.FAIL, bold=True)


def is_valid_solution_file(file_path, accepted_extensions=SUPPORTED_SOLUTION_EXT):
    extension = os.path.splitext(file_path)[1]
    return extension in accepted_extensions


def name_from_path(path):
    return os.path.splitext(os.path.basename(path))[0]


def eval_file_candidate(candidate_path: str, goal_name: str):
    candidate = None
    if '.' in goal_name:
        candidate = os.path.basename(candidate_path)
    else:
        candidate = name_from_path(candidate_path)
    return candidate == goal_name


class FILE_ARG_TYPES(Enum):
    NAME = 1
    FULL_PATH = 2
    LOCAL_PATH = 3


def get_file_arg_type(given_input):
    if isPath(given_input):
        if os.path.exists(given_input):
            return FILE_ARG_TYPES.FULL_PATH
        else:
            return FILE_ARG_TYPES.LOCAL_PATH
    return FILE_ARG_TYPES.NAME


class SolutionFile:

    def __init__(self, given_path, MAX_SEARCH_DEPTH=4, allowed_extensions=SUPPORTED_SOLUTION_EXT):
        self.allowed_extensions = allowed_extensions

        self.MAX_SEARCH_DEPTH = MAX_SEARCH_DEPTH
        self.name = None
        self.path = None
        given_path_type = get_file_arg_type(given_path)
        self.given_path_type = given_path_type

        if given_path_type is FILE_ARG_TYPES.FULL_PATH:
            self.path = given_path
            self.set_name()

        elif given_path_type is FILE_ARG_TYPES.LOCAL_PATH:
            self.path = os.path.abspath(given_path)
            self.set_name()

        elif given_path_type is FILE_ARG_TYPES.NAME:
            self.path = self.search_for_file(given_path, os.getcwd())
            if self.path is None:
                print_error("Couldn't find provided file name in current working directory tree")
                sys.exit(1)

            self.set_name()

        self.validate_path()


    def search_for_file(self, searched_name, searched_dir, depth=0):
        if depth > self.MAX_SEARCH_DEPTH:
            return None
        for file in os.listdir(searched_dir):
            path = os.path.join(searched_dir, file)
            if is_valid_solution_file(path, self.allowed_extensions) and eval_file_candidate(path, searched_name):
                return os.path.join(searched_dir, file)
            elif os.path.isdir(file):
                subtree = self.search_for_file(searched_name, os.path.join(searched_dir, file), depth + 1)
                if subtree is not None:
                    return subtree

    def set_name(self):
        self.name = os.path.basename(self.path)
        self.name = os.path.splitext(self.name)[0]


    def validate_path(self):
        if not os.path.exists(self.path):
            print_error("Provided path doesn't exist")
            sys.exit(1)
        elif not os.path.isfile(self.path):
            print_error("Provided path is not a file")

    def get_path_without_ext(self):
        return os.path.splitext(self.path)[0]


# Searching for tests
def is_generic_tests_folder(folder_name):
    return folder_name in GENERIC_TEST_FOLDER_NAMES

def is_test_folder(tested_file_name, folder_name):
    if tested_file_name in folder_name and 'test' in folder_name:
        return True
    return False

def search_generic_tests_folder(tested_file_name, directory, level=0, MAX_SEARCH_DEPTH=4):
    test_folders = []
    if level > MAX_SEARCH_DEPTH:
        return test_folders
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isdir(file_path):
            if file == tested_file_name:
                test_folders.append(file_path)
            else:
                test_folders += (search_generic_tests_folder(tested_file_name, file_path, level + 1, MAX_SEARCH_DEPTH))
    return test_folders

def find_test_folders(tested_file_name, directory, level=0, MAX_SEARCH_DEPTH=4):
    """
    Recursively searches for all test folders named correctly that could potentially contain tests.
    Returns list of folder paths.
    :rtype: list
    :arg directory: directory to search in
    :arg level: current search depth
    :return: list of test folders
    """
    test_folders = []
    if level > MAX_SEARCH_DEPTH:
        return test_folders
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isdir(file_path):
            if is_test_folder(tested_file_name, file):
                test_folders.append(file_path)
            elif is_generic_tests_folder(file):
                test_folders += search_generic_tests_folder(tested_file_name, file_path, level + 1, MAX_SEARCH_DEPTH)
            else:
                test_folders += find_test_folders(tested_file_name, file_path, level + 1)
    return test_folders
