import threading
import time
import random

ROBO_MAX = 5
POWER_MAX = 100
for robo_id in range(ROBO_MAX):
	power_init = int(random.random() * 100)
	Robo(robo_id, power_init).
