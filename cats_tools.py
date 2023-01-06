import os
from option_lib import getOption
from run import TestSet, TestResult, Test


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


def cprint(text, color, end='\n', bold=False):
    if bold:
        color += COLORS.BOLD
    print(color + text + COLORS.ENDC, end=end)


def tabulate(text, tabs=1):
    text = text.splitlines()
    for i in range(len(text)):
        text[i] = "\t" * tabs + " " + text[i]
    return os.linesep.join(text)


def isPath(path):
    return "\\" in path or "/" in path


def isRealPath(path):
    return os.path.exists(path)


def buildFile(filePath, filePathCpp):
    print("Building " + os.path.basename(filePathCpp) + "...")
    exitCode = os.system("g++ -o " + pathify(filePath) + " " + pathify(filePathCpp))
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

def pathify(path):
    return '"' + path + '"'

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


def runExecutable(executablePath):
    fileName = os.path.basename(executablePath)
    if not os.path.exists(executablePath):
        cprint("Can't run executable - file does not exist.", COLORS.WARNING)
        return
    cprint("Running " + fileName + "... ", COLORS.VIOLET, bold=True)
    os.system(executablePath)
    print("\nDone.")
