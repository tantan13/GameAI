  ### Compute the heuristic value of the current state using the HSP technique.
  ### Current_state and goal_state are State objects.
  def compute_heuristic(self, current_state, goal_state, actions):
    actions = copy.deepcopy(actions)  # Make a deep copy just in case
    h = 0                             # heuristic value to return
    ### YOUR CODE BELOW
    nodes = [] #Probably a list of Actions (including dummy Actions
    edges = [] #Probably an edge is a tuple (a1, prop, a2) where a1 and a2 could be pointers to Actions or Action.id
    for action in actions:
      nodes.append(action)
    for i in nodes:
      for j in nodes:
        currEdges = (i.add_list).intersection(j.preconditions) #new set with elements common to action1's add list and action 2's preconds
        for edge in currEdges:
          #edge is precond name so edges is in the form (action1, precond, action2)
          edges.append((i, edge, j))
    #now i should have all the edges for my grpah i think
    q = []
    currentPropositions = []
    from collections import defaultdict
    costs = defaultdict(list)
    costs = {current_state: [0]}
    q.append(current_state) #append dummy node to the queue
    # visited.append(current_state) #mark as visited
    while len(q)!= 0:
      currAction = q.pop()
      currentPropositions.append(currAction.add_list) #add dummy node's add list to the list of props
      for action in actions:
        if all(elem in currentPropositions for elem in action.preconditions):
          q.append(action)
        for edge in edges:
          if (edge[2] == currAction):
            #if this is incooming edge I want to track cost
            costs[currAction].append(currAction.cost)
          if (edge[0] == currAction):
            # if its an outgoing edge i wanna propogate cost to cost + curr_action's cost
            costs[currAction] = max(cost[currAction]) + currAction.cost
        if action == goal_state:
          h = costs[action]
          return h
          break
    h = costs[goal_state]




# heuristic_world
# while open
# curr = pop from q
# add curr to closed list
# add curr's add list to heuristic_world
# for each action
#     for each edge
#         if it is an incoming edge, track cost
#     have cost here
#     for each edge
#         if it is outgoing edge, propagate edge
#     if dummy goal
#         return stuff
    ### YOUR CODE ABOVE
    return h
