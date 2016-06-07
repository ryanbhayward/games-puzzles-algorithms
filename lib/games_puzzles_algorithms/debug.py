import sys
import traceback
import json
import logging


def log(data, level=logging.INFO):
    sf = traceback.extract_stack()[-2]
    logger = logging.getLogger(sf[0])
    logger.log(level, "\nIn {} on line {} in {}\n{}".format(
        sf[0], sf[1], sf[2], json.dumps(data,
                                        sort_keys=True,
                                        indent=4))
    )
