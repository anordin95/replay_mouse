from pynput import keyboard, mouse
import time
from pathlib import Path
import pyautogui

ACTION_LIST_FILE = Path('action_list.pkl')

keyboard_controller = keyboard.Controller()

class ActionList:
	def __init__(self, start_time):
		self.start_time = start_time
		self.prev_action_time = 0.0

		self.actions = []
		
	def add(self, action):
		current_ts = time.time()
		normalized_ts = self.normalize_ts(ts=current_ts)

		time_since_prev_action = normalized_ts - self.prev_action_time
		self.prev_action_time = normalized_ts

		action.add_duration(time_since_prev_action)

		if normalized_ts in self.actions:
			raise Exception("Duplicate timestamp keys in actions.")

		self.actions.append(action)
	
	def normalize_ts(self, ts):
		return ts - self.start_time

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
		pyautogui.click()

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