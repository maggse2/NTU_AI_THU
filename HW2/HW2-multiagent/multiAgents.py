# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        # 10 points for every food you eat
        """
        Returns a Grid of boolean food indicator variables.

        Grids can be accessed via list notation, so to check
        if there is food at (x,y), just call

        currentFood = state.getFood()
        if currentFood[x][y] == True: ...
        """
        newCapsule = successorGameState.getCapsules()
        # 200 points for every ghost you eat
        # but no point for capsule

        # For Ghost
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        # Position of ghost do not change regardless of your state
        # because you can't predict the future
        ghostPositions = [ghostState.getPosition() for ghostState in newGhostStates]
        # Count down from 40 moves
        ghostStartPos = [ghostState.start.getPosition() for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        ghostProximity = 0
        reward = 0
        # if there are scared ghosts within 10 steps, hunt them
        for ghostStats in zip(ghostPositions, newScaredTimes):
            if ghostStats[1] > 0 and manhattanDistance(ghostStats[0], newPos) <= ghostStats[1]:
                reward += 200/manhattanDistance(ghostStats[0], newPos)
            
            # count proximity of ghosts to know whether to consider capsules
            else:
                # basic survival instinct
                if manhattanDistance(ghostStats[0], newPos) <= 2:
                    reward -= 999999


        
        # otherwise find closest POI
        
        # convert grid of boolean to list of tuples
        foodList = newFood.asList()
        reward -= 11 * len(foodList)
        if foodList != []:
            for food in foodList:
                reward += 10/(manhattanDistance(newPos, food)**2)

        
        reward -= 201 * len(newGhostStates)
        if newCapsule != []:
            for capsule in newCapsule:
                reward += 200/(manhattanDistance(newPos, capsule)+min([manhattanDistance(ghost, capsule) for ghost in ghostPositions]))
       
        

        

        return successorGameState.getScore() + reward # - len(foodList) * 10  - 200 * len(newGhostStates)
    
    

            
        
        #return successorGameState.getScore()  # default scoure
        # please change the return score as the score you want

        
                

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def minimax(gameState, depth, agentIndex):
            if gameState.isWin() or gameState.isLose() or (depth == self.depth and agentIndex == gameState.getNumAgents()):
                print("depth", depth)
                print("self.depth", self.depth)
                print("agentIndex", agentIndex)
                print("self.getNumAgents", gameState.getNumAgents())
                return self.evaluationFunction(gameState)
            
            if agentIndex == gameState.getNumAgents():
                print("depth", depth)
                return minimax(gameState, depth + 1, 0)
            
            if agentIndex == 0:
                # pacman gets the max value
                return max(minimax(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1) for action in gameState.getLegalActions(agentIndex))
            else:
                # ghosts get the min value
                return min(minimax(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1) for action in gameState.getLegalActions(agentIndex))
                
        actions = gameState.getLegalActions(0)
        return max(actions, key = lambda x: minimax(gameState.generateSuccessor(0, x), 1, 1))

    # pacman gets the max value
    #            return max(minimax(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1) for action in gameState.getLegalActions(agentIndex))
    #        else:
    #            # ghosts get the min value
    #            return min(minimax(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1) for action in gameState.getLegalActions(agentIndex))
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alphabeta(gameState, depth, agentIndex, alpha, beta):
            if gameState.isWin() or gameState.isLose() or depth >= self.depth:
                return [self.evaluationFunction(gameState)]
            
            if agentIndex == gameState.getNumAgents()-1:
                nextAgent = 0
                nextDepth = depth + 1
            else:
                nextAgent = agentIndex + 1
                nextDepth = depth

            if agentIndex == 0:
                v = [float('-inf')]
                for a in gameState.getLegalActions(agentIndex):
                    v = max(v, alphabeta(gameState.generateSuccessor(agentIndex, a), nextDepth, nextAgent, alpha, beta) + [a])
                    if v[0] > beta:
                        return v
                    alpha = max(alpha, v[0])
                return v
            else:
                v = [float('inf')]
                for a in gameState.getLegalActions(agentIndex):
                    v = min(v, alphabeta(gameState.generateSuccessor(agentIndex, a), nextDepth, nextAgent, alpha, beta) + [a])
                    if v[0] < alpha:
                        return v
                    beta = min(beta, v[0])
                return v
            
        return alphabeta(gameState, 0, 0, float('-inf'), float('inf'))[-1]
    
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

