from pynput import keyboard, mouse
import time
import pickle
from primitives.actions import MoveAction, ClickAction, KeyAction
from primitives.action_list import ActionList
import pyautogui
import logging
from primitives.potion_tracker import setup_potions_tracker
from functools import partial

logger = logging.getLogger(__name__)

def on_move(x, y):
	'''
	deprecated. can't track all move locations. too expensive during replay.
	'''
	pass
	# action = MoveAction(x, y)
	# action_list.add(action)

def on_click(x, y, button, pressed, action_list):	
	if not pressed:
		# don't record mouse release events
		return

	if button == mouse.Button.left:
		button = 'left'
	else:
		button = 'right'

	logger.info(f"clicked: {x}, {y}, button: {button}")
	
	click_action = ClickAction(x, y, button)
	
	action_list.add(click_action)

def on_press(key, action_list):
	logger.info(f"key-press: {key}")

	if key == keyboard.Key.shift:
		action = KeyAction(key, is_press=True, is_release=False)
		action_list.add(action)

	elif key == keyboard.Key.esc:
		logger.critical("Escape pressed. Terminating listeners...")
		# returning False exits the handler.
		return False

def on_release(key, action_list):
	logger.info(f"key-release: {key}")

	if key == keyboard.Key.shift:
		action = KeyAction(key, is_press=False, is_release=True)
		action_list.add(action)

def record(use_potions, filename):
	if use_potions:
		setup_potions_tracker()

	start_time = time.time()
	action_list = ActionList(start_time)

	# setup callbacks with action_list arg passed.
	on_click_partial = partial(on_click, action_list=action_list)
	on_press_partial = partial(on_press, action_list=action_list)
	on_release_partial = partial(on_release, action_list=action_list)

	with keyboard.Listener(on_press=on_press_partial, on_release=on_release_partial) as keyboard_listener:
		with mouse.Listener(on_click=on_click_partial, on_move=on_move) as mouse_listener:
			
			keyboard_listener.join()
			# will reach here once esc has been pressed.
			
	logger.critical("\n\n\n DONE \n\n\n")
	logger.critical("Writing actions to pickle file.")

	with open(filename, "wb") as f:
		pickle.dump(action_list, f)



if __name__ == '__main__':
	record(use_potions=True)
	