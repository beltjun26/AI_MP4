def value(self, gameState, currentAgentIndex, currentDepth, type, alpha, beta):

    if(currentAgentIndex == gameState.getNumAgents()):
        currentAgentIndex = 0
        currentDepth += 1
    if(currentDepth == self.depth):
        return (None, self.evaluationFunction(gameState))
    if(gameState.isWin() or gameState.isLose()):
        return (None, self.evaluationFunction(gameState))
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
    		val = self.exp_value(gameState, currentAgentIndex, currentDepth)
    return val

def exp_value(self, gameState, currentAgentIndex, currentDepth):
    v = 0
    actionToTake = None
    legalActions = gameState.getLegalActions(currentAgentIndex)
    prob = 1.0/len(legalActions)

    for availAction in legalActions:
        successorState = gameState.generateSuccessor(currentAgentIndex, availAction)
        next_action, next_v = self.value(successorState, currentAgentIndex+1, currentDepth)
        v = v + (next_v * prob)

    return (None, v)

def max_value(self, gameState, currentAgentIndex, currentDepth, alpha, beta):
    current_value = -100000
    actionToTake = None
    legalActions = gameState.getLegalActions(currentAgentIndex);
    for availAction in legalActions:
        successorState = gameState.generateSuccessor(currentAgentIndex, availAction)
        next_action, next_score = self.value(successorState, currentAgentIndex+1, currentDepth) if not(alpha or beta) else self.value(successorState, currentAgentIndex+1, currentDepth, alpha, beta)
        if(next_score > current_value):
            current_value = next_score
            actionToTake = availAction
        if(alpha and beta):
	        if(current_value > beta):
	            return (actionToTake, current_value)
	        if(current_value > alpha):
	            alpha = current_value
    return (actionToTake, current_value)

def min_value(self, gameState, currentAgentIndex, currentDepth, alpha, beta):
	current_value = 100000
	actionToTake = None
	for availAction in gameState.getLegalActions(currentAgentIndex):
		successorState = gameState.generateSuccessor(currentAgentIndex, availAction)
		next_action, next_score = self.value(successorState, currentAgentIndex+1, currentDepth) if not(alpha or beta) else self.value(successorState, currentAgentIndex+1, currentDepth, alpha, beta)
		if(next_score < current_value):
			current_value = next_score
			actionToTake = availAction
		if(alpha and beta):
			if(current_value < alpha):
				return (actionToTake, current_value)
			if(current_value < beta):
				beta = current_value
	return (actionToTake, current_value)
