import pyautogui
import time
import random
from pynput.mouse import Button, Controller

'''
RESULTS:
pynput is over 400 times faster!

pyautogui_avg_time: 0.11693036079406738
pynput_avg_time: 0.00028290748596191404

'''

def pyautogui_do(x, y):	
	pyautogui.moveTo(x,
		y,
		duration=0.00,
	)

mouse = Controller()

def pynput_do(x, y):
	mouse.position = x, y
	pass

def benchmark_run(fn, num_runs):
	# generate locations before timer begins	
	x_locations = [random.randint(0, 1919) for i in range(num_runs)]
	y_locations = [random.randint(0, 1079) for i in range(num_runs)]
	
	start = time.time()
	
	for i in range(num_runs):
		x = x_locations[i]
		y = y_locations[i]
		fn(x, y)
	
	end = time.time()
	time_elapsed = end - start
	return time_elapsed

NUM_RUNS = 100
pyautogui_avg_time = benchmark_run(pyautogui_do, NUM_RUNS) / NUM_RUNS
pynput_avg_time = benchmark_run(pynput_do, NUM_RUNS) / NUM_RUNS

print(f"pyautogui_avg_time: {pyautogui_avg_time}")
print(f"pynput_avg_time: {pynput_avg_time}")

