from actions import ClickAction
from pynput import keyboard, mouse
import logging
import pickle
import random
import pyautogui
from functools import partial
import time

def on_press(key):
	if key == keyboard.Key.esc:
		logging.critical("Escape pressed. Done setting up quick pray location.")
		# returning False exits the handler.
		return False

def on_click(x, y, button, pressed):
	'''
	listens only for right clicks.
	'''
	if button != mouse.Button.right or pressed is False:
		return

	location = x, y
	
def get_quick_pray_location():
	with keyboard.Listener(on_press=on_press_partial) as keyboard_listener:
		with mouse.Listener(on_click=on_click_partial) as mouse_listener:
			keyboard_listener.join()
