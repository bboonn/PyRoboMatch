import threading
import time
import random

class Robo(threading.Thread):
	def __init__(self, robo_id, init_pwr, sex, queue_, max_idle = 10):
		threading.Thread.__init__(self)
		self.q = queue_
		self.words = []
		self.id = robo_id
		self.power = init_pwr
		self.max_idle = max_idle
		self.step = 0
		self.mate = None
		self.sex = sex
		#self.say("Hello, world.")

	def __del__(self):
		self.say("Quit.")

	def run(self):
		while(None == self.mate):
			self.step += 1
			# send self info
			self.sendMsg(self.q, self)
			# Sleep random time
			idle_time = random.random() * self.max_idle
			time.sleep(idle_time)
			# get target
			trgt = self.getMsg(self.q)
			if not None == trgt:
				if (not (trgt is self)) and (not (trgt.sex == self.sex)):
					# adept each other
					self.adept(trgt)
					# check matchability
					if self.isMatch(trgt) and (None == trgt.mate):
						self.mate = trgt
						trgt.mate = self
						self.say("I like " + str(trgt.id) + trgt.sex + " @ " + str(trgt.power) + "!")

	def isMatch(self, target):
			return target.power == self.power

	def say(self, words):
		self.words.append(words)

	def adept(self, target):
		#self.say("Approching #" + str(target.id) + " from " + str(self.power) + " to " + str(target.power))
		if target.power > self.power:
			self.power += 1
		elif target.power < self.power:
			self.power -= 1
		elif target.power == self.power:
			pass
	def sendMsg(self, queue, msg):
		if not queue.full():
			queue.put(msg)

	def getMsg(self, queue):
		if not queue.empty():
			return queue.get()
		else:
			return None
