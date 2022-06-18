# The 3-digit puzzle
Given are two 3-digit numbers called 𝑆 (start) and 𝐺 (goal) and also a set of 3-digit numbers called 𝑓𝑜𝑟𝑏𝑖𝑑𝑑𝑒𝑛. To solve the puzzle, we want to get from 𝑆 to 𝐺 in the smallest number of moves. A move is a transformation of one number into another number by adding or subtracting 1 to one of its digits. For example, a move can take you from 123 to 124 by adding 1 to the last digit or from 953 to 853 by subtracting 1 from the first digit. Moves must satisfy the following constraints:

+ You cannot add to the digit 9 or subtract from the digit 0;
+ You cannot make a move that transforms the current number into one of the forbidden numbers;
+ You cannot change the same digit twice in two successive moves.
+ Note that since the numbers have 3 digits, at the beginning there are at most 6 possible moves from 𝑆. After the first move, the branching factor is at most 4, due to the constraints on the moves and especially due to constraint 3.

For the purpose of this project numbers starting with 0, e.g. 018, are considered 3-digit numbers.

## Tasks
Write a program to find a solution of the puzzle using the following 6 search strategies: BFS, DFS, IDS, Greedy, A* and Hill-climbing. Use the Manhattan heuristic as a heuristic for A* and Greedy and also as the evaluation function in Hill-climbing.
The Manhattan heuristic for a move between two numbers A and B is the sum of the absolute differences of the corresponding digits of these numbers, e.g. ℎ(123, 492) = |1 − 4| + |2 − 9| + |3 − 2| = 11.

Avoid cycles. When selecting a node from the fringe for expansion, if it hasn’t been expanded yet, expand it, otherwise discard it. Hint: It is not just the three digits that you need to consider when determining if you have expanded a node before. Two nodes are the same if a) they have the same 3 digits; and b) they have the same ‘child’ nodes.
Generate the children in the following order:
+ 1 is subtracted from the first digit
+ 1 is added to the first digit
+ 1 is subtracted from the second digit
+ 1 is added to the second digit
+ 1 is subtracted from the third digit
+ 1 is added to the third digit
Example: the order of the children of node 678 coming from parent 668 is 578, 778, 677, 679. Note that there are no children for the second digit as it already has been changed in the previous move (constraint 3).

For the heuristic search strategies: if there are nodes with the same priority for expansion, expand the last added node.
Set a limit of 1000 expanded nodes maximum, and when it is reached, stop the search and print a message that the limit has been reached.

## Usage
The code in this repository is intended to be run from the command line with the following arguments:
+ A single letter representing the algorithm to search with
  + B for BFS
  + D for DFS
  + I for IDS
  + G for Greedy
  + A for A*
  + H for Hill-climbing.
+ The filename of a `.txt` file to open for the search details. 

This file requires the following three attributes:
+ A starting state
+ A goal state
+ An optional comma-seperated list of forbidden states (forbidden1,forbidden2,forbidden3,…,forbiddenN)

### Example

```
/* sample.txt */
345
555
355,445,554
```

This file asks the search algoritm to start at state 345 with a goal state of 555. The search may not pass through any of 355, 445 or 554. As the last line is optional, it may not be present in the file.

To initialise a search, call `main.py` from the command line with a letter corresponding to the search method and an input file
```
python main.py B sample.txt
```
