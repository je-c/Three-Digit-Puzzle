class Node:
    """
    Node Class 
    ----------
    Stores a state in the search and supports various tree searching algorithms
    """
    def __init__(self, value, parent = None, depth = 0, last=None, h_n = 0):
        """
        Initialises a node
            * :param value (list(int)): List of integer values, each item stores a digit of the state.\n
            * :param parent (Node): Pointer to the parent of the node\n
            * :param depth (int): Value denoting depth in tree of the node\n
            * :param last (list(list(bool))): List of boolean maps for filtering out nodes visited in prior iteration\n
            * :param h_n (int): Value denoting the heuristic
        """
        if isinstance(value, list):
            self.value = value
        else:
            self.value = [int(i) for i in str(value)]

        if not last:
            self.last = [
                True, True, 
                True, True,
                True, True,
            ]
        else:
            self.last = last

        self.parent = parent
        if self.parent:
            self.depth = self.parent.depth + 1
        else:
            self.depth = depth

        self.h_n = h_n
        self.f_n = self.depth + self.h_n
        self.children = []