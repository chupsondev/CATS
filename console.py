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


def runTestsWithoutResults(filePath, fileName, fileNameNoExtension):
    if not os.path.exists(fileName):
        print("File does not exist.")
        return
    t = TestSet(filePath, fileName, fileNameNoExtension)
    try:
        t.setTests()
    except Exception as e:
        print(e)
        return
    for test in t.tests:
        print("\tOutput: \n" + '\t' + t.tests[test].runWithoutResult())


def main():
    file = sys.argv[1]
    args = sys.argv[2:]

    fileNameNoExtension = file
    fileNameExe = file + ".exe"
    filePathExe = (os.getcwd() + "\\" + fileNameExe)
    fileNameCpp = file + ".cpp"
    filePathCpp = (os.getcwd() + "\\" + fileNameCpp)

    options = {
        "build": Option("Build the file", ["-b", "--build"]),
        "test": Option("Run the tests and compare result to expected result", ["-t", "--test"]),
        "create": Option("Create tests", ["-c", "--create"]),
        "submit": Option("Submit the file", ["-s", "--submit"]),
        "runInput": Option("Run the file with inputs from tests", ["-i", "--input"]),
        "run": Option("Run the file", ["-r", "--run"]),
        "help": Option("Show this help message", ["-h", "--help", "-?", "--?", "-wtf", "--wtf"])
    }

    allPassed = True  # whether all tests passed. set to True in case no tests are run

    for arg in args:
        if arg.startswith("-"):
            option = getOption(arg, options)  # get the option that corresponds to the tag
            if option is None:
                print("Invalid option: " + arg)
            else:
                options[option].setActive(True)  # if there is an option for the tag given, set it to active
        else:
            print("Invalid option: " + arg)

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
        print("Running " + fileNameExe + "." + " Please enter input below if needed.")
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
