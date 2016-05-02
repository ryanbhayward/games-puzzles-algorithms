#!/usr/bin/env python3

import random
import optparse
from games_puzzles_algorithms.htp import HtpInterface
from games_puzzles_algorithms.agent.rule_based_agent import CombinedPlayerRuleBasedAgent


def agent(r, **kwargs):
    return CombinedPlayerRuleBasedAgent(lambda: r.uniform(0, 1), **kwargs)


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option(
        "-r",
        "--random-seed",
        dest="random_seed",
        help="The agent's random seed. Defaults to system time."
    )
    parser.add_option(
        "-s",
        "--script",
        dest="script",
        help="A script of commands to play out."
    )
    parser.add_option(
        "-u",
        "--uct",
        dest="only_search",
        action="store_true",
        default=False,
        help="Use a RAVE enabled UCT agent. Defaults to False."
    )
    parser.add_option(
        "-c",
        "--only-corners",
        dest="only_corners",
        action="store_true",
        default=True,
        help="Play only in the obtuse corners on the first move instead of anywhere on the main diagonal. Defaults to True."
    )
    (options, args) = parser.parse_args()
    r = random.Random(options.random_seed)
    try:
        cli = HtpInterface(agent(r, only_corners=options.only_corners, only_search=options.only_search))
        if options.script is not None:
            with open(options.script) as f:
                for command in f:
                    command = command.strip()
                    print("< " + command)
                    cli.onecmd(command)
        cli.cmdloop()
    except KeyboardInterrupt:
        pass
