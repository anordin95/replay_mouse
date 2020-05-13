from pynput import keyboard, mouse
import time
import pickle
from actions import ActionList, MoveAction, ClickAction, KeyAction, ACTION_LIST_FILE
import pyautogui
import logging
from potion_tracker import setup_potions_tracker
from functools import partial

logging.basicConfig(level=logging.DEBUG)

def on_move(x, y):
	'''
	deprecated. can't track all move locations. too expensive during replay.
	'''
	pass
	# action = MoveAction(x, y)
	# action_list.add(action)

def on_click(x, y, button, pressed, action_list):	
	if not pressed or button != mouse.Button.left:
		return

	logging.info(f"clicked: {x}, {y}")

	click_action = ClickAction(x, y)
	action_list.add(click_action)

def on_press(key, action_list):
	logging.info(f"key-press: {key}")

	if key == keyboard.Key.shift:
		action = KeyAction(key, is_press=True, is_release=False)
		action_list.add(action)

	elif key == keyboard.Key.esc:
		logging.critical("Escape pressed. Terminating listeners...")
		# returning False exits the handler.
		return False

def on_release(key, action_list):
	logging.info(f"key-release: {key}")

	if key == keyboard.Key.shift:
		action = KeyAction(key, is_press=False, is_release=True)
		action_list.add(action)

def main(use_potions):
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
			
	logging.critical("\n\n\n DONE \n\n\n")
	logging.critical("Writing actions to pickle file.")

	with open(ACTION_LIST_FILE, "wb") as f:
		pickle.dump(action_list.actions, f)



if __name__ == '__main__':
	main(use_potions=True)
	