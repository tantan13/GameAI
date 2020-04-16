#Checking every node for shorter path
def shortcutPath(source, dest, path, world, agent):
	path = copy.deepcopy(path)
	### YOUR CODE GOES BELOW HERE ###
	newPath = []
	badPoints = world.getPoints()
	badLines = world.getLines()

	for node in path:
		if clearShot(source, node, badLines, badPoints, agent):
			continue
		else:
			source = path[path.index(node) - 1]
			newPath.append(source)
	if clearShot(source, dest, badLines, badPoints, agent) == False:
		#then i cant skip last node
		newPath.append(path[-1])
	path = newPath
	# newPath = []
	# badPoints = world.getPoints()
	# badLines = world.getLines()

	# for node in path:
	# 	if clearShot(source, node, badLines, badPoints, agent):
	# 		continue
	# 	else:
	# 		source = path[path.index(node) - 1]
	# 		newPath.append(source)
	# if clearShot(source, dest, badLines, badPoints, agent) == False:
	# 	#then i cant skip last node
	# 	newPath.append(path[-1])
	# path = newPath
	### YOUR CODE GOES BELOW HERE ###
	return path

#Only checking if the first and last nodes are removable
def shortcutPath2(source, dest, path, world, agent):
	path = copy.deepcopy(path)
	### YOUR CODE GOES BELOW HERE ###
	newPath = []
	badPoints = world.getPoints()
	badLines = world.getLines()

	if clearShot(source, path[1], badLines, badPoints, agent):
		path = path.remove(path[0]) #if there's a clear shot from source to the second element then i dont need the first node?
	if clearShot(path[-2], dest, badLines, badPoints, agent):
		path = path.remove(path[-1]) #if there's a clear shnot from the second last to dest then I don't need the last node?
	### YOUR CODE GOES BELOW HERE ###
	return path