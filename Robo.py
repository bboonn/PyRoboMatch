import threading
import time
import random

class Robo(threading.Thread):
	def __init__(self, robo_id, init_pwr, sex, queue_, robo_list, max_idle, dad = None, mom = None, gene = 0):
		threading.Thread.__init__(self)
		self.q = queue_
		self.id = robo_id
		self.power = init_pwr
		self.sex = sex
		self.max_idle = max_idle
		self.dad = dad
		self.mom = mom
		self.prep = 0
		self.step = 0
		self.mate = None
		self.child = None
		self.gene = gene
		self.l = robo_list
		self.l.append(self)
		self.setDaemon(True)
		self.start()
	def __del__(self):
		pass

	def run(self):
		while True:
			if (not self.mate):
				self.step += 1
				# send self info
				self.sendMsg(self.q, self)
				# Sleep random time
				self.goSleep(self.max_idle)
				# get target
				trgt = self.getMsg(self.q)
				# deal with msg
				self.readMsg(trgt)
			elif (not self.child):
				self.prep += 1
				self.goSleep(self.max_idle)
			elif self.power > 0:
				self.power -= 1
				self.goSleep(self.max_idle)
			if 0 == self.power:
				break

	def isMatch(self, target):
		if not target.mate:
			return target.power == self.power
		else:
			return False

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

	def bornChild(self):
		if (not self.child) and ("♀" == self.sex) and (self.mate != None):
			# generation digit / dad last name digit / mom last name digit
			child_gene = self.gene + 1
			child_id = (child_gene)*100 + (self.mate.id%10)*10 + (self.id % 10)
			child_power = int(self.power * (random.choice([0.5, 1, 1.2])))
			child_sex = random.choice(["♂","♀"])
			child = Robo(child_id, child_power, child_sex, self.q, self.l, self.max_idle, self.mate, self, child_gene)
			self.child = child
			self.mate.child = child
			return child
		else:
			return None

	def readMsg(self, target):
		if target:
			if (not (target is self)):
				if (target.sex != self.sex):
					# follow the trends
					self.adept(target)
					# check matchability
					if self.isMatch(target):
						self.mate = target
						target.mate = self

	def goSleep(self, multiplexer):
		idle_time = random.random() * multiplexer
		time.sleep(idle_time)
