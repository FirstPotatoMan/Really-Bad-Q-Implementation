import numpy as np

class Q:
    def __init__(self, stateShape, actionShape, rewardShape, discountFactor, learningRate, vision):
        super().__init__()
        self.__stateShape = stateShape
        self.__actionShape = actionShape
        self.__rewardShape = rewardShape
        
        self.__discountFactor = 1-discountFactor

        self.__learningRate = 1-learningRate
        self.__vision = vision
        self.__q = np.array([np.array([self.__stateShape, self.__actionShape, self.__rewardShape])]) #First one is a key
    def updateQTableState(self, state, action):
        # self.__q = np.insert(self.__q, 0, ).reshape()
        pair = [np.array([state, action, self.__rewardShape])]
        if not self.__forceShape(pair):
            self.__q = np.concatenate((self.__q, pair))
            # print(self.__q)
    def getQTable(self):
        return self.__q
    def __forceShape(self, arr):
        for i in arr:
            if i.shape != self.__stateShape.shape:
                if i.shape != self.__actionShape.shape:
                    if i.shape != self.__rewardShape.shape:
                        print('u')
                        return True
        return False
    def giveRewards(self, reward):
        reward_ = np.array((reward,))
        if self.__forceShape(reward_): 
            return
        reward_ = reward_[0]
        table = self.__q[1:]
        num_of_timesteps = table.shape[0]
        currentTimeStep = 0
        R = (reward_-(self.discountFactor*reward_))/(1-(self.discountFactor**num_of_timesteps))
        for i in range(0, num_of_timesteps):
            discounted_reward = R * (self.discountFactor**i)
            table[i][2] = discounted_reward
    def getBestAction(self, state):
        index = 1
        maxi = 0
        bAI = self.__actionShape
        bestAction = self.__actionShape
        for i in self.__q[1:]:
            if np.array_equal(i[0], state):
                expected_reward = np.sum((self.__lookAhead(index), i[2]))
                if np.greater(expected_reward, maxi):
                    maxi = expected_reward
                    bestAction = i[1]
            index += 1
        return bestAction
    def __lookAhead(self, index):
        #returns a reward based on the next 1000 values
        #check if index + self.vision is a valid part of the q-table
        rangey = self.vision + index
        if self.__q[1:].shape[0] < rangey:
            rangey = self.__q[1:].shape[0]
        reward = self.__rewardShape
        count = 0
        for i in range(index, rangey):
            reward = np.sum([reward, self.__q[1:][i][2] * self.learningRate ** count], axis=0)
            count +=1
        # if it dosent exist, get the max rewards from the rest of the q-table, discounted
        #if it does exist, then we get the rewards for the next 1000 moves, discounted
        #return the reward
        return reward
    def saveCurrentQTable(self, path):
        np.save(path, self.__q)
    def loadQTableFromFile(self, path):
        self.__q = np.load(f'{path}.npy', allow_pickle=True)

# [[state akak image, action[0, 0, 0, 0, 1, ..., 0, 0, ]]]
# [
#     [
#           [0, 0, 0, 0, 0], 
#           [0, 0],
#           [0]
#     ],
    
#     [
#           [0, 0, 0, 0, 0], 
#           [0, 0],
#           [0]
#     ],
# ]
# [
#     [
#         [3, 3],
#         [3, 3]
#     ],
#     [
#         [3, 3],
#         [3, 3]
#     ],
#     [
#         [3, 3],
#         [3, 3]
#     ]
# ]