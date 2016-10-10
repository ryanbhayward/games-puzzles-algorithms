import sys
import traceback
import json
import logging


def log(data, level=logging.INFO, raw=False):
    if logging.getLogger().getEffectiveLevel() >= level:
        return
    sf = traceback.extract_stack()[-2]
    logger = logging.getLogger(sf[0])
    data_to_print = data() if raw else json.dumps(data(), sort_keys=True, indent=4)
    logger.log(level, "\nIn {} on line {} in {}\n{}".format(
        sf[0], sf[1], sf[2], data_to_print)
    )

def log_t(data, level=logging.INFO, raw=False):
    if logging.getLogger().getEffectiveLevel() != logging.INFO:
        return
    sf = traceback.extract_stack()[-2]
    logger = logging.getLogger(sf[0])
    data_to_print = data() if raw else json.dumps(data(), sort_keys=True, indent=4)
    logger.log(level, "\nIn {} on\nline {} in {}\n{}".format(
        sf[0], sf[1], sf[2], data_to_print)
    )
