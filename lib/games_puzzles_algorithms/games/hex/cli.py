from cmd import Cmd
from .game_state import GameState
from .color import cell_str
from .color import cell_str_to_cell
from .color import next_player
from .color import player_to_color
from .color import color_to_player
from .color import COLORS
from .color import COLOR_SYMBOLS
from .color import IllegalAction


class Cli(Cmd, object):
    """Command line interface to play hex games."""

    _header = "Go Text Protocol for Hex---Commands:"

    _STOP_AND_EXIT = True

    _SUCCESS_RESPONSE = "="
    _FAILURE_RESPONSE = "?"

    _LAST_COMMAND_SUCCEEDED = True

    _LAST_COMMAND_RESPONSE = ""

    _COMMAND_ID = 1

    _protocol_version = 2

    def update_prompt(self):
        self.prompt = ""

    prompt = ""

    _GTP_COMMANDS = sorted(
        [
            'boardsize',
            'protocol_version',
            'name',
            'list_commands',
            'list_gtp_commands',
            'known_command',
            'q',
            'set_time',
            'quit',
            'size',
            'clear_board',
            'play',
            'genmove',
            'show',
            'showboard',
            'clear',
            'time',
            'winner',
            'analyze',
            'valid',
            'turn',
            'ls'
        ])

    def __init__(self, agent):
        super(self.__class__, self).__init__()
        self.game = GameState.root(8)
        self.agent = agent
        self.move_time = 10
        self.last_move = None

    def _nontrivial_cmd(self, cmd, arg, line):
        try: func = getattr(self, 'do_' + cmd)
        except AttributeError: return self.default(line)
        if cmd in self._GTP_COMMANDS:
            result = func(arg)
            try:
                len(result)
            except TypeError:
                if result:
                    self.stdout.write(self._SUCCESS_RESPONSE + "\n\n")
                else:
                    self.stdout.write(self._FAILURE_RESPONSE + "\n\n")
                return result
            if result[0]:
                self.stdout.write(self._SUCCESS_RESPONSE
                                  + " "
                                  + result[1]
                                  + "\n\n")
            else:
                self.stdout.write(self._FAILURE_RESPONSE
                                  + " "
                                  + result[1]
                                  + "\n\n")
            return False
        else:
            self.stdout.write(self._SUCCESS_RESPONSE + "\n\n")
            return func(arg)

    def onecmd(self, line):
        """Interpret the argument as though it had been typed in response
        to the prompt.

        The return value is a flag indicating whether interpretation of
        commands by the interpreter should stop.
        """
        cmd, arg, line = self.parseline(line)
        if not line: return self.emptyline()
        if cmd is None: return self.default(line)

        self.lastcmd = '' if line == 'EOF' else line
        return self.default(line) if cmd == '' else \
               self._nontrivial_cmd(cmd, arg, line)

    def postcmd(self, stop, line):
        self.update_prompt()
        return super(self.__class__, self).postcmd(stop, line)

    def default(self, line):
        self.stdout.write(self._FAILURE_RESPONSE)
        return super(self.__class__, self).default(line)

    def do_valid(self, arg, opts=None):
        '''Indicates that the last move returned by genmove was valid and has
        been played.'''
        return (True, "")

    def do_turn(self, arg, opts=None):
        return (True, COLOR_SYMBOLS[self.game.player_to_act()])

    def do_name(self, arg, opts=None):
        """Return the name of the agent you are playing against."""
        return (True, type(self.agent).__name__)

    def do_protocol_version(self, arg, opts=None):
        """Return the version of GTP being used."""
        return (True, str(self._protocol_version))

    def do_known_command(self, arg, opts=None):
        """Check whether the given argument is a recognized HTP command."""
        known = cmd in self._GTP_COMMANDS
        if known:
            return (True, 'Yes')
        else:
            return (False, 'No')

    def do_list_gtp_commands(self, arg):
        '''List available Hex text protocal commands with "list_commands".'''
        self.stdout.write("{}\n".format(str(self.doc_leader)))
        self.print_topics(
            self._header,
            self._GTP_COMMANDS,
            15,
            80
        )
        return (True, '')

    do_list_commands = do_list_gtp_commands
    do_ls = do_list_gtp_commands

    def do_quit(self, arg, opts=None):
        '''Quit this session'''
        return self._STOP_AND_EXIT

    do_exit = do_quit
    do_q = do_quit
    do_EOF = do_quit

    def do_boardsize(self, args, opts=None):
        """Set the size of the game board and clear the board."""
        num_arguments = 1
        if(len(args) < num_arguments):
            return (False, "Requires an argument: A board size > 0")
        try:
            size = int(args)
        except ValueError:
            return (False, "Argument \"{}\" is not a valid size".format(size))
        if size < 1:
            return (False, "Argument \"{}\" is not a valid size".format(size))
        self.game = GameState.root(size)
        self.agent.reset()
        return (True, "")

    do_size = do_boardsize

    def do_clear_board(self, arg, opts=None):
        """Clear the game board."""
        self.game = GameState.root(
            *self.game.board.size()
        )
        self.agent.reset()
        return (True, "")

    do_clear = do_clear_board

    def do_play(self, arg_string, opts=None):
        """Play a stone of a given colour in a given cell.

        1st arg should be the cell to play (e.g. g5).
        2nd (optional) arg should be the colour (white/w or black/b) to play.
        Defaults to the next player to act.
        """
        args = arg_string.split(' ')
        try:
            y, x = cell_str_to_cell(args[0].strip())

            if(
                x < 0 or
                y < 0 or
                x >= self.game.board.num_columns() or
                y >= self.game.board.num_rows()
            ):
                return (
                    False,
                    ("Cell with row {} and column {} is out of bounds on an "
                     + "{}x{} board.").format(
                        y,
                        x,
                        self.game.board.num_rows(),
                        self.game.board.num_columns()
                    )
                )

            if len(args) > 1:
                if args[1][0].lower() == 'w':
                    self.game.set_player_to_act(
                        color_to_player(COLORS["white"]))
                elif args[1][0].lower() == 'b':
                    self.game.set_player_to_act(
                        color_to_player(COLORS["black"]))
                else:
                    return (False, "Player not recognized")
            self.game.play(self.game.board.cell_index(y, x))
            return(True, "")
        except (ValueError, IllegalAction) as e:
            return (False, str(e))

    def do_genmove(self, args, opts=None):
        """Allow the agent to play a stone of the given colour (white/w or
        black/b).
        """
        if(len(args) > 0):
            if args[0][0].lower() == 'w':
                self.game.set_player_to_act(color_to_player(COLORS["white"]))
            elif args[0][0].lower() == 'b':
                self.game.set_player_to_act(color_to_player(COLORS["black"]))
            else:
                return (False, "Player not recognized")

        action = self.agent.select_action(
            self.game,
            time_allowed_s=self.move_time
        )
        try:
            self.game.play(action)
        except IllegalAction as e:
            return (True, str(e))
        else:
            return (True, cell_str(self.game.board.row(action),
                                   self.game.board.column(action)))

    def do_showboard(self, args, opts=None):
        """Return an ASCII representation of the current state of the game
        board."""
        return (True, str(self.game))

    do_show = do_showboard

    def do_set_time(self, args, opts=None):
        """Change the time per move allocated to the search agent (in units of
        secounds)"""
        if(len(args) < 1):
            return (False, "Not enough arguments")
        try:
            time = float(args)
        except ValueError:
            return (False, "Argument is not a valid time limit")
        self.move_time = time
        return (True, "")

    def do_time(self, args, opts=None):
        return (True, str(self.move_time))

    def do_winner(self, args, opts=None):
        """Return the winner of the current game (black or white), none if
        undecided."""
        return (True, COLOR_SYMBOLS[self.game.winner()])

    def do_analyze(self, arg, opts=None):
        """Added to avoid crashing with GTP tools but not yet implemented."""
        return (True, "")
