from libraries.run import TestSet
from libraries.run import TestResult
from libraries import themis_submitter
from libraries.print_lib import cprint, tabulate, colors
from libraries.option_lib import Option, getOption
from libraries.settings_lib import loadSettings
import os
import sys
import json
import webbrowser


def pathify(path):
    return '"' + path + '"'


def buildFile(filePath, filePathCpp):
    print("Building " + os.path.basename(filePathCpp) + "...")
    os.system("g++ -o " + pathify(filePath) + " " + pathify(filePathCpp))
    print("Done.")


def createTests(testFolderPath, numTests):
    maxNumberedTest = 0
    if os.path.exists(testFolderPath):
        testFiles = os.listdir(testFolderPath)
        completeTests = []
        maxNumberedTest = 0
        for file in testFiles:
            if file.split(".")[0].isnumeric():
                if int(file.split(".")[0]) > maxNumberedTest:
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
        open(testFolderPath + "\\" + str(i) + ".in", "w").write("\n".join(contents))

        print("Please enter the output for test " + str(i) + ":")
        contents = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            contents.append(line)

        open(testFolderPath + "\\" + str(i) + ".out", "w").write("\n".join(contents))


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


def main(args):
    options = {
        "settings": Option("Opens the settings file in notepad", ["-se", "--settings"]),
        "settingsPrint": Option("Prints the settings file", ["-sp", "--settings-print"]),
        "settingsHelp": Option("Prints the settings file help", ["-sh", "--settings-help"]),
        "build": Option("Build the file (g++ compiler for c++ files)", ["-b", "--build"]),
        "test": Option("Run the tests and compare result to expected result", ["-t", "--test"]),
        "create": Option("Create tests", ["-c", "--create"]),
        "submit": Option("Submit the file to themis. You need to set your username, password and group"
                         "in the settings file.", ["-s", "--submit"]),
        "runInput": Option("Run the file with inputs from tests", ["-ri", "--run-input"]),
        "run": Option("Run the file", ["-r", "--run"]),
        "problem": Option("Open the problem page on themis based on file name", ["-pr", "--problem"]),
        "help": Option("Show this help message", ["-h", "--help", "-?", "--?", "-wtf", "--wtf"])
    }

    settings = loadSettings(options)

    if getOption(args[0], options) == "help":
        help(options)
        return
    file = args[0]

    if len(args) <= 2:
        for option in options:
            if option + "DefaultValue" in settings and settings[option + "DefaultValue"]:
                options[option].setActive(True)

    args = args[1:]

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
            themis_submitter.sumbit(themis_submitter.auth(settings["themisUser"], settings["themisPass"])
                                    , settings["themisGroup"],
                                    os.path.basename(fileNameNoExtension),
                                    filePathExe.split(".exe")[0] + ".cpp")
        else:
            print("Not submitting because not all tests passed.")

    if options["problem"].active:
        webbrowser.open("https://themis.ii.uni.wroc.pl/{}/".format(settings["themisGroup"]) + fileNameNoExtension)


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
