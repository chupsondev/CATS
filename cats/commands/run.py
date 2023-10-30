from cats.cats_tools import *
from cats.option_lib import Option

options = {
    "input": Option("input", "Run the program with input specified in test files.", ["-i", "--input"], False,
                    valueType=str),
    "build": Option("build", "Build the file (g++ compiler for c++ files)", ["-b", "--build"], True),
}


def main(args, settings, location):
    settings = settings["run"]
    validOptions, fileNameGiven = getOptionsAndFileName(args, options)
    setOptions(validOptions, options, settings)

    tested_solution = SolutionFile(fileNameGiven)

    filePathNoExt = tested_solution.get_path_without_ext()
    filePathCpp = tested_solution.path

    if options["build"].getValue() is True:
        buildFile(filePathNoExt, filePathCpp)

    if options["input"].getValue() is not False:
        runTestsWithoutResults(filePathNoExt + ".exe")
    else:
        runExecutable(filePathNoExt + ".exe")
