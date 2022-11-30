from tests import TestSet
from tests import TestResult
import os
import sys
import themis_submitter
import json

themis_group = "SP762022_8"


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DEF = ''


def cprint(text, color, end='\n', bold=False):
    if bold:
        color += colors.BOLD
    print(color + text + colors.ENDC, end=end)


def tabulate(text, tabs=1):
    text = text.splitlines()
    for i in range(len(text)):
        text[i] = "\t" * tabs + " " + text[i]
    return os.linesep.join(text)


class Option:
    def __init__(self, description, tags, active=False):
        self.tags = tags
        self.description = description
        self.active = active

    def setTags(self, tags):
        self.tags = tags

    def setDescription(self, description):
        self.description = description

    def setActive(self, active):
        self.active = active

    def checkForTag(self, tag):
        if tag in self.tags:
            return True
        return False

    def __str__(self):
        return f"{self.tags} - {self.description}"


def getOption(tag, options):
    for option in options:
        if options[option].checkForTag(tag):
            return option
    return None


def pathify(path):
    return '"' + path + '"'


def buildFile(filePath, filePathCpp):
    print("Building " + os.path.basename(filePathCpp) + "...")
    os.system("g++ -o " + pathify(filePath) + " " + pathify(filePathCpp))
    print("Done.")


def createTests(testFolderPath, numTests):
    if os.path.exists(testFolderPath):
        print("Test folder already exists. Adding tests is work in progress.", colors.WARNING)
        return
    os.mkdir(testFolderPath)
    for i in range(1, numTests + 1):
        print("Please enter the input for test " + str(i) + ":")
        contents = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            contents.append(line)
        open(testFolderPath + "\\" + str(i) + ".in", "w").write("".join(contents))

        print("Please enter the output for test " + str(i) + ":")
        contents = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            contents.append(line)

        open(testFolderPath + "\\" + str(i) + ".out", "w").write("".join(contents))


def printTestResults(testResult: TestResult):
    tr = testResult
    if testResult.result is None:
        cprint(tr.emoji + " Test " + str(tr.testName) + " finished. Runtime: " + str(round(tr.runTime, 5)) + " seconds."
               , colors.OKBLUE, bold=True)
        cprint("\tInput:", colors.DEF, bold=True)
        print(tabulate(tr.input))
        cprint("\tOutput:", colors.DEF, bold=True)
        print(tabulate(tr.actual))
    elif testResult.result:
        cprint(tr.emoji + " Test " + str(tr.testName) + " passed. Runtime: " + str(round(tr.runTime, 5)) + " seconds.",
               colors.OKGREEN, bold=True)
    elif not testResult.result:
        cprint(tr.emoji + " Test " + str(tr.testName) + " failed. Runtime: " + str(round(tr.runTime, 5)) + " seconds.",
               colors.FAIL, bold=True)
        cprint("\tInput:", colors.DEF, bold=True)
        print(tabulate(tr.input))
        cprint("\tExpected:", colors.DEF, bold=True)
        print(tabulate(tr.expected))
        cprint("\tActual:", colors.DEF, bold=True)
        print(tabulate(tr.actual))


def runTests(filePath, fileName, fileNameNoExtension):
    if not os.path.exists(fileName):
        cprint("Can't test - file does not exist.", colors.WARNING)
        return
    t = TestSet(filePath, fileName, fileNameNoExtension)
    if not t.setTests():
        cprint("Can't test - no valid tests found.", colors.WARNING)
        return
    allPassed = True
    for test in t.tests:
        tr = t.tests[test].run()
        printTestResults(tr)
        if not tr.result:
            allPassed = False
    return allPassed


def runTestsWithoutResults(filePath, fileName, fileNameNoExtension):
    if not os.path.exists(fileName):
        cprint("Can't run with input - file does not exist.", colors.WARNING)
        return
    t = TestSet(filePath, fileName, fileNameNoExtension)
    try:
        t.setTests()
    except Exception as e:
        print(e)
        return
    for test in t.tests:
        tr = t.tests[test].runWithoutResult()
        printTestResults(tr)


def help(options):
    cprint("Welcome to Chupson's Amazing Testing System (CATS)!", colors.HEADER, bold=True)
    print("This program is designed to make testing and submitting code to themis easier. The usecase"
          "is pretty limited, so in case it's ever used by someone else, please keep in mind that there's a"
          "high chance that it won't work for you.")
    cprint("Usage:", colors.OKBLUE, bold=True, end=" ")
    cprint("cats.py <file> [options]", colors.DEF)
    cprint("\nOptions:", colors.OKBLUE, bold=True)
    cprint("If no options are specified, the program will run according to the settings file", colors.DEF, bold=True)
    for option in options:
        print(options[option])


def loadSettings(options):
    defaultSettings = {
        "themisUser" : "",
        "themisPass" : "",
        "themisGroup" : "",
        "buildDefaultValue" : True,
        "testDefaultValue" : True,
    }
    for option in options:
        if option + "DefaultValue" not in defaultSettings:
            defaultSettings[option+"DefaultValue"] = False
    if not os.path.exists("settings.json"):
        open("settings.json", "w").write(json.dumps(defaultSettings, indent=4))
    return json.load(open("settings.json", "r"))


def main():
    options = {
        "settings": Option("Opens the settings file in notepad", ["-s", "--settings"]),
        "settingsPrint": Option("Prints the settings file", ["-sp", "--settings-print"]),
        "settingsHelp": Option("Prints the settings file help", ["-sh", "--settings-help"]),
        "build": Option("Build the file (g++ compiler for c++ files)", ["-b", "--build"]),
        "test": Option("Run the tests and compare result to expected result", ["-t", "--test"]),
        "create": Option("Create tests", ["-c", "--create"]),
        "submit": Option("Submit the file to themis. You need to set your username, password and group"
                         "in the settings file.", ["-s", "--submit"]),
        "runInput": Option("Run the file with inputs from tests", ["-ri", "--run-input"]),
        "run": Option("Run the file", ["-r", "--run"]),
        "help": Option("Show this help message", ["-h", "--help", "-?", "--?", "-wtf", "--wtf"])
    }

    settings = loadSettings(options)

    if getOption(sys.argv[1], options) == "help":
        help(options)
        return
    file = sys.argv[1]

    args = []
    if len(sys.argv) <= 2:
        for option in options:
            if option + "DefaultValue" in settings and settings[option + "DefaultValue"]:
                options[option].setActive(True)
    else:
        args = sys.argv[2:]

    fileNameNoExtension = file
    fileNameExe = file + ".exe"
    filePathExe = (os.getcwd() + "\\" + fileNameExe)
    fileNameCpp = file + ".cpp"
    filePathCpp = (os.getcwd() + "\\" + fileNameCpp)

    allPassed = True  # whether all tests passed. set to True in case no tests are run

    for arg in args:
        if arg.startswith("-"):
            option = getOption(arg, options)  # get the option that corresponds to the tag
            if option is None:
                cprint("Invalid option: " + arg, colors.FAIL)
            else:
                options[option].setActive(True)  # if there is an option for the tag given, set it to active
        else:
            cprint("Invalid option: " + arg, colors.FAIL)

    if options["settings"].active:
        programFolder = os.path.dirname(os.path.realpath(__file__))
        settingsFile = pathify(programFolder + "\\settings.json")
        os.system(f"notepad {settingsFile}")

    if options["settingsPrint"].active:
        cprint("Settings:", colors.OKBLUE, bold=True)
        for setting in settings:
            cprint(setting + ":", colors.DEF, bold=True, end=" ")
            print(settings[setting])

    if options["settingsHelp"].active:
        cprint("Settings descriptions:", colors.OKBLUE, bold=True)
        print("themisUser: Your themis username")
        print("themisPass: Your themis password")
        print("themisGroup: The group you want to submit to")
        print("{option}DefaultValue: Whether the option should be on if no arguments are given")

    if options["help"].active:
        help(options)
        return

    if options["create"].active:  # if the create option is active, create tests
        testCount = int(input("How many tests do you want to create? "))
        testFolderPath = os.getcwd() + "\\" + fileNameNoExtension + "_tests"
        createTests(testFolderPath, testCount)

    if options["build"].active:  # if the build option is active, build the file
        buildFile(filePathExe, filePathCpp)

    if options["test"].active:  # if the test option is active, run the tests and compare the output to the expected
        # output
        allPassed = runTests(filePathExe, fileNameExe, fileNameNoExtension)  # runTests returns whether all tests passed

    if options["runInput"].active:  # if the run option is active, run the file without comparing output to expected
        # output
        runTestsWithoutResults(filePathExe, fileNameExe, fileNameNoExtension)

    if options["run"].active:  # if the run option is active, run the file without input
        cprint("Running " + fileNameExe + "." + " Please enter input below if needed.", colors.HEADER, bold=True)
        os.system(pathify(filePathExe))
        print("\nDone.")

    if options["submit"].active:
        if allPassed:  # if all tests passed, or none test were run, submit the file
            themis_submitter.sumbit(themis_submitter.auth(), themis_group,
                                    os.path.basename(fileNameNoExtension),
                                    filePathExe.split(".exe")[0] + ".cpp")
        else:
            print("Not submitting because not all tests passed.")


if __name__ == "__main__":
    main()
