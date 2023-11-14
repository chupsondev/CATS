import os
import sys
import time
from os import listdir
from os import path
from subprocess import Popen, PIPE
from cats_tools import cprint, COLORS, print_error, buildFile, tabulate
from cats_tools import find_test_folders
import importlib.util

MAX_SEARCH_DEPTH_ = 4
STATIC_TEST_EXTENSIONS = ['.in', '.out']
STATIC_TEST_OUT = '.out'
STATIC_TEST_IN = '.in'
SCRIPT_EXTENSIONS = ['.py']
SCRIPT_NAMES = ['script', 'judge']
BRUTE_EXTENSIONS = ['.cpp']
PASSED_EMOTE = '✅'
FAILED_EMOTE = '❌'
STATIC_TEST = 'static'
BRUTE_COMPARE_TEST = 'brute compare'
SCRIPT_TEST = 'script'
MAX_NUM_UNSHORTENED_LINES = 15


def is_static_test_complete(files) -> bool:
    files_ext = [path.splitext(file)[1] for file in files]
    return STATIC_TEST_IN in files_ext and STATIC_TEST_OUT in files_ext


def get_static_test_file(files, type):
    for file in files:
        ext = path.splitext(file)[1]
        if ext == type:
            return file
    return None


def remove_from_dict(dictionary, for_removal):
    for key in for_removal:
        dictionary.pop(key)


def tests_sort_key(test):
    return test.name


class RunResult:
    def __init__(self, output, stderr, execution_time):
        self.output = output.decode('utf-8')
        self.stderr = stderr.decode('utf-8')
        self.execution_time = execution_time


class TestResult:
    def __init__(self, passed: bool, actual_output=None):
        self.passed = passed
        self.actual_output = actual_output


class Test:
    def __init__(self, name, tested_file_bin_path, input_path):
        self.result: TestResult = None
        self.name = name
        self.tested_file_path = tested_file_bin_path
        if not path.exists(tested_file_bin_path):
            print_error("File " + tested_file_bin_path + " does not exist.")
        extension = path.splitext(tested_file_bin_path)[1]

        self.tested_file_name = path.basename(tested_file_bin_path)
        self.input_path = input_path
        self.runtime_in_secs = None
        self.type = "generic"
        self.max_num_unshortened_lines = MAX_NUM_UNSHORTENED_LINES

    def run(self):
        start_time = time.time()
        process = Popen([self.tested_file_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        with open(self.input_path, 'r') as input_file:
            output, error = process.communicate(input_file.read().encode('utf-8'))
        end_time = time.time()
        execution_time = end_time - start_time
        return RunResult(output, error, execution_time)

    def get_input(self):
        f = open(self.input_path, 'r')
        input = f.read()
        f.close()
        input = input.split()
        return input

    def get_expected_output(self):
        return "unknown"

    def get_actual_output(self):
        ac = self.result.actual_output
        if len(ac) > self.max_num_unshortened_lines:
            ac = ac[:self.max_num_unshortened_lines]
            ac.append(COLORS.BLUE + '...' + COLORS.ENDC)
        return ac

    def get_runtime(self) -> str:
        runtime = self.runtime_in_secs
        runtime = round(runtime, 4) if runtime is not None else 'unknown'
        runtime = str(runtime)
        return runtime

    def print_result(self, short: bool = False, max_num_unshortened_lines: int = MAX_NUM_UNSHORTENED_LINES):
        self.max_num_unshortened_lines = max_num_unshortened_lines
        if self.result is None:
            print_error(f"Result of test {self.name} can't be printed because result can't be found")
            return

        runtime = self.get_runtime()

        if short:
            self.print_short_result(runtime)
            return
        self.print_full_result(runtime)

    def print_full_result(self, runtime: str):
        if self.result.passed:
            cprint(f'{PASSED_EMOTE} Test {self.name} ({self.type}) passed. Runtime: {runtime} secs.', COLORS.GREEN)
        else:
            cprint(f'{FAILED_EMOTE} Test {self.name} ({self.type}) failed. Runtime: {runtime} secs.', COLORS.FAIL)
            cprint("\tInput:", COLORS.DEF, bold=True)
            input = self.get_input()
            print(tabulate(input))
            if self.type == SCRIPT_TEST:
                return
            cprint("\tExpected output:", COLORS.DEF, bold=True)
            expected_output = self.get_expected_output()
            print(tabulate(expected_output))
            cprint("\tActual output:", COLORS.DEF, bold=True)
            actual_output = self.get_actual_output()
            print(tabulate(actual_output))

    def print_short_result(self, runtime: str):
        if self.result.passed:
            return

        cprint(f'{FAILED_EMOTE} Test {self.name} ({self.type}) failed. Runtime: {runtime} secs.', COLORS.FAIL)
        cprint("\tActual output:", COLORS.DEF, bold=True)
        actual_output = self.get_actual_output()
        print(tabulate(actual_output))


class StaticTest(Test):

    def __init__(self, name, tested_file_bin_path, input_path, expected_output_path):
        super().__init__(name, tested_file_bin_path, input_path)
        self.expected_output_path = expected_output_path
        self.type = STATIC_TEST

    def get_expected_output(self):
        f = open(self.expected_output_path, 'r')
        expected_output = f.read()
        f.close()
        return expected_output.split()

    def judge(self):
        output = self.run()
        self.runtime_in_secs = output.execution_time
        output = output.output.split()
        expected_output = self.get_expected_output()
        passed = output == expected_output
        self.result = TestResult(passed, output)


class ScriptTest(Test):

    def __init__(self, name, tested_file_bin_path, input_path, script_path):
        super().__init__(name, tested_file_bin_path, input_path)
        self.script_path = script_path
        self.type = SCRIPT_TEST

    def judge(self):
        output = self.run()
        self.runtime_in_secs = output.execution_time
        output = output.output.split()
        input = open(self.input_path, 'r').read().split()
        # run script
        module_name = path.splitext(path.basename(self.script_path))[0]
        script_test_spec = importlib.util.spec_from_file_location(module_name, self.script_path)
        script_test = importlib.util.module_from_spec(script_test_spec)
        sys.modules[script_test_spec.name] = script_test
        script_test_spec.loader.exec_module(script_test)
        passed = script_test.judge(input, output)
        self.result = TestResult(passed, output)


class BruteCompareTest(Test):

    def __init__(self, name, tested_file_bin_path, input_path, brute_file_path):
        super().__init__(name, tested_file_bin_path, input_path)
        self.brute_file_path = brute_file_path
        self.input_path = input_path
        self.expected_output = None
        if not path.isfile(self.brute_file_path):
            print_error('Brute file not found: ' + self.brute_file_path)
        extension = path.splitext(self.brute_file_path)[1]
        if extension != '.cpp':
            print_error('Brute file must be a cpp file: ' + self.brute_file_path)
        self.type = BRUTE_COMPARE_TEST

    def judge(self):
        brute_path_no_ext = path.splitext(self.brute_file_path)[0]
        brute_path = brute_path_no_ext + '.exe'
        buildFile(brute_path_no_ext, self.brute_file_path)
        brute = Test(self.name + '_brute', brute_path, self.input_path)
        brute_result = brute.run()
        brute_output = brute_result.output.split()
        self.expected_output = brute_output
        output = self.run()
        self.runtime_in_secs = output.execution_time
        output = output.output.split()
        passed = output == brute_output
        self.result = TestResult(passed, output)

    def get_expected_output(self):
        return self.expected_output


class Tests:
    """
    A class that represents a set of tests for a given binary file
    """

    def __init__(self, tested_file_path, MAX_SEARCH_DEPTH=MAX_SEARCH_DEPTH_, full_verbosity: bool = True,
                 max_num_unshortened_tests: int = 12, max_num_unshortened_lines: int = 15):
        """
        :param tested_file_path: The path to the binary file to be tested
        """
        self.tested_file_path = tested_file_path
        self.tested_file_name = path.basename(tested_file_path)
        self.tested_file_name = path.splitext(self.tested_file_name)[0]
        self.MAX_SEARCH_DEPTH = MAX_SEARCH_DEPTH
        self.full_verbosity = full_verbosity
        self.max_num_unshortened_tests = max_num_unshortened_tests
        self.max_num_unshortened_lines = max_num_unshortened_lines
        self.tests = []
        self.num_passed_tests = 0

    def add_script_tests(self, file_sets, script_path, test_name_prefix):

        tests = []

        for file_set in file_sets:
            file_set = file_sets[file_set]
            extensions = [path.splitext(file)[1] for file in file_set]
            if STATIC_TEST_IN not in extensions:
                continue

            input_file = get_static_test_file(file_set, STATIC_TEST_IN)

            name = path.basename(file_set[0])
            name = path.splitext(name)[0]
            name = test_name_prefix + name
            tests.append(ScriptTest(name, self.tested_file_path, input_file, script_path))

        return tests

    def add_brute_tests(self, file_sets, brute_path, test_name_prefix):

        tests = []

        for file_set in file_sets:
            file_set = file_sets[file_set]
            extensions = [path.splitext(file)[1] for file in file_set]
            if STATIC_TEST_IN not in extensions:
                continue

            input_file = get_static_test_file(file_set, STATIC_TEST_IN)

            name = path.basename(file_set[0])
            name = path.splitext(name)[0]
            name = test_name_prefix + name
            tests.append(BruteCompareTest(name, self.tested_file_path, input_file, brute_path))

        return tests

    def get_tests(self, folder, level=0, test_name_prefix=''):
        tests = []
        if level > 1:
            return tests

        files = {}
        script_found = False
        script_path = None
        brute_found = False
        brute_path = None

        for file in listdir(folder):
            file_path = path.join(folder, file)
            name = path.basename(file_path)
            name = path.splitext(name)[0]
            if path.isdir(file_path):
                tests += self.get_tests(file_path, level + 1, test_name_prefix + file + '/')
                continue
            if not path.isfile(file_path):
                continue
            extension = path.splitext(file_path)[1]
            if extension in STATIC_TEST_EXTENSIONS:
                if name not in files:
                    files[name] = []
                files[name].append(file_path)
            elif extension in SCRIPT_EXTENSIONS and not script_found and name in SCRIPT_NAMES:
                script_found = True
                script_path = file_path
            elif extension in BRUTE_EXTENSIONS:
                brute_found = True
                brute_path = file_path

        static_tests = []
        for file_set in files:
            if is_static_test_complete(files[file_set]):
                input_path = get_static_test_file(files[file_set], STATIC_TEST_IN)
                output_path = get_static_test_file(files[file_set], STATIC_TEST_OUT)
                if input_path is None or output_path is None:
                    continue
                tests.append(StaticTest(test_name_prefix + file_set, self.tested_file_path, input_path, output_path))
                static_tests.append(file_set)

        remove_from_dict(files, static_tests)

        if script_found:
            tests += self.add_script_tests(files, script_path, test_name_prefix)
        elif brute_found:
            tests += self.add_brute_tests(files, brute_path, test_name_prefix)

        return tests

    def set_tests(self, folder):
        test_folders = find_test_folders(self.tested_file_name, folder, MAX_SEARCH_DEPTH=self.MAX_SEARCH_DEPTH)
        self.tests = []
        for folder in test_folders:
            self.tests += self.get_tests(folder)

    def run_tests(self):
        all_passed = True
        self.num_passed_tests = 0
        self.tests.sort(key=lambda x: x.name)
        highest_runtime = 0
        highest_runtime_name = ''
        runtime_sum = 0
        shorten_tests: bool = len(self.tests) > self.max_num_unshortened_tests and not self.full_verbosity
        passed_tests: list[str] = []
        for test in self.tests:
            test.judge()
            test.print_result(shorten_tests, self.max_num_unshortened_lines)
            highest_runtime = max(highest_runtime, float(test.get_runtime()))
            highest_runtime_name = highest_runtime_name if highest_runtime > float(test.get_runtime()) \
                else test.name
            runtime_sum += float(test.get_runtime())
            self.num_passed_tests += 1 if test.result.passed else 0
            if test.result.passed:
                passed_tests.append(test.name)
            all_passed = all_passed and test.result.passed

        # list of passed tests if shortened (when shortening passed are not printed)
        if shorten_tests and len(passed_tests) > 0:
            cprint(f"{PASSED_EMOTE} Tests passed: {', '.join(passed_tests)}", COLORS.GREEN)


        # test summary
        percent_passed = (self.num_passed_tests / len(self.tests) * 100).__round__(2)
        message: str = (f"{percent_passed}% of tests passed. Highest runtime: {highest_runtime} ({highest_runtime_name}). "
                        f"Average runtime: {(runtime_sum / len(self.tests)).__round__(4)}")
        print()
        cprint("■" * int(percent_passed / 10) + "□" * (10 - int(percent_passed / 10)),
               COLORS.GREEN if percent_passed >= 50 else COLORS.FAIL)
        if percent_passed >= 50:
            cprint(PASSED_EMOTE + " " + message, COLORS.GREEN)
        else:
            cprint(FAILED_EMOTE + " " + message, COLORS.FAIL)


        return all_passed

    def run_test(self, test_name: str):
        test_name = test_name.replace("'", '') if test_name[0] == "'" else test_name.replace('"', '')
        for test in self.tests:
            if test.name == test_name:
                test.judge()
                test.print_result()
                return test.result.passed
        print_error('Test ' + test_name + ' not found.')
        return False

    def print_results(self):  # function should be obsolete, keeping just in case
        for test in self.tests:
            if test.result is not None:
                test.print_result()
