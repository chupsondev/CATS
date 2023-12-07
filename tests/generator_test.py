import sys
sys.path.append("../")

from generator import Generator

generator = Generator("generator_generator.py", "std-test", "/Users/chupson/dev/CATS/tests/")
generator.generate()
