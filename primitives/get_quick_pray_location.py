from primitives.actions import ClickAction
from pynput import keyboard, mouse
import logging
import pickle
import random
import pyautogui
from functools import partial
import time

quick_pray_location = None

logger = logging.getLogger(__name__)

def on_press(key):
	if key == keyboard.Key.esc:
		logger.critical("Escape pressed. Done setting up quick pray location.")
		# returning False exits the handler.
		return False

def on_click(x, y, button, pressed):
	'''
	listens only for right clicks.
	'''
	if button != mouse.Button.right or pressed is False:
		return

	quick_pray_location = x, y

def log_instructions():
	logger.info("Right click once on the quick-prayer location.")
	logger.info("Press esc, when complete.")
	
def get_quick_pray_location(filename):
	log_instructions()
	
	with keyboard.Listener(on_press=on_press) as keyboard_listener:
		with mouse.Listener(on_click=on_click) as mouse_listener:
			keyboard_listener.join()

	logger.info(f"Captured quick pray location: {quick_pray_location}")

	with open(filename, "wb") as f:
		pickle.dump(quick_pray_location, f)

	logger.info(f"Wrote quick pray location to file: {filename}")

if __name__ == '__main__':
	get_quick_pray_location()