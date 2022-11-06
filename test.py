from os import listdir
from os import path


class Test:
    def __init__(self, filePath, fileName, fileNameNoExtension):
        self.tests = None
        self.filePath = filePath
        self.fileName = fileName
        self.fileNameNoExtension = fileNameNoExtension

    def setTests(self):
        filePath = self.filePath
        testsPath = path.join(path.dirname(filePath), self.fileNameNoExtension + "_tests")
        self.tests = [path.join(testsPath, f) for f in listdir(testsPath) if path.isfile(path.join(testsPath, f))]
        for test in self.tests:
            if not test.endswith(".in") or not test.endswith(".out"):
                self.tests.remove(test)
        if len(self.tests) % 2 != 0:
            self.tests = None
            raise Exception("There are an odd number of tests for this file.")
        if len(self.tests) == 0:
            self.tests = None
            raise Exception("There are no tests for this file.")
        return self.tests

    def getTests(self):
        self.setTests()
        return self.tests
