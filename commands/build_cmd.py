from cats_tools import *
import os, sys

options = {}


def main(args, settings, location):
    fileNameGiven = args[0]
    filePath = None
    filePathCpp = None
    filePathNoExt = None
    if not isPath(fileNameGiven):
        filePath = os.path.join(location, fileNameGiven)
    else:
        filePath = fileNameGiven

    filePathNoExt = os.path.splitext(filePath)[0]
    filePathCpp = filePathNoExt + ".cpp"
    fileName = os.path.basename(filePathNoExt)
    fileNameNoExt = os.path.splitext(fileName)[0]

    exitCode = buildFile(filePathNoExt, filePathCpp)
