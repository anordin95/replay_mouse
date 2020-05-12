from pynput import keyboard, mouse
import time
from pathlib import Path
import pyautogui
import random

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

def move_mouse_randomly(duration):
	# print(f"move_mouse_randomly..")
	start = time.time()
	num_moves = int(duration) // 2
	
	for move in range(num_moves):
		x = random.randint(420, 1614)
		y = random.randint(318, 874)
		# 0.3 - 0.7s
		duration = float(random.randint(300, 700)) / 1000.0

		pyautogui.moveTo(x,
						y, 
						duration=duration, 
						tween=pyautogui.easeInOutQuad,
		)

	return time.time() - start



class ClickAction(Action):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def execute(self):
		self.pre_execute()
		duration = self.duration
		if duration > 1.0:

			if duration > 5.0:
				random_move_time = duration / 2
				actual_random_move_time = move_mouse_randomly(random_move_time)
				duration = duration - actual_random_move_time

			# print("tweaking duration")

			sleep_fraction = float(random.randint(500, 600)) / 1000.0
			# sleep_fraction += 0.75
			sleep_time = sleep_fraction * duration
			new_duration = (1.0 - sleep_fraction) * duration
			
			# add delay to sleep time
			# sleep_time += 0.2
			duration = new_duration

			# print(f"original duration: {self.duration}")
			# print(f"sleep time: {sleep_time}")
			# print(f"new duration: {duration}")

			time.sleep(sleep_time)

		else:
			duration += 0.2


		pyautogui.moveTo(self.x,
			self.y, 
			duration=duration, 
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