from collections import defaultdict


class TournamentResult(object):
    """
    TournamentResult holds the result of a tournament. This is defined as a
    count of how many times each player has won, the count of how many draws
    have occurred, and the sequence of wins as they occurred.
    """
    def __init__(self):
        self._sequence = []
        self._results = defaultdict(int)
        self._draws = 0

    def increment_win_count(self, player, side):
        # Check for a draw.
        if side == '0':
            self._sequence.append(('Draw', '0'))
            self._draws += 1
        else:
            self._sequence.append((player, side))
            self._results[player] += 1

    def __str__(self):
        outcomes = []

        for (player, games) in self._results.items():
            outcomes.append('{} won {} games.'.format(player, games))

        if self._draws > 0:
            outcomes.append('{} draws occurred.'.format(self._draws))

        return '\n'.join(outcomes)


class Tournament(object):
    """
    Tournament is used to run a tournament between two GTP players. The
    tournament will handle configuring the players as necessary, and will then
    play a series of rounds between the players. The first player to play
    alternates between players each round. A round consists of both players
    making moves until they agree that the game is over. We make the assumption
    that players will agree the game is over after a winning move has been made.
    """
    def __init__(self, players, num_games, game_size, time_limit, logger):
        self._logger = logger
        self._results = TournamentResult()
        self._round = 1
        self._players = players
        self._games = num_games
        self._size = game_size
        self._time_limit = time_limit
        self._configure_players()

    def _configure_players(self):
        """Send configuration to each player"""
        for player in self._players:
            player.configure(size=self._size, time_limit=self._time_limit)

    def _initialize_round(self):
        self._player_has_resigned = False
        self._consecutive_passes = 0

        for player in self._players:
            player.clear()

    def _round_finished(self):
        """Ask if players agree the game is finished."""
        return self._player_has_resigned or self._consecutive_passes > 1

    def _notify_players(self, move, skip_index):
        """
        Notify all other players of the given move, skipping the player at
        index.
        """
        for (i, player) in enumerate(self._players):
            if i == skip_index:
                continue
            player.play(move)

    def _next_player(self, player_index):
        """Return the next to play after the player at the given index."""
        num_players = len(self._players)
        return (player_index + 1) % num_players

    def _play_round(self, first_to_play):
        """Play a single round of a tournament."""
        self._initialize_round()
        player_index = first_to_play

        player_mapping = {}

        while not self._round_finished():
            player = self._players[player_index]

            if player not in player_mapping.values():
                player_mapping[player.player_to_move()] = player

            move = player.play()

            self._logger.debug('{} plays {}\n{}'.format(player, move,
                                                        player.board()))

            if move == 'resign':
                self._player_has_resigned = True
            elif move == 'pass':
                self._consecutive_passes += 1
            else:
                self._consecutive_passes = 0

            self._notify_players(move, player_index)
            player_index = self._next_player(player_index)

        if self._player_has_resigned:
            winner = player.player_to_move()
        else:
            (winner, score) = player.final_score()

        if winner == '0':
            self._logger.debug('Round ends in a draw.')
            self._results.increment_win_count('', winner)
        else:
            winning_player = player_mapping[winner]
            self._logger.debug('{} wins round {} as {}'.format(winning_player,
                                                               self._round,
                                                               winner))
            self._results.increment_win_count(winning_player, winner)

        self._round += 1

    def play_tournament(self):
        """Play a full tournament between the players."""
        self._logger.info(self)
        self._round = 1

        first_to_play = 0
        for _ in range(self._games):
            self._play_round(first_to_play)
            first_to_play = self._next_player(first_to_play)

        self._logger.info(self._results)

    def __str__(self):
        players = ' vs. '.join(str(p) for p in self._players)
        size = 'Size: {}'.format(self._size)
        time = 'Time limit: {}s'.format(self._time_limit)
        games = 'Games: {}'.format(self._games)

        return '\n'.join((players, size, time, games))
