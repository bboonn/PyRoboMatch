import random
import time
import queue
import Robo
import csv
import KyanToolKit_Py
import ROboYard

start_time = time.time()
ktk = KyanToolKit_Py.KyanToolKit_Py()
CSV_FORM = [("time", "Power", "Alive Robo", "Total Robo")]
def csvGenerate(enable):
	if CSV_FORM and enable:
		file_name = "Robo_Yard_" + str(round(time.time())) + ".csv"
		csv_file = open(file_name,'w',newline="")
		writer = csv.writer(csv_file)
		writer.writerows(CSV_FORM)
		csv_file.close()

def byeBye():
	csvGenerate(True)
	self.ktk.byeBye()

yards = []
yard = RoboYard.RoboYard(16, 72, 0.5, "test")
yards.append(yard)
while True:
	time.sleep(200)
