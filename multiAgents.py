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

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
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

    def evaluationFunction(self, currentGameState, action):
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
        food_list = newFood.asList() #list of coordinates of food
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        power_list = successorGameState.getCapsules() #list of power pallets
        ghost_list = []
        for ghost in newGhostStates:
            ghost_list.append(ghost.getPosition())

        "*** YOUR CODE HERE ***"
        #good if its close to food
        #great if its close to power
        #great if its close to scared ghost
        #bad if its close to ghost
        min_distance_to_food = 10000
        min_distance_to_power = 10000
        min_distance_to_ghost = 10000
        for food in food_list:
            if manhattanDistance(newPos, food) < min_distance_to_food:
                min_distance_to_food = manhattanDistance(newPos, food)

        for power in power_list:
            if manhattanDistance(newPos, power) < min_distance_to_power:
                min_distance_to_power = manhattanDistance(newPos, power)

        for ghost in ghost_list:
            if manhattanDistance(newPos, ghost) < min_distance_to_ghost:
                min_distance_to_ghost = manhattanDistance(newPos, ghost)
        if min_distance_to_ghost < 2:
            return -10000
        if action == "STOP":
            return -10000
        score = -35*len(power_list)-30*len(food_list) + 3 / min_distance_to_food + 5/min_distance_to_power
        return score

def scoreEvaluationFunction(currentGameState):
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
    def node_value(self, gameState, depth, index): #get the value of any node
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        elif index == 0:
            return self.max_value(gameState, depth)
        else:
            return self.min_value(gameState, depth, index)

    def max_value(self, gameState, depth): #maximum utility for pacman at the current state and depth
        v = -100000000000000000
        for actions in gameState.getLegalActions(0): #getting legal actions of pacman at the state
            v = max(v, self.node_value(gameState.generateSuccessor(0, actions), depth, 1))
        return v

    def min_value(self, gameState, depth, index): #minimum utility for ghosts
        v = 100000000000000000
        for actions in gameState.getLegalActions(index):
            if index == gameState.getNumAgents() - 1:
                v = min(v, self.node_value(gameState.generateSuccessor(index, actions), depth + 1,  0))
            else:
                v = min(v, self.node_value(gameState.generateSuccessor(index, actions), depth, index + 1))
        return v
    def getAction(self, gameState):
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
        max_value = -100000000000000000 #very small number
        best_action = Directions.STOP
        for actions in gameState.getLegalActions(0):
            next_state = gameState.generateSuccessor(0, actions)
            next_value = self.node_value(next_state, 0, 1)
            if next_value > max_value:
                max_value = next_value
                best_action = actions
        return best_action

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def node_value(self, gameState, depth, index, alpha, beta): #get the value of any node
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        elif index == 0:
            return self.max_value(gameState, depth, alpha, beta)
        else:
            return self.min_value(gameState, depth, index, alpha, beta)

    def max_value(self, gameState, depth, alpha, beta):
        v = -1000000000000
        for actions in gameState.getLegalActions(0):
            v = max(v, self.node_value(gameState.generateSuccessor(0, actions), depth, 1, alpha, beta))
            if v > beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, gameState, depth, index, alpha, beta): #minimum utility for ghosts
        v = 1000000000000
        for actions in gameState.getLegalActions(index):
            if index == gameState.getNumAgents() - 1:
                v = min(v, self.node_value(gameState.generateSuccessor(index, actions), depth + 1,  0, alpha, beta))
                if alpha > v:
                    return v
                beta = min(beta, v)
            else:
                v = min(v, self.node_value(gameState.generateSuccessor(index, actions), depth, index + 1, alpha, beta))
                if alpha > v:
                    return v
                beta = min(beta, v)
        return v


    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        max_value = -100000000000000000 #very small number
        best_action = Directions.STOP
        alpha = -100000000000000000
        beta = 100000000000000000
        for actions in gameState.getLegalActions(0):
            next_state = gameState.generateSuccessor(0, actions)
            next_value = self.node_value(next_state, 0, 1, alpha, beta)
            if next_value > max_value:
                max_value = next_value
                best_action = actions
            alpha = max(alpha, max_value)
        return best_action

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def node_value(self, gameState, depth, index): #get the value of any node
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        if index == 0:
            return self.max_value(gameState, depth)
        if index != 0:
            return self.expecti_value(gameState, index, depth)

    def expecti_value(self, gameState, index, depth):
        v = 0
        if index == 0:
            return self.max_value(gameState, depth)
        else:
            for actions in gameState.getLegalActions(index):
                if index == gameState.getNumAgents() - 1:
                    v += self.node_value(gameState.generateSuccessor(index, actions), depth + 1, 0) / (len(gameState.getLegalActions(index)))
                else:
                    v += self.node_value(gameState.generateSuccessor(index, actions), depth, index + 1) / (len(gameState.getLegalActions(index)))
            return v

    def max_value(self, gameState, depth): #maximum utility for pacman at the current state and depth
        v = -100000000000000000
        for actions in gameState.getLegalActions(0): #getting legal actions of pacman at the state
            v = max(v, self.node_value(gameState.generateSuccessor(0, actions), depth, 1))
        return v

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        result_value = -10000000000000 #very small number
        best_action = Directions.STOP
        for actions in gameState.getLegalActions(0):
            next_state = gameState.generateSuccessor(0, actions)
            next_value = self.node_value(next_state, 0, 1)
            if next_value > result_value:
                result_value = next_value
                best_action = actions
        return best_action
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <I imagined as if I was playing the game of Pacman and designed this
    evaluation function. First thing I considered was that I should alwasy stay away
    from the ghost agents unless they were scared. So if the minimum distance to the
    ghost was less than two I gave a negative score. Also, I wanted my agent to eat
    the power pellet as soon as possible so he could gain freedom to move anywhere
    starting earlier in the game. Hence, I subtracted 40 times the number of remaining
    power pellets. I also wanted to motivate my agent to eat food as quickly as possible
    so I subtracted 25 times the number of remaining food. Lastly, I wanted pacman
    to move closer to the power pellet and food.>
    """
    currentPos = currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood()
    food_list = currentFood.asList() #list of coordinates of food
    currentGhostStates = currentGameState.getGhostStates()
    currentScaredTimes = [ghostState.scaredTimer for ghostState in currentGhostStates]
    current_power_list = currentGameState.getCapsules() #list of power pallets
    ghost_list = []
    for ghost in currentGhostStates:
        ghost_list.append(ghost.getPosition())

    "*** YOUR CODE HERE ***"
    #good if its close to food
    #great if its close to power
    #great if its close to scared ghost
    #bad if its close to ghost
    min_distance_to_food = 10000
    min_distance_to_power = 10000
    min_distance_to_ghost = 10000
    for food in food_list:
        if manhattanDistance(currentPos, food) < min_distance_to_food:
            min_distance_to_food = manhattanDistance(currentPos, food)

    for power in current_power_list:
        if manhattanDistance(currentPos, power) < min_distance_to_power:
            min_distance_to_power = manhattanDistance(currentPos, power)

    for ghost in ghost_list:
        if manhattanDistance(currentPos, ghost) < min_distance_to_ghost:
            min_distance_to_ghost = manhattanDistance(currentPos, ghost)
    if min_distance_to_ghost < 2:
        return -10000
    score = -40*len(current_power_list)-25*len(food_list) + 3 / min_distance_to_food + 5/min_distance_to_power
    return score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
