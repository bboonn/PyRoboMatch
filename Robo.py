import threading
import time
import random

class Robo(threading.Thread):
	def __init__(self, robo_id, init_pwr, queue_, max_idle = 10):
		threading.Thread.__init__(self)
		self.q = queue_
		self.words = []
		self.id = robo_id
		self.power = init_pwr
		self.max_idle = max_idle
		self.matched = False
		self.step = 0
		#self.say("Hello, world.")

	def __del__(self):
		self.say("Quit.")

	def run(self):
		while(not self.matched):
			self.step += 1
			# send self info
			if not self.q.full():
				self.q.put(self)
			# Sleep random time
			idle_time = int(random.random() * self.max_idle)
			time.sleep(idle_time)
			# get target info
			if not self.q.empty():
				trgt = self.q.get()
				# adept each other
				if not trgt is self:
					self.adept(trgt)
					# check matchability
					if self.isMatch(trgt):
						self.say("I like #" + str(trgt.id) + " @ " + str(trgt.power) + "!")
						self.matched = True
						trgt.matched = True

	def isMatch(self, target):
			return target.power == self.power

	def say(self, words):
		self.words.append(words)

	def adept(self, target):
		#self.say("Approching #" + str(target.id) + " from " + str(self.power) + " to " + str(target.power))
		if target.power > self.power:
			self.power += 1
		elif target.power < self.power:
			target.power += 1
		elif target.power == self.power:
			pass

