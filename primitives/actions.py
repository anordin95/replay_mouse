from pynput import keyboard, mouse
import time
from pathlib import Path
import pyautogui
import random
import logging

keyboard_controller = keyboard.Controller()
logger = logging.getLogger(__name__)

class Action:
	def add_duration(self, duration):
		self.duration = duration
	
	def pre_execute(self):
		if self.duration is None:
			raise Exception("Action must have duration.")

class MoveAction(Action):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def execute(self):
		self.pre_execute()

		pyautogui.moveTo(self.x,
			self.y, 
			duration=self.duration / 2, 
			tween=pyautogui.easeInOutQuad,
			)

	def __repr__(self):
		return "move"

class ClickAction(Action):

	def __init__(self, x, y, button):
		'''
		args:
			x: int
			y: int
			button: (str) 'left' or 'right'
		'''
		self.x = x
		self.y = y
		
		if button not in ['left', 'right']:
			raise Exception(f"button must be left or right, not: {button}")
		self.button = button

	def execute(self):
		self.pre_execute()

		duration = self.duration
		
		if duration > 2.0:
			duration_min, duration_max = 500, 1200
			new_duration = random.randint(duration_min, duration_max) / 1000.0
			sleep_time =  duration - new_duration
			duration = new_duration

			time.sleep(sleep_time)

		pyautogui.moveTo(self.x,
			self.y, 
			duration=duration, 
			tween=pyautogui.easeInOutQuad,
			)

		pyautogui.click(button=self.button)

	def __repr__(self):
		return "click"


class KeyAction(Action):
	def __init__(self, key, is_press, is_release):
		self.key = key
		self.is_press = is_press
		self.is_release = is_release

	def execute(self):
		self.pre_execute()

		if self.is_press:
			keyboard_controller.press(self.key)
		else:
			keyboard_controller.release(self.key)

	def __repr__(self):
		if self.is_press:
			return f"press {self.key}"
		if self.is_release:
			return f"release {self.key}"