from option_lib import Option
import options_parser
import generators.empty
import generator as gen
import cats_tools

NEW_TEST_LOCATION_PLACEHOLDER = 'create  (or use existing) generic "tests" folder, and a problem directory in ' \
                                'that directory'

builtin_generators = {
    "empty": generators.empty
}

options = {
    "generator": Option("generator", "Generator to use -- to use one of the built-in ones pass a name only, if you"
                                     "want to use your own, pass name.py or a full path",
                        ["-g", "--generator"], "empty", valueType=str),
    "number": Option("number", "The number of tests to generate", ["-n", "--number"], 1, valueType=int),
    "location": Option("location", "The location to generate the tests in", ["-l", "--location"],
                       NEW_TEST_LOCATION_PLACEHOLDER, valueType=str),
}


def get_generator_path(requested_generator: str) -> str:
    is_builtin_generator = requested_generator in builtin_generators
    if is_builtin_generator:
        return builtin_generators[requested_generator].__file__
    return cats_tools.SolutionFile(requested_generator, allowed_extensions=['.py']).path


def main(current_options: options_parser.OptionsParser, settings, location):
    args = current_options.get_arguments()
    given_problem_string = args[0]
    problem_name = cats_tools.SolutionFile(given_problem_string).name

    options = current_options.get_options()
    requested_generator = options['generator'].getValue()

    generator_path = get_generator_path(requested_generator)
    generator = gen.Generator(generator_path, problem_name, location)
    for _ in range(options['number'].getValue()):
        generator.generate()
