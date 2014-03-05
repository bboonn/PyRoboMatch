import random
import time
import queue
import Robo
import KyanToolKit_Py

ktk = KyanToolKit_Py.KyanToolKit_Py()
ROBO_MAX = 6
POWER_MAX = 72
IDLE_MAX = 1
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
		if None == r.mate :
			conn = str(r.id) + r.sex
		else:
			conn = str(r.id) + r.sex + "+" + str(r.mate.id) + r.mate.sex
		print("== " + "Robot "+ conn + " " + power_bar + " (" + str(r.power) + ")")
		# step
		step_bar = ""
		for i in range(r.step):
			step_bar += "-"
		# words
		print("==+" + step_bar + ">" + " (" + str(r.step) + ")")
		for s in r.words:
			print("|> " +  s)
		print("==+" + step_bar + ">", end="")
		# match
		if None != r.mate:
			print("Matched!!\n")
		else:
			print("\n")
for robo_id in range(ROBO_MAX):
	power_init = int(random.random() * POWER_MAX)
	#sex = random.choice(["♂", "♀"])
	if 1 == (robo_id%2):
		sex = "♂"
	else:
		sex = "♀"
	r = Robo.Robo(robo_id, power_init, sex, env_q, IDLE_MAX)
	robo_list.append(r)
	robo_words.append("")
	r.setDaemon(True)
	r.start()
while True:
	ktk.clearScreen()
	PrintScreen()
	time.sleep(0.1)
	if env_q.empty():
		break

input("Press to continue ...\n")
