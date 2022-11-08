from tests import TestSet
import os
import sys


def main():
    args = sys.argv[1:]
    action = args[0]
    fileName = args[1] + ".exe"
    fileNameNoExtension = args[1]
    filePath = os.path.join(os.getcwd(), fileName)
    if action == "b":
        print("Building...")
        os.system("g++ -o " + filePath + " " + filePath.split(".")[0] + ".cpp")
        print("Done.")
    elif action == "n":
        pass
    elif action.startswith("t"):
        testFolderPath = os.getcwd()+ "\\" + args[1] + "_tests"
        try:
            os.mkdir(testFolderPath)
        except Exception as e:
            print(e)
        for i in range(1, int(action.split("t")[1]) + 1):
            open(testFolderPath + "\\" + str(i) + ".in", "w")
            open(testFolderPath + "\\" + str(i) + ".out", "w")
        return

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
        t.tests[test].run()


main()
