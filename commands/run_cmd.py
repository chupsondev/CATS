from cats_tools import *
from option_lib import Option, getOption
import sys, os

options = {
    "input": Option("input", "Run the program with input specified in test files.", ["-i", "--input"], False,
                    valueType=str),
    "build": Option("build", "Build the file (g++ compiler for c++ files)", ["-b", "--build"], True),
}


def main(args, settings, location):
    validOptions, fileNameGiven = getOptionsAndFileName(args, options)
    setOptions(validOptions, options, settings)

    filePath = fileNameGiven if isPath(fileNameGiven) else os.path.join(location, fileNameGiven)
    filePathNoExt = os.path.splitext(filePath)[0]
    filePathCpp = filePathNoExt + ".cpp"
    fileName = os.path.basename(filePathNoExt)
    fileNameNoExt = os.path.splitext(fileName)[0]

    if options["build"].getValue() is True:
        buildFile(filePathNoExt, filePathCpp)

    if options["input"].getValue() is not False:
        runTestsWithoutResults(filePathNoExt + ".exe")
    else:
        runExecutable(filePathNoExt + ".exe")
