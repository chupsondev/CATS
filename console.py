from tests import TestSet
import os
import sys
import themis_submitter

themis_group = "SP762022_8"


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


def getOption(tag, options):
    for option in options:
        if options[option].checkForTag(tag):
            return option
    return None


def pathify(path):
    return '"' + path + '"'


def buildFile(filePath, filePathCpp):
    print("Building...")
    os.system("g++ -o " + pathify(filePath) + " " + pathify(filePathCpp))
    print("Done.")


def createTests(testFolderPath, numTests):
    if os.path.exists(testFolderPath):
        print("Test folder already exists. Adding tests is work in progress.")
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
        open(testFolderPath + "\\" + str(i) + ".in", "w").write(os.linesep.join(contents))

        print("Please enter the output for test " + str(i) + ":")
        contents = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            contents.append(line)

        open(testFolderPath + "\\" + str(i) + ".out", "w").write(os.linesep.join(contents))


def runTests(filePath, fileName, fileNameNoExtension):
    if not os.path.exists(fileName):
        print("File does not exist.")
        return
    t = TestSet(filePath, fileName, fileNameNoExtension)
    try:
        t.setTests()
    except Exception as e:
        print(e)
        return
    allPassed = True
    for test in t.tests:
        if not t.tests[test].run():
            allPassed = False
    return allPassed


def main():
    file = sys.argv[1]
    args = sys.argv[2:]

    fileNameNoExtension = file
    fileNameExe = file + ".exe"
    filePathExe = (os.getcwd() + "\\" + fileNameExe)
    fileNameCpp = file + ".cpp"
    filePathCpp = (os.getcwd() + "\\" + fileNameCpp)

    buildOpt = False
    runTestOpt = False
    createTestsOpt = False
    submitOpt = False

    options = {
        "build": Option("Build the file", ["-b", "--build"]),
        "test": Option("Run the tests", ["-t", "--test"]),
        "create": Option("Create tests", ["-c", "--create"]),
        "submit": Option("Submit the file", ["-s", "--submit"]),
        "run": Option("Run the file with input", ["-r", "--run"])
    }

    allPassed = True  # whether all tests passed

    for arg in args:
        if arg.startswith("-"):
            option = getOption(arg, options)
            if option is None:
                print("Invalid option: " + arg)
            else:
                options[option].setActive(True)
        else:
            print("Invalid option: " + arg)

    if buildOpt:
        buildFile(filePathExe, filePathCpp)

    if createTestsOpt:
        testCount = int(input("How many tests do you want to create? "))
        testFolderPath = os.getcwd() + "\\" + fileNameNoExtension + "_tests"
        createTests(testFolderPath, testCount)
    if runTestOpt:
        allPassed = runTests(filePathExe, fileNameExe, fileNameNoExtension)
    if submitOpt:
        if allPassed:
            themis_submitter.sumbit(themis_submitter.auth(), themis_group,
                                    os.path.basename(fileNameNoExtension),
                                    filePathExe.split(".exe")[0] + ".cpp")
        else:
            print("Not submitting because not all tests passed.")


if __name__ == "__main__":
    main()
