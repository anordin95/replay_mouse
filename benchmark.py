import pyautogui
import time
import random

DURATION = 0.05
x = random.randint(0, 1919)
y = random.randint(0, 1079)
def pyautogui_do():	
	pyautogui.moveTo(x,
		y,
		duration=0.01,
		# tween=pyautogui.easeInOutQuad,
	)
	# pyautogui.click(button='right')

from pynput.mouse import Button, Controller
mouse = Controller()

def pynput_do():
	x = random.randint(0, 1919)
	y = random.randint(0, 1079)
	mouse.position = x, y
	pass

start = time.time()

for i in range(100):
	# pyautogui_do()
	pynput_do()

end = time.time()
time_elapsed = end - start
print(f"Time elapsed: {time_elapsed}")




