from cmd import Cmd
from copy import deepcopy


class Cli(Cmd, object):
    """Command line interface to play hex games.""" # TODO

    _header = "Go Text Protocol for Hex---Commands:" # TODO

    _STOP_AND_EXIT = True

    _SUCCESS_RESPONSE = "="
    _FAILURE_RESPONSE = "?"

    _LAST_COMMAND_SUCCEEDED = True

    _LAST_COMMAND_RESPONSE = ""

    _COMMAND_ID = 1

    _protocol_version = 2

    def update_prompt(self): self.prompt = ""

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
            'final_score',
            'analyze',
            'valid',
            'player_to_move',
            'ls',
            'undo'
        ])

    def __init__(self, game, agent):
        super(self.__class__, self).__init__()
        self.game = game
        self.agent = agent
        self.move_time = 10

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

    def do_player_to_move(self, arg, opts=None):
        return (True,
                self.game.player_to_ui_player(self.game.state.player_to_act()))

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
            return (False, "Argument \"{}\" is not a valid size".format(args))
        if size < 1:
            return (False, "Argument \"{}\" is not a valid size".format(size))
        self.game.reset(size)
        self.agent.reset()
        return (True, "")

    do_size = do_boardsize

    def do_clear_board(self, arg, opts=None):
        """Clear the game board."""
        self.game.reset_state()
        self.agent.reset()
        return (True, "")

    do_clear = do_clear_board

    def do_play(self, arg_string, opts=None):
        """Play a stone of a given colour in a given cell.

        1st arg should be the action to play (e.g. g5 for hex).
        2nd (optional) arg should be the colour (white/w or black/b) to play.
        Defaults to the next player to act.
        """
        args = arg_string.split(' ')
        try:
            ui_action = args[0].strip()
            action = self.game.ui_action_to_action(ui_action)
        except Exception as e:
            return (False,
                    "Unable to interpret action, \"{}\": {}".format(ui_action,
                                                                    str(e)))

        if len(args) > 1:
            ui_player = args[1].strip()
            try:
                player = self.game.ui_player_to_player(ui_player)
            except:
                return (False, "Unrecognized player, \"{}\"".format(ui_player))
            else:
                assert(player is not None)
                self.game.state.set_player_to_act(player)

        try:
            self.game.state.play(action)
        except Exception as e:
            return (False,
                    "Unable to take action, \"{}\", ({}): {}".format(ui_action,
                                                                     action,
                                                                     str(e)))

        return (True, ui_action)

    def do_genmove(self, args, opts=None):
        """Allow the agent to play a stone of the given colour (white/w or
        black/b).
        """
        if len(args) > 0:
            ui_player = args[0].strip()
            try:
                player = self.game.ui_player_to_player(ui_player)
            except:
                return (False, "Unrecognized player, \"{}\"".format(ui_player))
            else:
                self.game.state.set_player_to_act(player)
        try:
            action = self.agent.select_action(
                deepcopy(self.game.state),
                time_allowed_s=self.move_time
            )
            self.game.state.play(action)
        except Exception as e:
            return (True, "Unable to take action: " + str(e))
        else:
            return (True, self.game.action_to_ui_action(action))

    def do_showboard(self, args, opts=None):
        """Return an ASCII representation of the current state of the game
        board."""
        return (True, self.game.state_to_ui_state())

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

    def do_final_score(self, args, opts=None):
        """Return the final_score of the current game."""
        scores = [(self.game.state.score(p), p) for p in range(2)]

        if any(s is None for (s, _) in scores):
            return (True, "") # Game is not over yet.

        (score, winner) = max(scores)

        if score == 0:
            return (True, "0")
        return (True, "{}+{}".format(self.game.player_to_ui_player(winner),
                                     score))

    def do_analyze(self, arg, opts=None):
        """Added to avoid crashing with GTP tools but not yet implemented."""
        return (True, "")

    def do_undo(self, arg, opts=None):
        self.game.state.undo()
        return (True, "")
