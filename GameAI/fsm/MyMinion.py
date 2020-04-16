'''
 * Copyright (c) 2014, 2015 Entertainment Intelligence Lab, Georgia Institute of Technology.
 * Originally developed by Mark Riedl.
 * Last edited by Mark Riedl 05/2015
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import sys, pygame, math, numpy, random, time, copy
from pygame.locals import * 

from constants import *
from utils import *
from core import *
from moba import *

class MyMinion(Minion):
	
	def __init__(self, position, orientation, world, image = NPC, speed = SPEED, viewangle = 360, hitpoints = HITPOINTS, firerate = FIRERATE, bulletclass = SmallBullet):
		Minion.__init__(self, position, orientation, world, image, speed, viewangle, hitpoints, firerate, bulletclass)
		self.states = [Idle]
		### Add your states to self.states (but don't remove Idle)
		### YOUR CODE GOES BELOW HERE ###
		self.states += [MoveAgent, ShootTower, ShootBase]


		### YOUR CODE GOES ABOVE HERE ###

	def start(self):
		Minion.start(self)
		self.changeState(Idle)





############################
### Idle
###
### This is the default state of MyMinion. The main purpose of the Idle state is to figure out what state to change to and do that immediately.

class Idle(State):
	
	def enter(self, oldstate):
		State.enter(self, oldstate)
		# stop moving
		self.agent.stopMoving()
	
	def execute(self, delta = 0):
		State.execute(self, delta)
		### YOUR CODE GOES BELOW HERE ###
		target = None
		minDist = float("inf")
		enemyTowers = self.agent.world.getEnemyTowers(self.agent.getTeam())
		enemyBases = self.agent.world.getEnemyBases(self.agent.getTeam())

		if enemyTowers != None and len(enemyTowers) > 0:
			for tower in enemyTowers:
				currDist = distance(self.agent.getLocation(), tower.getLocation())
				if (currDist < minDist):
					target = tower
					minDist = currDist
		if target != None:
			self.agent.changeState(MoveAgent, target)
		if enemyTowers == None or len(enemyTowers) == 0:
			if enemyBases != None and len(enemyBases) > 0:
				for base in enemyBases:
					currDist = distance(self.agent.getLocation(), base.getLocation())
					if (currDist < minDist):
						target = base
						minDist = currDist
			if target != None:
				self.agent.changeState(MoveAgent, target)
		if target != None:
			self.agent.changeState(MoveAgent, target)

		### YOUR CODE GOES ABOVE HERE ###
		return None

##############################
### Taunt
###
### This is a state given as an example of how to pass arbitrary parameters into a State.
### To taunt someome, Agent.changeState(Taunt, enemyagent)

class Taunt(State):

	def parseArgs(self, args):
		self.victim = args[0]

	def execute(self, delta = 0):
		if self.victim is not None:
			print("Hey " + str(self.victim) + ", I love my hubs!")
		self.agent.changeState(Idle)

##############################
### YOUR STATES GO HERE:
class MoveAgent(State):
	def parseArgs(self, args):
		self.target = args[0]

	def enter(self, oldstate):
		self.agent.navigateTo(self.target.getLocation())
		#self.agent.turnToFace(self.target.getLocation())

	def execute(self, delta = 0):
		enemyTowers = self.agent.world.getEnemyTowers(self.agent.getTeam())
		enemyBases = self.agent.world.getEnemyBases(self.agent.getTeam())
		if not self.agent.isMoving() or self.target is not None:
			#self.agent.turnToFace(self.target.getLocation())
			self.agent.navigateTo(self.target.getLocation())
		# currDist = distance(self.agent.getLocation(), self.target.getLocation())
		# if currDist <= BULLETRANGE:
		# 	self.agent.changeState(ShootTower, self.target)
		# 	self.agent.changeState(ShootBase, self.target)
		for tower in enemyTowers:
			currDist = distance(self.agent.getLocation(), tower.getLocation())
			if tower in self.agent.getVisible() and currDist <= BULLETRANGE:
				self.agent.changeState(ShootTower, tower)
		for base in enemyBases:
			currDist = distance(self.agent.getLocation(), base.getLocation())
			if base in self.agent.getVisible() and currDist <= BULLETRANGE:
				self.agent.changeState(ShootBase, base)

class ShootTower(State):

	def parseArgs(self, args):
		self.target = args[0]

	def enter(self, oldstate):
		self.agent.stopMoving()
		self.agent.navigator.path = None
		self.agent.navigator.destination = None

	# def exit(self, oldstate):
	# 	self.agent.stopMoving()
	# 	self.agent.navigator.path = None
	# 	self.agent.navigator.destination = None

	def execute(self, delta = 0):
		currDist = distance(self.agent.getLocation(), self.target.getLocation())
		if self.target not in self.agent.getVisible() and currDist <= BULLETRANGE:
			self.agent.changeState(Idle)
		else:
			self.agent.turnToFace(self.target.getLocation())
			self.agent.shoot()

        ### YOUR CODE GOES ABOVE HERE ###

class ShootBase(State):

	def parseArgs(self, args):
		self.target = args[0]

	def enter(self, oldstate):
		self.agent.stopMoving()
		self.agent.navigator.path = None
		self.agent.navigator.destination = None

	# def exit(self, oldstate):
	# 	self.agent.stopMoving()
	# 	self.agent.navigator.path = None4
	# 	self.agent.navigator.destination = None

	def execute(self, delta = 0):
		currDist = distance(self.agent.getLocation(), self.target.getLocation())
		if self.target not in self.agent.getVisible() and currDist <= BULLETRANGE:
			self.agent.changeState(Idle)
		else:
			self.agent.turnToFace(self.target.getLocation())
			self.agent.shoot()

        ### YOUR CODE GOES ABOVE HERE ###

