import sys
import traceback
import json
import logging


def log(data, level=logging.INFO, raw=False):
    sf = traceback.extract_stack()[-2]
    logger = logging.getLogger(sf[0])
    data_to_print = data if raw else json.dumps(data, sort_keys=True, indent=4)
    logger.log(level, "\nIn {} on line {} in {}\n{}".format(
        sf[0], sf[1], sf[2], data_to_print)
    )
