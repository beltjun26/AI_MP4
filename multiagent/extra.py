def value(self, gameState, currentAgentIndex, currentDepth, type, alpha, beta):
    if(currentAgentIndex == gameState.getNumAgents()):
        currentAgentIndex = 0
        currentDepth += 1
    if(currentDepth == self.depth):
        return (None, self.evaluationFunction(gameState))
    # will just return the value since it's already win or lose
    if(gameState.isWin() or gameState.isLose()):
        return (None, self.evaluationFunction(gameState))
    # the type variable will tell whenever we use the function from the minmax or alpha beta
    # since currentAgentIndex tells which turn it is. since we need the pacman agent to always run the max and for the ghost agent to
    # run the min always
    if(currentAgentIndex == 0):
		if(type == 2):
			val = self.max_value(gameState, currentAgentIndex, currentDepth, alpha, beta)
		else:
			val = self.max_value(gameState, currentAgentIndex, currentDepth)
    else:
    	if(type == 1):
    		val = self.min_value(gameState, currentAgentIndex, currentDepth)
    	elif(type == 2):
    		val = self.min_value(gameState, currentAgentIndex, currentDepth, alpha, beta)
    	else:
            # this is for the expectimax problem
    		val = self.exp_value(gameState, currentAgentIndex, currentDepth)
    return val

def exp_value(self, gameState, currentAgentIndex, currentDepth):
    v = 0
    actionToTake = None
    legalActions = gameState.getLegalActions(currentAgentIndex)
    # computing the probability
    prob = 1.0/len(legalActions)
    # looping throught the possible action that pactman can do.
    for availAction in legalActions:
        successorState = gameState.generateSuccessor(currentAgentIndex, availAction)
        # this line will serve as recursion point for the value function
        next_action, next_v = self.value(successorState, currentAgentIndex+1, currentDepth)
        # will compute for the v
        v = v + (next_v * prob)
    return (None, v)

def max_value(self, gameState, currentAgentIndex, currentDepth, alpha, beta):
    current_value = -100000
    actionToTake = None
    legalActions = gameState.getLegalActions(currentAgentIndex);
    # this will loop for the possible action of pacman
    for availAction in legalActions:
        successorState = gameState.generateSuccessor(currentAgentIndex, availAction)
        # this will reserve as recursion for the value function, and the setup will go so that the bottom of the tree will first be evaluated.
        next_action, next_score = self.value(successorState, currentAgentIndex+1, currentDepth) if not(alpha or beta) else self.value(successorState, currentAgentIndex+1, currentDepth, alpha, beta)
        # sinc the score of the next move is better than the current score then we will set the action to take to current interation's action
        if(next_score > current_value):
            current_value = next_score
            actionToTake = availAction
        # if we have alpha and beta value meaning we are using the function for alpoha and beta prunning
        if(alpha and beta):
            # following the algorithm for the alpha and beta prunning if the value is greater the beta we continue
            # but if the value is greater than the alpha we will replace the value of alpha to current value
	        if(current_value > beta):
	            return (actionToTake, current_value)
	        if(current_value > alpha):
	            alpha = current_value
    return (actionToTake, current_value)

def min_value(self, gameState, currentAgentIndex, currentDepth, alpha, beta):
	current_value = 100000
	actionToTake = None
    # the same idea with the max inly that we are looking for a score that is less.
	for availAction in gameState.getLegalActions(currentAgentIndex):
		successorState = gameState.generateSuccessor(currentAgentIndex, availAction)
        # this will reserve as recursion for the value function, and the setup will go so that the bottom of the tree will first be evaluated.
		next_action, next_score = self.value(successorState, currentAgentIndex+1, currentDepth) if not(alpha or beta) else self.value(successorState, currentAgentIndex+1, currentDepth, alpha, beta)
		if(next_score < current_value):
			current_value = next_score
			actionToTake = availAction
        # the difference with the max value is if the current value is less than the beta with change the value of beta to current value
		if(alpha and beta):
			if(current_value < alpha):
				return (actionToTake, current_value)
			if(current_value < beta):
				beta = current_value
	return (actionToTake, current_value)
