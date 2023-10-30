from cats.cats_tools import *
import os, sys

options = {}


def main(args, settings, location):
    fileNameGiven = args[0]
    filePath = None
    filePathCpp = None
    filePathNoExt = None

    built_file = SolutionFile(fileNameGiven)
    filePathNoExt = built_file.get_path_without_ext()
    filePathCpp = built_file.path

    exitCode = buildFile(filePathNoExt, filePathCpp)
