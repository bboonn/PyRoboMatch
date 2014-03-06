import random
import time
import queue
import Robo
import KyanToolKit_Py

ktk = KyanToolKit_Py.KyanToolKit_Py()
ROBO_MAX = 8
POWER_MAX = 72
IDLE_MAX = 0.8
PREG_TIME = 10
def checkChild():
	for r in Robo.Robo.robo_list:
		if (r.mate):
			if (not r.child):
				if (r.age - r.grow) >= PREG_TIME:
					r.bornChild()
		if 0 == r.power:
			Robo.Robo.robo_list.remove(r)

def PrintScreen():
	for r in Robo.Robo.robo_list:
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
		# grow & age
		grow_bar = ""
		age_bar = ""
		for i in range(r.grow):
			grow_bar += "-"
		for i in range(r.age - r.grow):
			age_bar += "="
		print("==+" + grow_bar + ">", end="")
		# match
		if r.mate:
			print("Matched!!" + age_bar + ">", end = "")
		if r.child:
			print("Born!!", end = "")
		print("\n")

for robo_id in range(ROBO_MAX):
	power_init = int(random.random() * POWER_MAX)
	sex = random.choice(["♂","♀"])
	r = Robo.Robo(robo_id, power_init, sex, IDLE_MAX)

while True:
	# input("[step debug mode]")
	ktk.clearScreen()
	checkChild()
	PrintScreen()
	time.sleep(0.2)
	if Robo.Robo.msg_queue.empty():
		break

input("All Matched!! ...\n")
