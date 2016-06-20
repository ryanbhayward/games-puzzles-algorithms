from games_puzzles_algorithms.players.minimax.minimax_agent import MinimaxAgent
from games_puzzles_algorithms.games.hex.game_state import GameState


def test_one_by_one():
    state = GameState.root(1)
    assert str(state) == (
'''
  A
1  .  O
    @''')

    patient = MinimaxAgent()
    assert patient.value(state) == 1


def test_one_by_one_action():
    state = GameState.root(1)
    assert str(state) == (
'''
  A
1  .  O
    @''')

    patient = MinimaxAgent()
    assert patient.select_action(state) == 0


def test_two_by_two():
    state = GameState.root(2)
    assert str(state) == (
'''
  A  B
1  .  .  O
 2  .  .  O
     @  @''')

    patient = MinimaxAgent()
    assert patient.value(state) == 1

    state.play(0)
    assert str(state) == (
'''
  A  B
1  O  .  O
 2  .  .  O
     @  @''')

    assert patient.value(state) == 1

    state.undo()
    state.play(1)
    assert str(state) == (
'''
  A  B
1  .  .  O
 2  O  .  O
     @  @''')

    assert patient.value(state) == -1


def test_two_by_two_action():
    state = GameState.root(2)
    assert str(state) == (
'''
  A  B
1  .  .  O
 2  .  .  O
     @  @''')

    patient = MinimaxAgent()
    assert patient.select_action(state) == 1

    state.play(0)
    assert str(state) == (
'''
  A  B
1  O  .  O
 2  .  .  O
     @  @''')

    assert patient.select_action(state) == 2

    state.undo()
    state.play(1)
    assert str(state) == (
'''
  A  B
1  .  .  O
 2  O  .  O
     @  @''')

    assert patient.select_action(state) == 0
