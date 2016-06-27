from flask import Flask, g, jsonify, render_template, request

import games_puzzles_algorithms.players.mcts.mcts_agent as mcts

import games_puzzles_algorithms.games.hex.game_state as game
import games_puzzles_algorithms.games.hex.color as color


class GameAndPlayerManager(object):
    ALGORITHMS = {
        'MCTS': mcts.MctsAgent.Mcts
    }

    def __init__(self, app, num_rows=2, num_columns=2, alg_name='MCTS'):
        self._state = game.GameState.root(num_rows, num_columns)
        self._alg = self.ALGORITHMS[alg_name]()

        @app.route('/', methods=['GET'])
        def index():
            return render_template('index.html')

        @app.route('/_search', methods=['GET'])
        def search():
            stats = self._alg.search(self._state, num_iterations=10)
            return jsonify(
                error=False,
                board=self._state.board._cells.tolist(),
                data={'statistics': stats, 'tree': self._alg.to_dict()})


if __name__ == '__main__':
    app = Flask(__name__)
    server = GameAndPlayerManager(app)

    app.debug = True
    app.run()
