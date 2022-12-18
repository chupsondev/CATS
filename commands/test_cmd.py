from run import TestSet
from run import TestResult
import themis_submitter
from cats import tabulate, cprint, COLORS
from option_lib import Option, getOption
import sys
import os
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


def runTestsWithoutResults(filePath, fileName, fileNameNoExtension):
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
        printTestResults(tr)


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


def isArg(arg):
    return arg.startswith("-")


def isValidOption(option):
    return options is not None


def getOptionsAndFileName(args):
    validOptions = []
    nonOptionArguments = []

    for arg in args:
        if isArg(arg):
            option = getOption(arg, options)  # get the option that corresponds to the tag
            if not isValidOption(option):
                cprint("Invalid option: " + arg, COLORS.FAIL)
            else:
                if option.getType() is not bool:
                    option.setValue(arg.split("=")[1])
                else:
                    validOptions.append(option)
        else:
            nonOptionArguments.append(arg)

    file = None if len(nonOptionArguments) == 0 else nonOptionArguments[0]
    return validOptions, file


def setOptionsToDefault(options, settings):
    for option in options:
        optionName = options[option].getName()
        options[option].setValue(settings[optionName])


def setOptions(optionArguments, options, settings):
    if len(optionArguments) == 0:
        setOptionsToDefault(options, settings)
        return
    for optionArgument in optionArguments:
        options[optionArgument].setValue(True)


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
}


def main(args, settings, location):
    if getOption(args[0], options) == "help":
        help(options)
        return

    allTestsPassed = True
    validOptionsFound = False

    optionArguments, file = getOptionsAndFileName(args)
    setOptions(optionArguments, options,
               settings)  # sets the options' values to those provided by the arguments, and the default
    # values if no arguments were provided

    fileNameNoExtension = file
    fileNameExe = file + ".exe"
    filePathExe = (os.getcwd() + "\\" + fileNameExe)
    fileNameCpp = file + ".cpp"
    filePathCpp = (os.getcwd() + "\\" + fileNameCpp)

    if options["help"].active:
        help(options)
        return

    if options["build"].getValue() == True:  # if the build option is active, build the file
        buildFile(filePathExe, filePathCpp)

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
