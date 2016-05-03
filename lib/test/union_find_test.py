from games_puzzles_algorithms.union_find import UnionFind


def test_uf():
    patient = UnionFind()
    patient.merge(0, 1)
    assert patient.find(0) == patient.find(1)
    assert patient.connected(0, 1)

    assert patient.find(0) != patient.find(2)
    assert not patient.connected(0, 2)
