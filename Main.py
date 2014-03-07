import random
import time
import queue
import Robo
import csv
import KyanToolKit_Py

start_time = time.time()
ktk = KyanToolKit_Py.KyanToolKit_Py()
ROBO_INIT = 6
POWER_MAX = 72
IDLE_MAX = 0.5
PREG_TIME = 10
CSV_FORM = [("time", "Power", "Alive Robo", "Total Robo")]
def csvGenerate(enable):
	if CSV_FORM and enable:
		file_name = "Robo_Yard_" + str(round(time.time())) + ".csv"
		csv_file = open(file_name,'w',newline="")
		writer = csv.writer(csv_file)
		writer.writerows(CSV_FORM)
		csv_file.close()

def childbearingPolicy():
	CHILD_RESTRICT = 2
	for r in Robo.Robo.robo_list:
		if "alive" == r.state:
			r.bornChild(CHILD_RESTRICT)
			if r.dad:
				if 1 == r.dad.childNum() or 1 == r.mom.childNum():
					r.bornChild(CHILD_RESTRICT)

def printYard(limit = "UNLIMIT"):
	counter=0
	for r in Robo.Robo.robo_list:
		if counter == limit:
			break

		if "alive" == r.state:
			counter+=1
			# power
			power_bar = ""
			for i in range(r.power):
				power_bar = "".join((power_bar,"*"))
			conn = "".join((str(r.id),r.sex))
			if r.mate:
				conn += "".join(("+",str(r.mate.id),r.mate.sex))
			if r.dad and r.mom:
				conn += "".join((" by (",str(r.dad.id),"+",str(r.mom.id),")"))
			print("".join(("== ",conn," ",power_bar," (",str(r.power),")")))
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
				print("Matched" + age_bar + ">", end = "")
			if r.child:
				print("Born*" + str(r.childNum()), end = "")
			print("\n")
def printStatistics():
	word_list = []
	def printAll():
		nonlocal word_list
		frame = ""
		longest_1st = 0
		longest_2nd = 0
		for w in word_list:
			if longest_1st < len(w[0]):
				longest_1st = len(w[0])
			if longest_2nd < len(w[1]):
				longest_2nd = len(w[1])
		for i in range(longest_1st + longest_2nd + 7):
			frame = "".join((frame,"="))
		print(frame)
		for w in word_list:
			for i in range(longest_1st-len(w[0])):
				w = ("".join((" ",w[0])),w[1])
			for i in range(longest_2nd-len(w[1])):
				w = (w[0], "".join((w[1]," ")))
			print("".join(("| ",w[0]," : ",w[1]," |")))
		print(frame)
	def printInfo(first, second):
		nonlocal word_list
		word_list.append((first,second))
	def printWithSex(title, li):
		printInfo(title, "".join((str(sum(li))," (",str(li[0]),":",str(li[1]),")")))
	def getRoboInfo():
		total = [0,0]
		alive = [0,0]
		power_off = [0,0]
		old_enough = [0,0]
		matched = [0,0]
		single = [0,0]
		avg_matched = 0
		current_power = [0,0]
		global peak_power
		lastest_gene = 0
		for r in Robo.Robo.robo_list:
			if "♂" == r.sex:
				sex = 0
			else:
				sex = 1
			total[sex] += 1
			if "alive" == r.state:
				alive[sex] += 1
				current_power[sex] += r.power
			elif "power_off" == r.state:
				power_off[sex] += 1
			elif "old_enough" == r.state:
				old_enough[sex] += 1
			if r.mate:
				avg_matched += r.grow
				matched[sex] += 1
			if lastest_gene < r.gene:
				lastest_gene = r.gene
			if peak_power < sum(current_power):
				peak_power = sum(current_power)
		printWithSex("Total Robo",total)
		printInfo("Init #",str(ROBO_INIT))
		printWithSex("Alive #",alive)
		printWithSex("Power off #",power_off)
		printWithSex("Old enough #",old_enough)
		printWithSex("Current Power",current_power)
		printInfo("","")
		if sum(matched):
			printInfo("Average Matched",toStr(avg_matched/sum(matched)) + " steps")
			printInfo("Matched Rate", toStr(sum(matched)/sum(total)*100) + " %")
		if sum(alive):
			printInfo("Power per Alive", toStr(sum(current_power)/sum(alive)))
		printInfo("Civilization Point",toStr(peak_power/sum(total)))
		printInfo("Peak Power",str(peak_power))
		printInfo("Generation", str(lastest_gene) +" G")
		if 0 == sum(alive):
			return False
		CSV_FORM.append((round(time.time()-start_time,2),sum(current_power),sum(alive),sum(total)))
		return True
	continued = getRoboInfo()
	printInfo("","")
	printInfo("Queue Size",str(Robo.Robo.msg_queue.qsize()))
	printAll()
	if not continued:
		byeBye("-- The Silent of the Yard --")
def byeBye(words = ""):
	csvGenerate(True)
	ktk.pressToContinue("\n" + words + "\nPopulation exsits: " + toStr(time.time()-start_time) + "s\n")
	ktk.byeBye()
def toStr(num):
	return str(round(num,2))

for robo_id in range(ROBO_INIT):
	power_init = int(random.random() * POWER_MAX)
	sex = random.choice(["♂","♀"])
	r = Robo.Robo(robo_id, power_init, sex, IDLE_MAX)

peak_power = 0
while True:
	ktk.clearScreen()
	childbearingPolicy()
	printYard(10)
	printStatistics()
	time.sleep(0.2)
	if Robo.Robo.msg_queue.empty():
		break
byeBye("-- Happy Robo Life! --")
