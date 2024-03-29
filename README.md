<h1 align = center> CATS </h1>
<p align = center> Welcome to CATS - Competitive Algorithm Tool Set </p>
This is a simple program, a set of tools, mostly for testing solutions to competitive programming problems.


# Installing
What _I_ would do, is:
1. Clone this repo into some folder like `/usr/local` on Linux or `C:\Users\username\CATS` on Windows.
    - `git clone https://github.com/chupsondev/CATS.git`
2. Add the folder I just cloned to PATH
_But_, install it however you want, I don't know what you wanna do. 

# Commands 
CATS has mulitple sub-commands. All of them are discribed below.

## `test`
<pre>
cats test <i>solution file [options]</i>
</pre>

This command tests a given solution file, using a set of tests predefined by the user. You must provide a solution file to be tested - you can either give just the name of that file, a name and an extension, or the full path. For now, the only supported files are those with the `.cpp` extension.

### Options
- `--build` or `-b`
    - build the solution file
- `--submit` or `-s`
    - submit the solution to themis, if all tests passed
- `--verbose` or `-v`
    - print all available information, bypassing rules meant to prevent CATS' output from being too long
- `--test *name of test*` or `-t *name of test*`
    - if provided, run only the test given, instead of all of them

##  `build`
<pre>
cats build <i>solution file</i>
</pre>

Builds the solution file given.

## `run`
<pre>
cats run <i>solution file [options]</i>
</pre>

Runs solution file.

**CURRENTLY BROKEN**

## `gentest`
<pre>
cats run <i>solution file [options]</i>
</pre>

Generates tests for the given solution, using your own generator, or one of the generators built-in to CATS.

### Options
- `--generator` or `-g`
    - the generator to be used
- `--number` or `-n`
    - number of tests to be created


# Generators
Generators for generating tests can only be written in Python (for now).
The generator should have a function called `generate()` that takes no arguments and returns a list (or tuple) that has exactly two strings: the first begin the input for the test, and the second being the expected output.

# Tests
You have to put tests in one of the following locations (problem_name should be replaced with the name of the file you're testing, without extension):
- `./tests/problem_name`
- `./problem_name_tests`

Those folders do not actually have to be in the working directory - CATS looks for them up to 4 levels down the directory tree. It is however recommended that you start CATS in the same folder where you solution file and all your tests are.
