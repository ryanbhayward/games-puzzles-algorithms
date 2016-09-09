#! /usr/bin/env python3

import argparse
import logging
import sys

from player import Player
from tournament import Tournament


def tournament_args():
    parser = argparse.ArgumentParser('Play a tournament between two GTP '
                                     'players.')
    parser.add_argument('players', nargs=2,
                        help='Invocation for each GTP player.')
    parser.add_argument('-n', '--num-games', type=int, default=1,
                        help='Number of games in tournament.')
    parser.add_argument('-s', '--size', type=int, default=3,
                        help='Size of game instance.')
    parser.add_argument('-t', '--time-limit', type=int, default=1,
                        help='Time limit for each move, in seconds.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Use verbose output for stdout.')
    parser.add_argument('-l', '--log-file', help='File to store logs.')
    return parser.parse_args()


def tournament_logger(verbose=False, log_file=None):
    """Creates and configures a logger for use with the tournament."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s\n')

    if log_file is not None:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)

    if verbose:
        stdout_handler.setLevel(logging.DEBUG)
    else:
        stdout_handler.setLevel(logging.INFO)

    logger.addHandler(stdout_handler)

    return logger


def main():
    args = tournament_args()

    logger = tournament_logger(verbose=args.verbose, log_file=args.log_file)

    players = [Player(invocation) for invocation in args.players]

    tournament = Tournament(players, args.num_games, args.size,
                            args.time_limit, logger)

    tournament.play_tournament()

    for p in players:
        p.exit()


if __name__ == '__main__':
    main()
