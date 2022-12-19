from cats_tools import cprint, COLORS
from cats_tools import isPath, isRealPath, buildFile, pathify
import os, sys

options = {}


def main(args, settings, location):
    fileName = args[0]
    filePath = None
    filePathCpp = None
    filePathNoExt = None
    if not isPath(fileName):
        filePath = os.path.join(location, fileName)
    else:
        filePath = fileName

    filePathNoExt = os.path.splitext(filePath)[0]
    filePathCpp = filePathNoExt + ".cpp"

    exitCode = buildFile(filePathNoExt, filePathCpp)
