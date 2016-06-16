from cmd import Cmd

from .game_state import GameState
from .game_state import cell_str
from .game_state import cell_str_to_cell
from .game_state import next_player
from .game_state import player_to_color
from .game_state import color_to_player
from .game_state import COLORS
from .game_state import COLOR_SYMBOLS
from .game_state import IllegalAction


# TODO Fix, clean up, extract to a common CLI module, and document


class HtpInterface(Cmd, object):
    """docstring for HtpInterface"""

    intro = ""
    htp_header = "Go Text Protocol for Hex Commands:"

    _STOP_AND_EXIT = True

    SUCCESS_RESPONSE = "="
    FAILURE_RESPONSE = "?"

    _LAST_COMMAND_SUCCEEDED = True

    _LAST_COMMAND_RESPONSE = ""

    _COMMAND_ID = 1

    version = 0.1
    protocol_version = 2

    def update_prompt(self):
        # self._COMMAND_ID += 1
        # self.prompt = "{} ".format(self._COMMAND_ID)
        self.prompt = ""

    # prompt = "{} ".format(_COMMAND_ID)
    prompt = ""

    HTP_COMMANDS = sorted(
        [
            'boardsize',
            'protocol_version',
            'name',
            'version',
            'list_commands',
            'list_htp_commands',
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
            'show_revealed_board',
            'clear',
            'time',
            'winner',
            'analyze',
            'valid',
            'occupied',
            'turn',
            'ls'
        ])

    def __init__(self, agent):
        super(HtpInterface, self).__init__()
        self.game = GameState.root(8)
        self.agent = agent
        self.move_time = 10
        self.last_move = None
        self.num_times_occupied = 0

    def onecmd(self, line):
        """Interpret the argument as though it had been typed in response
        to the prompt.

        The return value is a flag indicating whether interpretation of
        commands by the interpreter should stop.

        """
        cmd, arg, line = self.parseline(line)
        if not line:
            return self.emptyline()
        if cmd is None:
            return self.default(line)
        self.lastcmd = line
        if line == 'EOF':
            self.lastcmd = ''
        if cmd == '':
            return self.default(line)
        else:
            try:
                func = getattr(self, 'do_' + cmd)
            except AttributeError:
                return self.default(line)
            if cmd in self.HTP_COMMANDS:
                result = func(arg)
                try:
                    len(result)
                except TypeError:
                    if result:
                        self.stdout.write(self.SUCCESS_RESPONSE + "\n\n")
                    else:
                        self.stdout.write(self.FAILURE_RESPONSE + "\n\n")
                    return False
                if result[0]:
                    self.stdout.write(self.SUCCESS_RESPONSE + " " + result[1] + "\n\n")
                else:
                    self.stdout.write(self.FAILURE_RESPONSE + " " + result[1] + "\n\n")
                return False
            else:
                self.stdout.write(self.SUCCESS_RESPONSE + "\n\n")
                return func(arg)

    def postcmd(self, stop, line):
        self.update_prompt()
        return super(self.__class__, self).postcmd(stop, line)

    def default(self, line):
        self.stdout.write(self.FAILURE_RESPONSE)
        return super(self.__class__, self).default(line)

    def do_occupied(self, arg, opts=None):
        '''Indicates that the last move returned by genmove is already occupied. Responds with a new move from genmove.'''
        self.game.undo()
        player = self.game.actor
        self.game.place(self.last_move, next_player(player), allow_noop=True)
        self.game.place(self.last_move, player, allow_noop=True)

        self.num_times_occupied += 1

        if opts is None:
            opts = {}
        opts['time_fraction'] = self.num_times_occupied * 2
        return self.do_genmove(arg, opts)

    def do_valid(self, arg, opts=None):
        '''Indicates that the last move returned by genmove was valid and has been played.'''
        self.num_times_occupied = 0
        return (True, "")

    def do_turn(self, arg, opts=None):
        '''Indicates that the last move returned by genmove was valid and has been played.'''
        return (True, COLOR_SYMBOLS[self.game.actor])

    def do_name(self, arg, opts=None):
        """Return the name of the agent you are playing against."""
        return (True, "morrill")

    def do_version(self, arg, opts=None):
        """Return the version of the agent you are playing against."""
        return (True, str(version))

    def do_protocol_version(self, arg, opts=None):
        """Return the version of HTP being used."""
        return (True, str(protocol_version))

    def do_known_command(self, arg, opts=None):
        """Check whether the given argument is a recognized HTP command."""
        known = cmd in self.HTP_COMMANDS
        if known:
            return (True, 'Yes')
        else:
            return (False, 'No')

    def do_list_htp_commands(self, arg):
        '''List available Hex text protocal commands with "list_commands".'''
        self.stdout.write("{}\n".format(str(self.doc_leader)))
        self.print_topics(
            self.htp_header,
            self.HTP_COMMANDS,
            15,
            80
        )
        return (True, '')

    do_list_commands = do_list_htp_commands

    def do_quit(self, arg, opts=None):
        '''Quit this session'''
        return self._STOP_AND_EXIT

    do_exit = do_quit
    do_q = do_quit

    do_EOF = do_q

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
        """
        Play a stone of a given colour in a given cell.
        1st arg should be the cell to play (e.g. g5)
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
                    "Cell with row {} and column {} is out of bounds on an {}x{} board.".format(
                        y,
                        x,
                        self.game.board.num_rows(),
                        self.game.board.num_columns()
                    )
                )

            if len(args) > 1:
                if args[1][0].lower() == 'w':
                    self.game.place((y, x), color_to_player(COLORS['white']))
                    return (True, "")
                elif args[1][0].lower() == 'b':
                    self.game.place((y, x), color_to_player(COLORS['black']))
                    return (True, "")
            else:
                self.game.play((y, x))
                return(True, "")
        except (ValueError, IllegalAction) as e:
            return (False, str(e))

    def do_genmove(self, args, opts=None):
        """Allow the agent to play a stone of the given colour (white/w or
        black/b)

        Note: play order is not enforced but out of order turns will cause the
        agents search tree to be reset

        """
        # if user specifies a player generate the appropriate move
        # otherwise just go with the current turn
        if(len(args) > 0):
            if args[0][0].lower() == 'w':
                self.game.set_turn(color_to_player(COLORS["white"]))
            elif args[0][0].lower() == 'b':
                self.game.set_turn(color_to_player(COLORS["black"]))
            else:
                return (False, "Player not recognized")

        time_fraction = 1.01
        if opts and 'time_fraction' in opts:
            time_fraction *= opts['time_fraction']

        self.last_move = self.agent.act(
            self.game,
            time_allowed_s=self.move_time / time_fraction
        )
        try:
            self.game.play(self.last_move)
        except IllegalAction as e:
            return (True, str(e))
        else:
            return (True, cell_str(self.last_move))

    def do_show_revealed_board(self, args, opts=None):
        """Return an ascii representation of the current state of the game
        board after all stones are revealed."""
        return (True, str(self.game))

    def do_showboard(self, args, opts=None):
        """Return an ascii representation of the current state of the game
        board from the given player's point of view."""
        player = None
        if(len(args) > 0):
            if args[0][0].lower() == 'w':
                player = color_to_player(COLORS["white"])
            elif args[0][0].lower() == 'b':
                player = color_to_player(COLORS["black"])
            else:
                return (False, "Player not recognized")
            return (True, self.game.to_s(player))
        else:
            return self.do_show_revealed_board(args, opts)

    do_show = do_showboard
    do_ls = do_show

    def do_set_time(self, args, opts=None):
        """Change the time per move allocated to the search agent (in units of
        secounds)"""
        if(len(args) < 1):
            return (False, "Not enough arguments")
        try:
            time = int(args)
        except ValueError:
            return (False, "Argument is not a valid time limit")
        if time < 1:
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
        """Added to avoid crashing with gui but not yet implemented."""
        return (True, "")
