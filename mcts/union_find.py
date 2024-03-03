# Created by Luke Schultz
# Fall 2022, Winter 2023, Spring 2023, Summer 2023, Fall 2023
# Written with the help of GitHub Copilot

class UnionFind():
    def __init__(self, size):
        self.parent_list = [i for i in range(size)]

    def union(self, x: int, y: int) -> bool:
        """
        Joins two sets

        Parameters:
        x (int): member of one set
        y (int): member of (possibly) another set

        Returns:
        bool: False if x, y were in the same set prior to function call,
              True otherwise
        """

        repr_x = self.find(x)
        repr_y = self.find(y)

        if repr_x == repr_y:  # In the same disjoint set
            return False

        self.parent_list[repr_x] = y
        return True

    def find(self, x: int) -> int:
        """
        Find the repr of an element.

        Uses grandparent compression to speed up execution.

        Parameters:
        x (int): element to find repr of

        Returns:
        int: repr of x
        """

        while True:
            parent_x = self.parent_list[x]
            if x == parent_x:
                return x

            grandparent_x = self.parent_list[parent_x]
            if parent_x == grandparent_x:
                return parent_x

            # grandparent compression:
            self.parent_list[x], x = grandparent_x, grandparent_x
