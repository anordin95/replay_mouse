from pynput import keyboard, mouse
import time
from pathlib import Path
import pyautogui
import random
import logging

ACTION_LIST_FILE = Path('action_list.pkl')

keyboard_controller = keyboard.Controller()

logger = logging.getLogger(__name__)

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

	def get_total_time(self):
		# subtracting by 0 does nothing,
		# but it does help understanding the point of the code.
		# 0.0 is the start of time for this object.
		start_time = 0.0
		total_time = self.prev_action_time - start_time
		return total_time

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
	'''
	randomly move mouse for a period less than duration.

	args:
		duration: time to run

	returns:
		time_elapsed: actual time
	'''
	logger.info("Beginning move_mouse_randomly.")
	
	start = time.time()
	num_moves = min(int(duration), 10)
	
	logger.info(f"Moving mouse {num_moves} times.")

	# purposely yet roughly chosen 
	# as few hundred pixels away from border
	x_min, x_max = 420, 1614
	y_min, y_max = 318, 874

	# min and max wait in milliseconds.
	wait_min, wait_max = 300, 700
	
	has_clicked = False
	
	for move in range(num_moves):
		
		# right-click sometimes but at least once.
		if random.random() > 0.85 or not has_clicked:
			logger.info("Random right click button.")
			pyautogui.click(button='right')
			has_clicked = True

		x = random.randint(x_min, x_max)
		y = random.randint(y_min, y_max)
		
		duration = random.randint(wait_min, wait_max) / 1000.0

		pyautogui.moveTo(x,
						y, 
						duration=duration, 
						tween=pyautogui.easeInOutQuad,
		)

	time_elapsed = time.time() - start

	return time_elapsed

class ClickAction(Action):

	LONG_CLICK_THRESHOLD = 15

	# 4 minutes
	VERY_LONG_THRESHOLD = 240

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def wait_on_long_durations(self, wait_time):
		logger.info(f"Waiting on very long duration click. wait_time: {wait_time}")

		time_elapsed = move_mouse_randomly(wait_time)
		remaining_sleep_time = wait_time - time_elapsed
		
		logger.info(f"Sleeping for {remaining_sleep_time} seconds.")
		time.sleep(remaining_sleep_time)

	def wait_on_very_long_durations(self, wait_time):
		time_remaining = wait_time

		logger.info(f"Waiting on very long duration click. wait_time: {wait_time}")

		sleep_time = 180
		time_buffer = 30
		logout_time = 300
		
		assert sleep_time + time_buffer < 300

		while time_remaining > sleep_time + time_buffer:

			logger.info(f"Sleeping: {sleep_time}.")
			time.sleep(sleep_time)
			time_remaining -= sleep_time

			time_elapsed = move_mouse_randomly(time_remaining)
			time_remaining -= time_elapsed

		logger.info(f"Sleeping: {time_remaining}.")
		time.sleep(time_remaining)

	def execute(self):
		self.pre_execute()

		duration = self.duration

		click_time = duration
		
		if duration > self.VERY_LONG_THRESHOLD:
			# click min and max in milliseconds.
			wait_min, wait_max = 300, 700
			click_time = random.randint(wait_min, wait_max) / 1000.0
			
			stall_time = duration - click_time

			self.wait_on_very_long_durations(stall_time)

		elif duration > self.LONG_CLICK_THRESHOLD:
			
			# click min and max in milliseconds.
			wait_min, wait_max = 300, 700
			click_time = random.randint(wait_min, wait_max) / 1000.0
			
			stall_time = duration - click_time

			self.wait_on_long_durations(stall_time)

		pyautogui.moveTo(self.x,
			self.y, 
			duration=click_time, 
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