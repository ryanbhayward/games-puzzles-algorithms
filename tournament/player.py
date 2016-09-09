import re
import shlex

from subprocess import PIPE, Popen, TimeoutExpired


class PlayerException(Exception):
    pass


class PlayerCmdException(PlayerException):
    pass


class Player(object):
    """
    Player is a simple interface to a game playing process which is communicated
    with using the GTP protocol. Player contains very minimal logic outside of
    nicely handling interaction with the player process.
    """
    def __init__(self, invocation):
        args = shlex.split(invocation)
        self._process = Popen(args, stdin=PIPE, stdout=PIPE,
                              universal_newlines=True)
        self._stdout = self._process.stdout
        self._stdin = self._process.stdin

    def _write(self, command):
        self._stdin.write(command)
        self._stdin.write('\n')
        self._stdin.flush()

    def _read(self):
        response = self._stdout.readline()

        next_line = self._stdout.readline()

        while next_line != '\n':
            response += next_line
            next_line = self._stdout.readline()

        return response

    def _cmd(self, command):
        self._write(command)

        response = self._read()
        error_occurred = response.startswith('?')
        response = response[2:].rstrip()

        if error_occurred:
            raise PlayerCmdException("Error issuing command: '{}'. Response "
                                     "was: '{}'".format(command, response))
        return response

    def exit(self):
        self._cmd('q')
        try:
            rc = self._process.wait(timeout=10)
            if rc != 0:
                raise PlayerException('{} exited with non-zero error code {}'
                                      .format(self._process.pid, rc))
        except TimeoutExpired:
            raise PlayerException('Timed out wating for {} to exit.'
                                  .format(self._process.pid))

    def _set_size(self, size):
        self._cmd('size {}'.format(size))

    def _set_time_limit(self, time_limit):
        self._cmd('set_time {}'.format(time_limit))

    def _gen_move(self):
        return self._cmd('genmove')

    def _play_move(self, move):
        self._cmd('play {}'.format(move))

    def _name(self):
        return self._cmd('name')

    def _clear_board(self):
        self._cmd('clear_board')

    def _final_score(self):
        return self._cmd('final_score')

    def _board(self):
        return self._cmd('showboard')

    def _player_to_move(self):
        return self._cmd('player_to_move')

    def configure(self, size=None, time_limit=None):
        if size is not None:
            self._set_size(size)
        if time_limit is not None:
            self._set_time_limit(time_limit)

    def play(self, move=None):
        if move is not None:
            self._play_move(move)
            return
        return self._gen_move()

    def clear(self):
        self._clear_board()

    def game_finished(self):
        # An empty string indicates the game is ongoing.
        score_string = self._final_score()
        return bool(score_string)

    def final_score(self):
        score_string = self._final_score()

        if score_string == '0':
            return ('0', '0')

        regex = r'(?P<winner>.*)\+(?P<score>.*)'
        result = re.match(regex, score_string)

        if result is None:
            raise PlayerException('Could not parse win string: '
                                  '{}'.format(score_string))

        return (result.group('winner'), result.group('score'))

    def board(self):
        return self._board()

    def player_to_move(self):
        return self._player_to_move()

    def __str__(self):
        return '{}-{}'.format(self._name(), self._process.pid)
