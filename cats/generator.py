import os.path

from cats import cats_tools
from cats.cats_tools import find_test_folders
from os import path
import importlib.util
import sys


class Generator:

    def __init__(self, generator_path: str, tested_file_name: str, working_dir: str, test_location: None | str = None):
        self.generator_path = generator_path

        self.tested_file_name = tested_file_name

        self.working_dir = working_dir

        self.test_location = test_location

    def generate(self):
        module_name = path.splitext(path.basename(self.generator_path))[0]
        generator_spec = importlib.util.spec_from_file_location(module_name, self.generator_path)
        generator = importlib.util.module_from_spec(generator_spec)
        sys.modules[generator_spec.name] = generator
        generator_spec.loader.exec_module(generator)

        generator_output = generator.generate()
        test_input = generator_output[0]
        test_output = generator_output[1]

        test_location: str | None = None
        test_folders = find_test_folders(self.tested_file_name, self.working_dir)
        if os.path.dirname(self.generator_path) in test_folders:
            test_location = os.path.dirname(self.generator_path)
        elif len(test_folders) > 0:
            test_location = test_folders[0]
        else:
            test_location = os.path.join(self.working_dir, "tests", self.tested_file_name)
        test_location = self.test_location if self.test_location is not None else test_location

        max_numbered_test = 0

        for file in os.listdir(test_location):
            file_path = os.path.join(test_location, file)
            if os.path.isdir(file_path):
                continue

            file = os.path.basename(file)
            file = os.path.splitext(file)[0]
            max_numbered_test = max(max_numbered_test, int(file)) if file.isnumeric() else max_numbered_test

        test_name = str(max_numbered_test + 1)
        input_file_path = os.path.join(test_location, test_name) + '.in'
        output_file_path = os.path.join(test_location, test_name) + '.out'

        open(input_file_path, 'w').write(test_input)
        open(output_file_path, 'w').write(test_output)
