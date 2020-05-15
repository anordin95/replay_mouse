from primitives.actions import ClickAction
from pynput import keyboard, mouse
import logging
import pickle
import random
import pyautogui
from functools import partial
import time

logger = logging.getLogger(__name__)

class Potion(ClickAction):
	
	potion_px_width = 15
	potion_px_height = 30

	def __init__(self, location, doses = 4):
		self.x, self.y = location
		self.doses = doses

	def has_doses_left(self):
		return self.doses > 0

	def is_empty(self):
		return self.doses == 0

	def drink(self):
		logger.info("Drinking potion.")
		self.doses -= 1
		
		# ms
		duration_min, duration_max = 300, 600
		duration = random.randint(duration_min, duration_max) / 1000.0
			
		x_deviation = self.potion_px_width // 6
		x = self.x + random.randrange(-x_deviation, x_deviation)

		y_deviation = self.potion_px_height // 8
		y = self.y + random.randrange(-y_deviation, y_deviation)

		pyautogui.moveTo(x,
						y, 
						duration=duration, 
						tween=pyautogui.easeInOutQuad,
						)
		pyautogui.click()

		# provide in-game time to drink potion.
		time.sleep(2.0)

class PotionsTracker:
	def __init__(self, potion_type):
		self.potions = []
		self.potion_type = potion_type

	def add_potion_location(self, x, y):
		logger.info(f"Adding {self.potion_type} potion location: {x}, {y}")

		location = x, y
		potion = Potion(location)
		
		self.potions.append(potion)

	def sip_next_available_potion(self):
		logger.info(f"Attempting to sip next available {self.potion_type} potion.")
		
		for potion in self.potions:
			if potion.has_doses_left():
				potion.drink()
				return True

		logger.critical(f"No available {self.potion_type} potions.")
		return False


def on_press(key, potions_tracker):
	if key == keyboard.Key.esc:
		logger.critical("Escape pressed. Done setting up potions tracker.")
		# returning False exits the handler.
		return False

def on_click(x, y, button, pressed, potions_tracker):
	'''
	listens only for right clicks.
	'''
	if button != mouse.Button.right or pressed is False:
		return

	potions_tracker.add_potion_location(x, y)


def log_instructions(potion_type):
	logger.info("Instructions: \n")
	logger.info(f"Right-click each {potion_type.upper()} potion in your inventory.")
	logger.info("Only click potions with 4 doses!")
	logger.info("Press esc, once you are complete.")

def setup_potions_tracker(filename, potion_type: str):
	'''
	args:
		filename: file to save .pkl potion tracker to
		potion_type: name of potion to use.
	'''
	logger.info("Setting up potions tracker...")
	
	log_instructions(potion_type)
	potions_tracker = PotionsTracker(potion_type)

	on_click_partial = partial(on_click, potions_tracker=potions_tracker)
	on_press_partial = partial(on_press, potions_tracker=potions_tracker)
	
	with keyboard.Listener(on_press=on_press_partial) as keyboard_listener:
		with mouse.Listener(on_click=on_click_partial) as mouse_listener:
			keyboard_listener.join()

	with open(filename, "wb") as f:
		pickle.dump(potions_tracker, f)

	logger.info("Potion tracker is complete and saved.")
