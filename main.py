import sys
from main_parser import parse_main_arguments
from checkers.CheckersRunner import CheckersRunner


if __name__ == "__main__":
    args = parse_main_arguments(sys.argv[1:])

    if args.app == "checkers":
        r = CheckersRunner()
    
    r.run(args)


