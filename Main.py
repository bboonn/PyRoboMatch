import random
import time
import queue
import Robo
import KyanToolKit_Py

ktk = KyanToolKit_Py.KyanToolKit_Py()
ROBO_MAX = 6
POWER_MAX = 20
IDLE_MAX = 5
env_q = queue.Queue()
robo_list = []
robo_words = []
def PrintScreen():
	for i in range(ROBO_MAX):
		r = robo_list[i]
		# power
		power_bar = ""
		for i in range(r.power):
			power_bar += "*"
		print("== Robot " + str(r.id) + " " + power_bar + " (" + str(r.power) + ")")
		# step
		step_bar = ""
		for i in range(r.step):
			step_bar += "-"
		# words
		print("+" + step_bar + ">" + " (" + str(r.step) + ")")
		for s in r.words:
			print("|> " +  s)
		print("+" + step_bar + ">", end="")
		# match
		if True == r.matched:
			print("Matched!!\n")
		else:
			print("\n")
for robo_id in range(ROBO_MAX):
	power_init = int(random.random() * POWER_MAX)
	r = Robo.Robo(robo_id, power_init, env_q, IDLE_MAX)
	robo_list.append(r)
	robo_words.append("")
	r.setDaemon(True)
	r.start()
while not env_q.empty():
	ktk.clearScreen()
	PrintScreen()
	time.sleep(0.5)

input("Press to continue ...\n")
