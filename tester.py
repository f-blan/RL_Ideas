from test.TestRunner import TestRunner
from test_parser import parse_test_arguments
import sys

if __name__ == "__main__":
    args = parse_test_arguments(sys.argv[1:])

    r = TestRunner()
    r.run(args)