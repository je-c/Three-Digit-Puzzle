from node import Node
from itertools import compress

class Tree:
    """
    Tree Class 
    ----------
    Stores a tree of states, preserving node-to-node relation and supporting various search algorithms
    """
    def __init__(self, root, goal, forbidden):
        """
        Initialises a tree
            * :param root (list(int)): List of integer values denoting the root node's state.
            * :param goal (list(int)): List of integer values denoting the goal node's state.
            * :param forbidden (list(list(int))): List of lists of integer values denoting the forbidden states in the tree.
        """
        self.root = root
        self.goal = goal
        self.forbidden = forbidden
        self.expanded = []
        self.fringe = []

    def expanded_valid_size(self, exact = False):
        """ 
        :return (bool): Whether the list of expanded nodes is able to support any more.
        """
        return len(self.expanded) < 1000

    def fringe_is_empty(self):
        """ 
        :return (bool): Whether the fringe is empty.
        """
        return len(self.fringe) < 1
    
    def mannhatten_dist(self, a, b):
        """ 
            * :param a (Node): Node a
            * :param b (Node): Node b
        :return (int):  Manhatten distance heuristic between node a and node b
        """
        return sum([abs(i-j) for i, j in zip(a, b)])

    def reshuffle_fringe(self, heuristic):
        """
        :param heuristic (str): Heuristic used to determine order\n
        :return (list): Reshuffled fringe, ties with lowest heuristic value are swapped so last added is first
        """
        last_tie = 0
        for idx, node in enumerate(self.fringe):
            params = {
                'h_n': (node.h_n, self.fringe[0].h_n),
                'f_n': (node.f_n, self.fringe[0].f_n)
            }
            if idx == last_tie:
                continue
            if params[heuristic][0] == params[heuristic][1]:
                last_tie = idx
        return [self.fringe.pop(last_tie)] + self.fringe

    def get_children(self, current_node, heuristic = False):
        """
        Generates the children of a node following the rules that;
            - A child is generated by either adding or subtracting 1 from one of the 3 digits
            - Cannot add to a '9' or subtract from a '0'
            - Cannot generate a child listed as forbidden
            - Cannot generate a child by (in)decrementing a digit if the parent was generated by
              (in)decrementing that same digit

            * :param current_node (Node): Node to generate children for.
            * :param heuristic (int): Heuristic value for informed search algorithms

        :return (None): .children, .edges attributes for the node
        """
        #Placeholders for all possible combinations
        staged_values = [
            [current_node.value[0], current_node.value[1], current_node.value[2]] for i in range(6)
        ]

        #Placeholders for all possible combinations of previous expansion maps
        staged_lasts = [
            [False, False, True, True, True, True],  #0 - [0]-1
            [False, False, True, True, True, True],  #1 - [0]+1
            [True, True, False, False, True, True],  #2 - [1]-1
            [True, True, False, False, True, True],  #3 - [1]+1
            [True, True, True, True, False, False],  #4 - [2]-1
            [True, True, True, True, False, False]   #5 - [2]+1
        ]
        
        #Note what possible values dont meet Criteria 1
        rm_idx = []
        idx = [*range(0,6)]
        
        for i, j in zip(range(0, 5, 2), range(0, 3)):
            if staged_values[i][j] == 0:
                rm_idx.append(i)
        for i, j in zip(range(1, 6, 2), range(0, 3)):
            if staged_values[i][j] == 9:
                rm_idx.append(i)

        #Define positional transforms
        transform_map = {
            i: (
                (int((i)/2), -1) if i % 2 == 0 else (int((i)/2), 1)
            ) for i in range(6)
        }

        #Nullify invalid transforms
        for i in rm_idx:
            transform_map[i] = (transform_map[i][0], 0)

        #Transform remaining values in line with position
        transforms = [transform_map[x] for x in idx]
        for transform, child in zip(transforms, staged_values):
            child[transform[0]] += transform[1]

        #Tether staged and transformed values to staged lasts arrays
        staged_children = [
            (i, j) for i, j in zip(staged_values, staged_lasts)
        ]

        #Remove values of which that digit was transformed last iteration (Criteria 3)
        valid_children = list(
            compress(
                staged_children, 
                current_node.last
            )
        )

        #Remove any forbidden values (Criteria 2)
        for val in self.forbidden:
            for item in valid_children:
                if val in item:
                    valid_children.remove(item)
        
        #Remove any untransformed values (copies of parent)
        repr_flags = []
        for item in valid_children:
            if current_node.value == item[0]:
                repr_flags.append(False)
            else:
                repr_flags.append(True)

        valid_children = list(
            compress(
                valid_children, 
                repr_flags
            )
        )
        #Return valid children
        if heuristic:
            current_node.children = [
                Node(
                    value = i[0], 
                    parent = current_node, 
                    depth = current_node.depth + 1, 
                    last = i[1],
                    h_n = self.mannhatten_dist(self.goal, i[0])
                ) for i in valid_children
            ]
        else:
            current_node.children = [
                Node(
                    value = i[0], 
                    parent = current_node, 
                    depth = current_node.depth + 1, 
                    last = i[1],
                    h_n = 0
                ) for i in valid_children
            ]   
    
    def _condense(self, ls):
        """ 
            * :param ls (list): list of node values in digit form
        :return (str): Decomposed node value formatting.
        """
        return ','.join([''.join([str(j) for j in i.value]) for i in ls])

    def _trace(self, node, path = []):
        """ 
            * :param node (Node): Node to trace back from
            * :param path (list (optional)): Path calculated so far
        :returns (list): Path from node to root
        """
        path.append(node)
        if node.parent: return self._trace(node.parent, path) 

        path.reverse()
        return path

    def _visited(self, node, local_list = False):
        """ 
            * :param node (Node): Node to check
            * :param local_list (list (optional)): For IDS, whether to parse a localised expanded nodes list.
        :return (bool): Boolean representation for if the node has been visited previously in the search
        """
        if local_list:
            for expanded_node in local_list:
                if node.value == expanded_node.value:
                    if self._compare(node, expanded_node):
                        return True
            return False
        else:
            for expanded_node in self.expanded:
                if node.value == expanded_node.value:
                    if self._compare(node, expanded_node):
                        return True
            return False


    def _compare(self, a, b):
        """ 
            * :param a (Node): Node a.
            * :param b (Node): Node b.
        :returns (bool): Boolean representing whether nodes are identical. 
        """
        dim_a, dim_b = len(a.children), len(b.children)
        if any((dim_a == 0, dim_b == 0)):
            return False
        if dim_a != dim_b:
            return False
        for a_child, b_child in zip(a.children, b.children):
            if a_child.value != b_child.value:
                return False
        return True

    def _solution(self, node):
        """ 
            * :param node (Node): Node for which to trace from
        :returns ((str, str)): String path from root to node, string representation of nodes expanded in search. 
        """
        return self._condense(self._trace(node)), self._condense(self.expanded)

    def BFS(self):
        """
        ====================
        Breadth First Search
        ====================
        :returns (tup): tuple(path, expanded nodes) if iteration depth not exceeded, else tuple('No solution found', expanded)
        """
        self.fringe.append(Node(self.root))

        while self.expanded_valid_size():
            if self.fringe_is_empty():
                break
            
            cur = self.fringe.pop(0)
            self.get_children(cur)

            if self._visited(cur):
                continue

            self.expanded.append(cur)

            if cur.value == self.goal:
                return self._solution(cur)

            self.fringe = self.fringe + cur.children
    
        return "No solution found", self._condense(self.expanded)

    def DFS(self):
        """
        ===================
        Depth First Search
        ===================
        :returns (tup): tuple(path, expanded nodes) if iteration depth not exceeded, else tuple('No solution found', expanded)
        """
        self.fringe.append(Node(self.root))

        while self.expanded_valid_size():
            if self.fringe_is_empty():
                break

            cur = self.fringe.pop(0)
            self.get_children(cur)

            if self._visited(cur):
                continue 

            self.expanded.append(cur)

            if cur.value == self.goal:
                return self._solution(cur)

            self.fringe = cur.children + self.fringe 
        
        return "No solution found", self._condense(self.expanded)

    def IDS(self):
        """
        ===================
        Iterative Deepening Search
        ===================
        :returns (tup): tuple(path, expanded nodes) if iteration depth not exceeded, else tuple('No solution found', expanded)
        """
        limit = 0
        while self.expanded_valid_size(): 
            self.fringe = [Node(self.root)]
            visited_local = []
            first_loop = True

            while not self.fringe_is_empty():
                if self.fringe_is_empty():
                    break

                cur = self.fringe.pop(0)
                self.get_children(cur)

                if first_loop:
                    first_loop = False

                elif self._visited(cur, visited_local):
                    continue
                
                if self.expanded_valid_size():
                    visited_local.append(cur)
                    self.expanded.append(cur)

                if cur.value == self.goal:
                    return self._solution(cur) 

                if cur.depth < limit:
                    self.fringe = cur.children + self.fringe 

            limit += 1

        return "No solution found", self._condense(self.expanded)

    def greedy(self):
        """
        ===================
        Greedy Search
        ===================
        :returns (tup): tuple(path, expanded nodes) if iteration depth not exceeded, else tuple('No solution found', expanded)
        """
        self.fringe.append(Node(self.root))

        while self.expanded_valid_size():
            if self.fringe_is_empty():
                break

            cur = self.fringe.pop(0)
            self.get_children(cur, heuristic=True)

            if self._visited(cur):
                continue

            self.expanded.append(cur)
            
            if cur.value == self.goal:
                return self._solution(cur)

            self.fringe += cur.children
            self.fringe.sort(key=lambda node: node.h_n)
            if not self.fringe_is_empty():
                self.fringe = self.reshuffle_fringe('h_n')
        
        return "No solution found", self._condense(self.expanded)

    def A_star(self):
        """
        ===================
        A* Search
        ===================
        :returns (tup): tuple(path, expanded nodes) if iteration depth not exceeded, else tuple('No solution found', expanded)
        """
        self.fringe.append(Node(self.root))

        while self.expanded_valid_size():
            if self.fringe_is_empty():
                break 

            cur = self.fringe.pop(0)
            self.get_children(cur, heuristic=True)

            if self._visited(cur):
                continue

            self.expanded.append(cur)
            
            if cur.value == self.goal:
                return self._solution(cur)
            
            self.fringe += cur.children
            self.fringe.sort(key = lambda node: node.f_n)
            if not self.fringe_is_empty():
                self.fringe = self.reshuffle_fringe('f_n')

        return "No solution found", self._condense(self.expanded)
    
    def hill_climb(self):
        """
        ===================
        Hill Climb Search
        ===================
        :returns (tup): tuple(path, expanded nodes) if iteration depth not exceeded, else tuple('No solution found', expanded)
        """
        self.fringe.append(Node(self.root, h_n = self.mannhatten_dist(self.root, self.goal)))

        while self.expanded_valid_size():
            if self.fringe_is_empty():
                break

            cur = self.fringe.pop(0)
            self.get_children(cur, heuristic=True)

            if self._visited(cur):
                continue

            self.expanded.append(cur)

            if cur.value == self.goal:
                return self._solution(cur)
            
            self.fringe = cur.children
            self.fringe.sort(key = lambda node: node.h_n)
            if not self.fringe_is_empty():
                self.fringe = self.reshuffle_fringe('h_n')
                if self.fringe[0].h_n > cur.h_n:
                    break
                
        return "No solution found", self._condense(self.expanded)