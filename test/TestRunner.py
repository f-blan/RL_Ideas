
from argparse import Namespace
from test.test_checkers.test_checkers import TestCheckers

class TestRunner:
    def run(self, args: Namespace) -> None:
        if args.app == "all" or args.app == "checkers":
            t = TestCheckers(args)
            t.run()
