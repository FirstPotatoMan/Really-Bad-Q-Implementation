//Another Q learning implementation. This time in JS

class Q{
    constructor(stateShape, actionShape, rewardShape){
      this.stateShape = stateShape
      this.actionShape = actionShape
      this.rewardShape = rewardShape
      this.Q = [[stateShape, actionShape, rewardShape]]/*This is a key to how all states/actions/rewards should be defined in the table now*/
    }
    updateQTable = (state, action, reward) => {
      if (this.checkShape(state, action, reward)){
        for (let pair of this.q) { 
          if (pair.includes(state) && pair[2] < reward) { //only update the q table with new values for a state if the old values have a lower reward
            this.q[this.q.getIndexOf(pair)] = [state, action, reward]
            return
          }
        }
        this.Q.push(state, action, reward)
        return Q
      }
    }
    getFromQTable = (state) => {
      for(let pair of this.q) {
        if (pair.includes(state))
          return pair[1]
       }
      return null
    }
    checkShape = (state, action, reward) => {
      if (state.length !== this.stateShape.length)
        return false
      if (action.length !== this.actionShape.length)
        return false
      if (reward.length !== this.rewardShape.length)
        return false
      return true
    }
  }
  
class Agent{
    constructor(q){
      //be warned, this is a really bad attempt to define shape. There are much better ways, but Im too lazy to implenet them
      this.stateShape = [null, null, null, null, null, null, null, null, null, null, null]
      this.actionShape = [null, null, null, null, null] //this is the number of actions the user can take, so in our example, the agent can take 5 actions
      this.rewardShape = [null]
      
      this.env = new Env() // this is your environment. It dosent have to be a class. For our purpose it is
      this.q = new Q(this.stateShape, this.actionShape, this.rewardShape)
      //define more controls here
    }
    explore = async() => {
      const state = env.getCurrentState()
      let action = this.state.actionState
      action[Math.floor(Math.random() * Math.floor(this.actionShape))] = 1
      const [action, reward] = await this.doAction(action)
      this.q.updateQTable(state, action, reward)
      return action
    }
    doAction = async(actionNumber) => {
      const reward = await this.env.doAction(actionNumber.indexOf(1) + 1) //for example, 1 might lead to going left, 2 might be right, etc. The enviornment then returns the reward for our actions
      return [actionNumber, reward]
    }
    bestMove = () => {
      const bestMove = Q.getFromQTable()
      if (!bestMove) {
        this.explore()
        return
      }
      const [action, reward] = this.doAction(bestMove)
      return action
    }
}