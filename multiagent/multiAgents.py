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
import random, util, extra

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        curPos = currentGameState.getPacmanPosition()
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        ghostsPos = successorGameState.getGhostPositions()

        "*** YOUR CODE HERE ***"
        score = successorGameState.getScore()
        nearestGhost = 1000
        curToNearestGhost = 0
        # looping through all the ghosts and find what is the nearest ghost and how near
        for ghostPos in ghostsPos:
            nearGhost = manhattanDistance(ghostPos, newPos)
            if(nearGhost < nearestGhost):
                nearestGhost = nearGhost
                curToNearestGhost = manhattanDistance(ghostPos, curPos)

        nearestFood = 1000
        curToNearestFood = 0
        # this simply loops through the food in the foodlist to know what is the closest food
        for food in newFood.asList():
            nearFood = manhattanDistance(food, newPos)
            if(nearFood < nearestFood):
                nearestFood = nearFood
                curToNearestFood = manhattanDistance(food, curPos)
        # this condition takes care when pacman is near to the ghost while far from the nearest food
        if(nearestFood >= nearestGhost):
                # meaning that pacman is getting near to the nearest food and getting far from the ghost
                if(nearestGhost > curToNearestGhost and nearestFood < curToNearestFood):
                    score += 2
                else:
                    # as long as the nearest ghost has distance of 2 and greater
                    if(nearGhost > 2):
                        # we will still persue the food here
                        if(nearestFood < curToNearestFood):
                            score += 1
                    else:
                        # meaning that the ghost is pretty much near
                        score -= 1
        # if the nearest food is nearer than the ghost
        if(nearestFood < nearestGhost):
            if(nearestFood < curToNearestFood):
                score += 1
            else:
                score -= 1
        # HINTS:
        # Given currentGameState and successorGameState, determine if the next state is good / bad
        # Compute a numerical score for next state that will reflect this
        # Base score = successorGameState.getScore() - Line 77
        # Can increase / decrease this score depending on:
        #   new pacman position, ghost position, food position,
        #   distances to ghosts, distances to food
        # You can choose which features to use in your evaluation function
        # You can also put more weight to some features
        print score
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
        """
        "*** YOUR CODE HERE ***"
        currentDepth = 0
        currentAgentIndex = self.index # agent's index
        action,score = self.value(gameState, currentAgentIndex, currentDepth)
        return action

    # Note: always returns (action,score) pair
    def value(self, gameState, currentAgentIndex, currentDepth):
        # we will use the same function as the alpha beta prunning only that we set the alpha and beta into None
      return extra.value(self, gameState, currentAgentIndex, currentDepth, 1, None, None)
      # Check when to update depth
      # check if currentDepth == self.depth
      #   if it is, stop recursion and return score of gameState based on self.evaluationFunction
      # check if gameState.isWin() or gameState.isLose()
      #   if it is, stop recursion and return score of gameState based on self.evaluationFunction
      # check whether currentAgentIndex is our pacman agent or ghost agent
      # if our agent: return max_value(....)
      # otherwise: return min_value(....)



    # Note: always returns (action,score) pair
    def max_value(self, gameState, currentAgentIndex, currentDepth):
        # we will use the same function as the alpha beta prunning only that we set the alpha and beta into None
      return extra.max_value(self, gameState, currentAgentIndex, currentDepth, None, None)

      # current_value = -inf
      # loop over each action available to current agent:
      # (hint: use gameState.getLegalActions(...) for this)
      #     use gameState.generateSuccessor to get nextGameState from action
      #     compute value of nextGameState by calling self.value
      #     compare value of nextGameState and current_value
      #     keep whichever value is bigger, and take note of the action too
      # return (action,current_value)

    # Note: always returns (action,score) pair
    def min_value(self, gameState, currentAgentIndex, currentDepth):
        # we will use the same function as the alpha beta prunning only that we set the alpha and beta into None
      return extra.min_value(self, gameState, currentAgentIndex, currentDepth, None, None)
      # current_value = inf
      # loop over each action available to current agent:
      # (hint: use gameState.getLegalActions(...) for this)
      #     use gameState.generateSuccessor to get nextGameState from action
      #     compute value of nextGameState by calling self.value
      #     compare value of nextGameState and current_value
      #     keep whichever value is smaller, and take note of the action too
      # return (action,current_value)



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        currentDepth = 0
        currentAgentIndex = self.index # agent's index
        alpha = float('inf') * -1
        beta = float('inf')
        action,score = self.value(gameState, currentAgentIndex, currentDepth, alpha, beta)
        return action

    # Note: always returns (action,score) pair
    def value(self, gameState, currentAgentIndex, currentDepth, alpha, beta):
      return extra.value(self, gameState, currentAgentIndex, currentDepth, 2, alpha, beta)
      # More or less the same with MinimaxAgent's value() method
      # Just update the calls to max_value and min_value (should now include alpha, beta params)

    # Note: always returns (action,score) pair
    def max_value(self, gameState, currentAgentIndex, currentDepth, alpha, beta):
        return extra.max_value(self, gameState, currentAgentIndex, currentDepth, alpha, beta)
      # Similar to MinimaxAgent's max_value() method
      # Include checking if current_value is worse than beta
      #   if so, immediately return current (action,current_value) tuple
      # Include updating of alpha

    # Note: always returns (action,score) pair
    def min_value(self, gameState, currentAgentIndex, currentDepth, alpha, beta):
        return extra.min_value(self, gameState, currentAgentIndex, currentDepth, alpha, beta)
      # Similar to MinimaxAgent's min_value() method
      # Include checking if current_value is worse than alpha
      #   if so, immediately return current (action,current_value) tuple
      # Include updating of beta

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        currentDepth = 0
        currentAgentIndex = self.index # agent's index
        action,score = self.value(gameState, currentAgentIndex, currentDepth)
        return action

    # Note: always returns (action,score) pair
    def value(self, gameState, currentAgentIndex, currentDepth):
      return extra.value(self, gameState, currentAgentIndex, currentDepth, 3, None, None)
      # More or less the same with MinimaxAgent's value() method
      # Only difference: use exp_value instead of min_value

    # Note: always returns (action,score) pair
    def max_value(self, gameState, currentAgentIndex, currentDepth):
      return extra.max_value(self, gameState, currentAgentIndex, currentDepth, None, None)
      # Exactly like MinimaxAgent's max_value() method

    # Note: always returns (action,score) pair
    def exp_value(self, gameState, currentAgentIndex, currentDepth):
      return extra.exp_value(self, gameState, currentAgentIndex, currentDepth)
      # use gameState.getLegalActions(...) to get list of actions
      # assume uniform probability of possible actions
      # compute probabilities of each action
      # be careful with division by zero
      # Compute the total expected value by:
      #   checking all actions
      #   for each action, compute the score the nextGameState will get
      #   multiply score by probability
      # Return (None,total_expected_value)
      # None action --> we only need to compute exp_value but since the
      # signature return values of these functions are (action,score), we will return an empty action


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    score = currentGameState.getScore()
    curPos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    ghostsPos = currentGameState.getGhostPositions()

    nearestGhost = float('inf')
    for ghostPos in ghostsPos:
        nearGhost = manhattanDistance(ghostPos, curPos)
        if(nearGhost < nearestGhost):
            nearestGhost = nearGhost
    score -= nearestGhost

    nearestFood = float('inf')
    for food in food.asList():
        nearFood = manhattanDistance(food, curPos)
        if(nearFood < nearestFood):
            nearestFood = nearFood
    # since it looks the same with the q1 we used the logic but much simplier
    # if the ghost is nearer than the food
    if(nearestFood >= nearestGhost):
        # as long as the ghost has a manhattanDistance of 2 or greater we will pursue the path
        if(nearestGhost > 2):
            score += 1
        # but if it is almost next to pacman then we get away from there
        else:
            score -= 1
    # if the food is nearer than the ghost, we will highly encourage pacman to go that path by increasing the score by 2
    if(nearestFood < nearestGhost):
        score += 2
    # Similar to Q1, only this time there's only one state (no nextGameState to compare it to)
    # Use similar features here: position, food, ghosts, scared ghosts, distances, etc.
    # Can use manhattanDistance() function
    # You can add weights to these features
    # Update the score variable (add / subtract), depending on the features and their weights
    # Note: Edit the Description in the string above to describe what you did here
    # print nearestGhost, nearestFood
    # if(nearestFood < nearestGhost):
    #   score += nearestFood

    # if(nearestGhost < 10):
    #   score -= nearestGhost

    return score

# Abbreviation
better = betterEvaluationFunction
