import numpy as np
from numpy import random
from Q import Q

class Agent:
    def __init__(self, screen, actions, rewards, discountFactor, learningRate, vision, explorationRate, *functions):
        super().__init__()
        self.q = Q(screen, actions, rewards, discountFactor, learningRate, vision)
        self.explorationRate = explorationRate
        self.epoch = 0
        self.tablePath = 'table'
        for i in functions:
            self.__setattr__(i.__name__, i)
        self.actionShape = actions
    def loadQTable(self):
        self.q.loadQTableFromFile(self.tablePath)
    def saveQTable(self):
        self.q.saveCurrentQTable(self.tablePath)
    def explore(self, state):
        randAction = self.actionShape
        randAction[random.randInt(1, 735)] = 1.
        self.move(randAction)
        self.q.updateQTableState(state, randAction)
    def bestKnownMove(self, state):
        bestAction = self.q.getBestAction(state)
        self.move(randAction)
        self.q.updateQTableState(state, bestAction)
    def eplisonLearn(self, state):
        if 0.5 > (random.normal(0, 1, 1) * ((1-self.explorationRate) ** self.q.getQTable().shape[0])):
            self.bestKnownMove(state)
            return
        self.explore(state)
