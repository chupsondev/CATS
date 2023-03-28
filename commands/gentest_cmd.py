from option_lib import Option

options = {
    "generator": Option("generator", "The generator to use", ["-g", "--generator"], "empty", valueType=str),
    # default is empty tests if no generator is specified, or the generator present in the tests folder if present
    "number": Option("number", "The number of tests to generate", ["-n", "--number"], False, valueType=int),
    # default is 1
    "location": Option("location", "The location to generate the tests in", ["-l", "--location"], False),
    # default is creating "tests" folder in the current directory and a problem directory in that folder
}


def main(args, settings, location):
    pass
