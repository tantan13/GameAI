from constants import *
from utils import *
from core import *
import heapq
import pdb
import copy
from functools import reduce

from statesactions import *

############################
## HELPERS

### Return true if the given state object is a goal. Goal is a State object too.
def is_goal(state, goal):
  return len(goal.propositions.difference(state.propositions)) == 0

### Return true if the given state is in a set of states.
def state_in_set(state, set_of_states):
  for s in set_of_states:
    if s.propositions == state.propositions:
      return True
  return False

### For debugging, print each state in a list of states
def print_states(states):
  for s in states:
    ca = None
    if s.causing_action is not None:
      ca = s.causing_action.name
    print(s.id, s.propositions, ca, s.get_g(), s.get_h(), s.get_f())


############################
### Planner 
###
### The planner knows how to generate a plan using a-star and heuristic search planning.
### It also knows how to execute plans in a continuous, time environment.

class Planner():

  def __init__(self):
    self.running = False              # is the planner running?
    self.world = None                 # pointer back to the world
    self.the_plan = []                # the plan (when generated)
    self.initial_state = None         # Initial state (State object)
    self.goal_state = None            # Goal state (State object)
    self.actions = []                 # list of actions (Action objects)

  ### Start running
  def start(self):
    self.running = True
    
  ### Stop running
  def stop(self):
    self.running = False

  ### Called every tick. Executes the plan if there is one
  def update(self, delta = 0):
    result = False # default return value
    if self.running and len(self.the_plan) > 0:
      # I have a plan, so execute the first action in the plan
      self.the_plan[0].agent = self
      result = self.the_plan[0].execute(delta)
      if result == False:
        # action failed
        print("AGENT FAILED")
        self.the_plan = []
      elif result == True:
        # action succeeded
        done_action = self.the_plan.pop(0)
        print("ACTION", done_action.name, "SUCCEEDED")
        done_action.reset()
    # If the result is None, the action is still executing
    return result

  ### Call back from Action class. Pass through to world
  def check_preconditions(self, preconds):
    if self.world is not None:
      return self.world.check_preconditions(preconds)
    return False

  ### Call back from Action class. Pass through to world
  def get_x_y_for_label(self, label):
    if self.world is not None:
      return self.world.get_x_y_for_label(label)
    return None

  ### Call back from Action class. Pass through to world
  def trigger(self, action):
    if self.world is not None:
      return self.world.trigger(action)
    return False

  ### Generate a plan. Init and goal are State objects. Actions is a list of Action objects
  ### Return the plan and the closed list
  def astar(self, init, goal, actions):
      plan = []    # the final plan
      open = []    # the open list (priority queue) holding State objects
      closed = []  # the closed list (already visited states). Holds state objects
      ### YOUR CODE GOES HERE
      queue = []
      cameFrom = {}
      counter = 0
      g = {init: 0}
      h = self.compute_heuristic(init, goal, actions)
      if (is_goal(init,goal)):
        return plan, closed

      queue.append((h, counter, init))
      curr = init
      while len(queue) != 0 and (is_goal(curr, goal) == False):
        if curr not in closed:
          closed.append(curr)
        curr = heapq.heappop(queue)[2]
        neighbors = self.getNeighbors(curr, actions, closed)
        for neighbor in neighbors:
          if neighbor not in closed:
            tentativeScore = g[curr] + self.compute_heuristic(curr, neighbor, actions)
            if neighbor not in g or g[neighbor] > tentativeScore:
              counter = counter + 1
              cameFrom[neighbor] = curr
              g[neighbor] = tentativeScore
              h = self.compute_heuristic(neighbor, goal, actions) 
              f = h + g[neighbor]
              heapq.heappush(queue, (f, counter, neighbor))
      plan = self.reconstructPath(cameFrom, curr, init)
      ### CODE ABOVE
      return plan, closed

  def reconstructPath(self, cameFrom, curr, init):
    path = []
    path.append(curr.causing_action)
    while cameFrom.get(curr) != None and cameFrom.get(curr) != init:
      curr = cameFrom.get(curr)
      path = list(path)
      path.append(curr.causing_action)
    path.reverse()
    return path

  def getNeighbors(self, curr, actions, closed):
    # neighbors = [action[1] for action in actions if action[0].preconditions == curr.add_list] + \
    #              [action[0] for action in actions if action[1].preconditions == curr.add_list]
    neighbors = []
    for action in actions:
      if curr.propositions.issuperset(action.preconditions):
        #if all the preconditions of the action are in the set of current state propositions
        neighbor = copy.deepcopy(curr)
        if neighbor not in closed:
          neighbor.causing_action = action
        neighbor.propositions = (neighbor.propositions).union(action.add_list)
        neighbor.propositions = (neighbor.propositions).difference(action.delete_list)
        neighbors.append(neighbor)
    return neighbors
  #go look at the door thing gotta delete shit too and add list before adding to neighbors

  ### Compute the heuristic value of the current state using the HSP technique.
  ### Current_state and goal_state are State objects.
  def compute_heuristic(self, current_state, goal_state, actions):
    actions = copy.deepcopy(actions)  # Make a deep copy just in case
    h = 0                             # heuristic value to return
    ### YOUR CODE BELOW
    dummyStart = Action(name = "dummyStart", preconditions = {}, add_list = current_state.propositions, delete_list = {}, cost = 0)
    dummyGoal = Action(name = "dummyGoal", preconditions = goal_state.propositions, add_list = {}, delete_list = {})
    nodes = [] #Probably a list of Actions (including dummy Actions
    edges = [] #Probably an edge is a tuple (a1, prop, a2) where a1 and a2 could be pointers to Actions or Action.id
    actions.append(dummyStart)
    actions.append(dummyGoal)
    for action in actions:
      nodes.append(action)
    for i in nodes:
      for j in nodes:
        currEdges = (i.add_list).intersection(j.preconditions) #new set with elements common to action1's add list and action 2's preconds
        for edge in currEdges:
          #edge is precond name so edges is in the form (action1, precond, action2)
          edges.append((i, edge, j))
    #now i should have all the edges for my grpah i think
    #name, preconditions, add_list, delete_list, cost = 1
    q = []
    visited = []
    currentPropositions = set()
    from collections import defaultdict
    costs = defaultdict(list)
    costs = {}
    q.append(dummyStart) #append dummy node to the queue
    # visited.append(dummyStart) #mark as visited
    while len(q)!= 0:
      currAction = q.pop()
      currentPropositions = currentPropositions.union(currAction.add_list) #add dummy node's add list to the list of props
      if currAction in visited:
        break
      visited.append(currAction)
      if currAction == dummyGoal:
        return costs[currAction]
      for action in actions:
        if currentPropositions.issuperset(action.preconditions):
          if action not in visited:
            q.append(action)
      current_value = 0
      for edge in edges:
        if (edge[2] == currAction):
          #if this is incoming edge I want to track cost
          current_value = max(current_value, costs[edge[2]])
      costs[currAction] = current_value
      for edge in edges:
        if (edge[0] == currAction):
          #fixing the cost of all outgoing edges from the current action
          costs[edge[2]] = costs[edge[0]] + currAction.cost
    #last currAction must be goal..       
    h = costs[currAction]
    ### YOUR CODE ABOVE
    return h

