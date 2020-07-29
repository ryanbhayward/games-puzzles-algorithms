from copy import copy


class UnionFind:
    """
    Union-find data structure specialized for finding hex connections.
    Implementation inspired by UAlberta CMPUT 275 2015 class notes.
    """
    def __init__(self):
        """
        Initialize parent and rank as empty dictionary, we will
        lazily add items as necessary.
        """
        self.parent = {}
        self.rank = {}

    def set_from_raw(self, raw):
        self.parent = raw[0]
        self.rank = raw[1]

    def copy_from_raw(self, raw):
        self.parent = copy(raw[0])
        self.rank = copy(raw[1])

    def copy_raw(self):
        return (copy(self.parent), copy(self.rank))

    def join(self, x, y):
        """
        Merge the groups of x and y if they were not already,
        return False if they were already merged, true otherwise
        """
        rep_x = self.find(x)
        rep_y = self.find(y)

        if rep_x == rep_y:
            return False
        if self.rank[rep_x] < self.rank[rep_y]:
            self.parent[rep_x] = rep_y
        elif self.rank[rep_x] > self.rank[rep_y]:
            self.parent[rep_y] = rep_x
        else:
            self.parent[rep_x] = rep_y
            self.rank[rep_y] += 1
        return True

    merge = join

    def find(self, x):
        """
        Get the representative element associated with the set in
        which element x resides. Uses grandparent compression to compression
        the tree on each find operation so that future find operations are faster.
        """
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0

        px = self.parent[x]
        if x == px: return x

        gx = self.parent[px]
        if gx==px: return px

        self.parent[x] = gx

        return self.find(gx)

    def connected(self, x, y):
        """
        Check if two elements are in the same group.
        """
        return self.find(x)==self.find(y)

    def elements(self):
        return list(self.parent.keys())
