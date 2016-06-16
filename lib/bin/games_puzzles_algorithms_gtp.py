#!/usr/bin/env python3

import random
import optparse
from games_puzzles_algorithms.games.hex.htp import HtpInterface
from games_puzzles_algorithms.players.rule_based.uniform_random_agent import UniformRandomAgent


def agent(r, **kwargs):
    return UniformRandomAgent(lambda: r.uniform(0, 1), **kwargs)


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
    (options, args) = parser.parse_args()
    r = random.Random(options.random_seed)
    try:
        cli = HtpInterface(agent(r))
        if options.script is not None:
            with open(options.script) as f:
                for command in f:
                    command = command.strip()
                    print("< " + command)
                    cli.onecmd(command)
        cli.cmdloop()
    except KeyboardInterrupt:
        pass
