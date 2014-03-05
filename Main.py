import random
import time
import queue
import Robo
import KyanToolKit_Py

ktk = KyanToolKit_Py.KyanToolKit_Py()
ROBO_MAX = 9
POWER_MAX = 72
IDLE_MAX = 0.5
PREG_TIME = 10
env_q = queue.Queue()
robo_list = []
def checkChild():
	for r in robo_list:
		if (r.mate):
			if (not r.child):
				if r.prep >= PREG_TIME:
					r.bornChild()
		if 0 == r.power:
			robo_list.remove(r)

def PrintScreen():
	for r in robo_list:
		# power
		power_bar = ""
		for i in range(r.power):
			power_bar += "*"
		conn = str(r.id) + r.sex
		if r.mate:
			conn += "+" + str(r.mate.id) + r.mate.sex
		if r.dad and r.mom:
			conn += " by (" + str(r.dad.id) + "+" + str(r.mom.id) + ")"
		print("== " + conn + " "  + power_bar + " (" + str(r.power) + ")")
		# step & prep
		step_bar = ""
		prep_bar = ""
		for i in range(r.step):
			step_bar += "-"
		for i in range(r.prep):
			prep_bar += "="
		print("==+" + step_bar + ">", end="")
		# match
		if r.mate:
			print("Matched!!" + prep_bar + ">", end = "")
		if r.child:
			print("Born!!")
		print("\n")

for robo_id in range(ROBO_MAX):
	power_init = int(random.random() * POWER_MAX)
	sex = random.choice(["♂","♀"])
	r = Robo.Robo(robo_id, power_init, sex, env_q, robo_list, IDLE_MAX)

while True:
	# input("[step debug mode]")
	ktk.clearScreen()
	checkChild()
	PrintScreen()
	time.sleep(0.2)
	if env_q.empty():
		break

input("All Matched!! ...\n")
