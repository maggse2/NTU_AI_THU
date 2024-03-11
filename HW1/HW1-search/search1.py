# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    #implement an occur check to get better results
    occurred = []
    node_stack = util.Stack()
    current_node = problem.getStartState()

    path = []
    edge_stack = util.Stack()
    
    # run the loop until the current node is the goal state
    while not problem.isGoalState(current_node):
        if current_node not in occurred:
            occurred.append(current_node)
            for successor, direction, _ in problem.getSuccessors(current_node):
                node_stack.push(successor)
                #print('pushing to edge_stack:', path + [direction])
                edge_stack.push(path + [direction])
        current_node = node_stack.pop()
        #print('current node is goal:', problem.isGoalState(current_node))
        path = edge_stack.pop()
        #print("current path:", path)
    print("final path:", path)
    return path

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # to go from DFS to BFS, we just need to change the stack to a queue to go from FILO to FIFO
    occurred = []
    node_queue = util.Queue()
    current_node = problem.getStartState()

    path = []
    edge_queue = util.Queue()
    
    # run the loop until the current node is the goal state
    while not problem.isGoalState(current_node):
        if current_node not in occurred:
            occurred.append(current_node)
            for successor, direction, _ in problem.getSuccessors(current_node):
                node_queue.push(successor)
                #print('pushing to edge_stack:', path + [direction])
                edge_queue.push(path + [direction])
        current_node = node_queue.pop()
        #print('current node is goal:', problem.isGoalState(current_node))
        #print('edge_queue:', edge_queue.list)
        path = edge_queue.pop()
        #print("current path:", path)
    print("final path:", path)
    return path

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #UCS is similar or the same as the Lee Algortihm for pathfinding in EDA, but with weighted edges
    #use a priority queue to get the node with the lowest cost first (same goes for the edge)
    occurred = []
    node_queue = util.PriorityQueue()   #use a priority queue to get the node with the lowest cost
    current_node = problem.getStartState()

    path = []
    edge_queue = util.PriorityQueue()   #use a priority queue to get the edge with the lowest cost
    
    # run the loop until the current node is the goal state
    while not problem.isGoalState(current_node):
        if current_node not in occurred:
            occurred.append(current_node)
            for successor, direction, edge_cost in problem.getSuccessors(current_node):
                total_cost = problem.getCostOfActions(path) + edge_cost
                node_queue.push(successor, total_cost)
                #print('pushing to edge_stack:', path + [direction])
                edge_queue.push(path + [direction], total_cost)
        current_node = node_queue.pop()
        #print('current node is goal:', problem.isGoalState(current_node))
        #print('edge_queue:', edge_queue.list)
        path = edge_queue.pop()
        #print("current path:", path)
    print("final path:", path)
    return path

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #Astar ist the same as UCS, we only add the heuristic to the total cost
    occurred = []
    node_queue = util.PriorityQueue()
    current_node = problem.getStartState()

    path = []
    edge_queue = util.PriorityQueue()
    
    # run the loop until the current node is the goal state
    while not problem.isGoalState(current_node):
        if current_node not in occurred:
            occurred.append(current_node)
            for successor, direction, edge_cost in problem.getSuccessors(current_node):
                total_cost = problem.getCostOfActions(path) + edge_cost + heuristic(successor, problem)         #add the heuristic to the total cost
                node_queue.push(successor, total_cost)
                #print('pushing to edge_stack:', path + [direction])
                edge_queue.push(path + [direction], total_cost)
        current_node = node_queue.pop()
        #print('current node is goal:', problem.isGoalState(current_node))
        #print('edge_queue:', edge_queue.list)
        path = edge_queue.pop()
        #print("current path:", path)
    print("final path:", path)
    return path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
