from tests import TestSet
import os
import sys
import themis_submitter


def main():
    global action
    args = sys.argv[1:]
    try:
        action = args[0]
    except Exception as e:
        pass
    fileName = args[1] + ".exe"
    fileNameNoExtension = args[1]
    filePath = (os.getcwd() + "\\" + fileName)
    if action == "b":
        print("Building...")
        os.system("g++ -o " + filePath + " " + filePath.split(".")[0] + ".cpp")
        print("Done.")
    elif action == "n":
        pass
    elif action.startswith("t"):
        testFolderPath = os.getcwd() + "\\" + args[1] + "_tests"
        try:
            os.mkdir(testFolderPath)
        except Exception as e:
            print(e)
        for i in range(1, int(action.split("t")[1]) + 1):
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
    allPassed = True
    for test in t.tests:
        if not t.tests[test].run():
            allPassed = False
    if allPassed:
        themis_submitter.sumbit(themis_submitter.auth(), "2022_POKRZ_8",
                                os.path.basename(fileNameNoExtension),
                                filePath.split(".exe")[0]+".cpp")


main()
