import os
import time
from os import listdir
from os import path
from subprocess import Popen, PIPE
import themis_submitter


class TestSet:
    def __init__(self, filePath, fileName, fileNameNoExtension):
        self.testsRaw = None
        self.tests = None
        self.filePath = filePath
        self.fileName = fileName
        self.fileNameNoExtension = fileNameNoExtension

    def setTests(self):
        filePath = self.filePath
        testsPath = path.join(path.dirname(filePath), self.fileNameNoExtension + "_tests")
        self.testsRaw = [path.join(testsPath, f) for f in listdir(testsPath) if path.isfile(path.join(testsPath, f))]
        self.tests = {}

        for test in self.testsRaw:
            if not test.endswith(".in") and not test.endswith(".out"):
                self.testsRaw.remove(test)
                continue
            if test.endswith(".in"):
                if self.tests.get(path.basename(test).split(".")[0]) is None:
                    self.tests[path.basename(test).split(".")[0]] = Test(test, None, self.filePath)
                else:
                    self.tests[path.basename(test).split(".")[0]].input = test
            elif test.endswith(".out"):
                if self.tests.get(path.basename(test).split(".")[0]) is None:
                    self.tests[path.basename(test).split(".")[0]] = Test(None, test, self.filePath)
                else:
                    self.tests[path.basename(test).split(".")[0]].output = test
        for test in self.tests:
            if self.tests[path.basename(test).split(".")[0]].input is None or self.tests[path.basename(test).split(".")[0]].output is None:
                self.tests[path.basename(test).split(".")[0]] = None
                print("Test " + str(test) + " is missing an input or output file.")
        if len(self.tests) == 0:
            self.tests = None
            raise Exception("There are no tests for this file, or some tests are incomplete.")

    def getTests(self):
        self.setTests()
        return self.tests




class Test:
    def __init__(self, input, output, testedFilePath):
        self.input = input
        self.output = output
        self.testedFilePath = testedFilePath

    def run(self):
        timeStarted = time.time()
        p = Popen([self.testedFilePath], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        output = p.communicate(os.linesep.join(open(self.input).readlines()).encode())[0].decode()
        timeEnded = time.time()
        runTime = timeEnded - timeStarted
        if output.split() == open(self.output).read().split():
            print("✅  Test " + str(path.basename(self.input).split(".")[0]) + " passed. Runtime: " + str(round(runTime, 10)) + " seconds.")

            return True
        else:
            print("❌  Test " + str(path.basename(self.input).split(".")[0]) + " failed. Runtime: " + str(round(runTime, 10)) + " seconds.")
            print("\tExpected output: \n" + open(self.output).read())
            print("\tActual output:\n " + str(output))
            return False

    def compareOutpusts(self, out1, out2):
        out1Code = out1.encode()
        out2Code = out2.encode()

        isSame = True

        index = 0

        for i in range(len(out1Code)):
            print(out1Code)
            if out1Code[i] != out2Code[index] and out1Code[i] != "\r":
                isSame = False
                return isSame
            index += 1
            if out1Code[i] == "\r":
                index -= 1
        return isSame
