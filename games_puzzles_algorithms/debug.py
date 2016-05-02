import sys
import traceback


def log(data, file=sys.stdout):
    sf = traceback.extract_stack()[-2]
    print("\nIn {} on line {} in {}\n    {}".format(
        sf[0], sf[1], sf[2], data, file=file)
    )
