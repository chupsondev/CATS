from tests import TestSet
import os
import sys


def main():
    args = sys.argv[1:]
    if not len(args) == 1:
        print("Please provide a file.")
        return
    fileName = args[0] + ".exe"
    fileNameNoExtension = args[0]
    filePath = os.path.join(os.getcwd(), fileName)
    if not os.path.exists(fileName):
        print("File does not exist.")
        return
    t = TestSet(filePath, fileName, fileNameNoExtension)
    try:
        t.setTests()
    except Exception as e:
        print(e)
        return
    print(t.getTests())


main()
