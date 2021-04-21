from tree import Tree
import sys
import os
from random import randint

class Container:
    """
    Container Class 
    ----------
    Handles data ingest, formatting and outputting requested search algorithm
    """
    def __init__(self, data):
        """
        Initialises the container
            * :param data (.txt file)): Text file containing start, goal and forbidden stats
        """
        self._file_in(data)

    def _reformat(self, state):
        """
            * :param (str): A string representing a state\n
        :return: A list with each item corresponding to a single digit in the state
        """
        return [int(digit) for digit in str(state)]

    def _file_in(self, filepath):
        """
            * :param (str): Filepath to input .txt file
        :return (tup): Reformatted start, goal and forbidden states
        """
        f = open(filepath, 'r')
        lines = f.readlines()
        num_lines = len(lines)

        assert not num_lines < 2, 'Either the start value, or goal value is missing! Please check the input.'
        assert not num_lines > 3, 'Too many values! Please check the input.'
        
        self.start, self.goal = self._reformat(lines[0].strip('\n')), self._reformat(lines[1].strip('\n'))

        if num_lines == 2:
            self.forbidden = []
        else:
            self.forbidden = [self._reformat(i.strip('\n')) for i in lines[2].split(',')]
    
    def compute(self, method):
        """
            * :param (str): Search method to use
        :return (None): Print of solution path and nodes expanded in search
        """
        tree = Tree(self.start, self.goal, self.forbidden)
        if method == 'B': 
            path, exp = tree.BFS()
        if method == 'D': 
            path, exp = tree.DFS()
        if method == 'I':
            path, exp = tree.IDS()
        if method == 'G': 
            path, exp = tree.greedy()
        if method == 'H': 
            path, exp = tree.hill_climb()
        if method == 'A': 
            path, exp = tree.A_star()
        print('==   PATH   == ')
        print(path)
        print('== EXPANDED == ')
        print(exp)

    @staticmethod
    def _test():
        _test = [
            ''.join([str(randint(0,9)) for i in range(3)])+'\n',
            ''.join([str(randint(0,9)) for i in range(3)])+'\n',
            ','.join([''.join([str(randint(0,9)) for i in range(3)]) for j in range(randint(0,50))])
        ]
        f_name = f'test{len(os.listdir("./generated_tests"))}.text'
        f = open(f'./generated_tests/{f_name}', 'w')
        f.write(''.join(_test))
        f.close()

        container = Container(f'./generated_tests/{f_name}')
        for method in ['B', 'D', 'I', 'G', 'H', 'A']:
            print(f'==  METHOD  ==')
            print(method)
            container.compute(method)
            print('===========================================')
        
        

def main():
    if sys.argv[1].lower() == 'test':
        Container._test()

    else:
        container = Container(sys.argv[2])
        container.compute(sys.argv[1])

if __name__ == '__main__':
    main()
    