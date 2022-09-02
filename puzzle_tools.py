"""
This module contains the functions that find solutions to puzzles, step by step.
"""

from __future__ import annotations
from typing import List, Optional, Union, Any
from puzzle import Puzzle

from collections import deque


import sys
sys.setrecursionlimit(10**6)



def depth_first_solve(puzzle: Puzzle) -> PuzzleNode:
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.
    """
    seen = set()
    new_puzzle = [PuzzleNode(puzzle)]

    while len(new_puzzle) > 0:
        item = new_puzzle.pop()
        for ext in item.puzzle.extensions():
            if ext.is_solved():
                return PuzzleNode(ext)
            if ext.fail_fast() or\
               ext.__str__() in seen or ext.extensions == []:
                continue
                
            new_node = PuzzleNode(ext)
            seen.add(new_node.puzzle.__str__())
            new_puzzle.append(new_node)
        
    return None
            
    

def breadth_first_solve(puzzle: Puzzle) -> PuzzleNode:
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.
    """
    seen = set()
    new_puzzle = [PuzzleNode(puzzle)]

    while len(new_puzzle) > 0:
        item = new_puzzle.pop(0)
        for ext in item.puzzle.extensions():
            if ext.is_solved():
                return PuzzleNode(ext)
            if ext.fail_fast() or\
               ext.__str__() in seen or ext.extensions() == []:
                continue

            new_node = PuzzleNode(ext)
            seen.add(new_node.puzzle.__str__())
            new_puzzle.append(new_node)
    return None
    


class PuzzleNode:
    """
    The class PuzzleNode helps build trees of PuzzleNodes that have
    an arbitrary number of children, and a parent.

    === Attributes ===
    puzzle: Optional[Puzzle]
        The configuration (layout) of this puzzle
    children: List[PuzzleNode]
        A list of puzzle nodes that contain puzzles which are extensions (one
        step away) from this puzzle
    parent: Optional[PuzzleNode]
        An optional puzzle node containing a puzzle for which this node's
        puzzle is an extension (one step away) from
    """
    puzzle: Optional[Puzzle]
    children: List[PuzzleNode]
    parent: Optional[PuzzleNode]

    def __init__(self, puzzle: Optional[Puzzle] = None, \
                 children: Optional[List[PuzzleNode]] = None, \
                 parent: Optional[PuzzleNode] = None) -> None:
        """
        Create a new puzzle node self with configuration <puzzle>,
        <children> and <parent>.
        """

        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other: Union[PuzzleNode, Any]) -> bool:
        """
        Return whether this PuzzleNode is equivalent to <other>.

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1.__eq__(pn2)
        True
        >>> pn1.__eq__(pn3)
        False
        """

        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self) -> str:
        """
        Return a human-readable string representing PuzzleNode self.
        """

        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))
