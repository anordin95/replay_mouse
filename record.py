from pynput import keyboard, mouse
import time
import pickle
from actions import ActionList, MoveAction, ClickAction, KeyAction, ACTION_LIST_FILE
import pyautogui

DEBUG=True

def on_move(x, y):
	pass
	
	# if DEBUG:
	# 	print(f"move: {x}, {y}")
	
	# action = MoveAction(x, y)
	# action_list.add(action)

def on_click(x, y, button, pressed):
	if DEBUG:
		print(f"clicked: {x}, {y}")

	if pressed:
		click_action = ClickAction(x, y)
		action_list.add(click_action)

def on_press(key):
	if DEBUG:
		print(f"key-press: {key}")

	if key == keyboard.Key.shift:
		action = KeyAction(key, is_press=True, is_release=False)
		action_list.add(action)

def on_release(key):
	if DEBUG:
		print(f"key-release: {key}")

	if key == keyboard.Key.shift:
		action = KeyAction(key, is_press=False, is_release=True)
		action_list.add(action)
	
	elif key == keyboard.Key.esc:
		print("Escape pressed. Terminating listeners...")
		# returning False exits the handler.
		return False
		# print("released shift")

if __name__ == '__main__':
	# mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
	# keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)     
	
	# mouse_listener.start()
	# keyboard_listener.start()

	start_time = time.time()
	action_list = ActionList(start_time)

	with keyboard.Listener(on_press=on_press, on_release=on_release) as keyboard_listener:
		with mouse.Listener(on_click=on_click, on_move=on_move) as mouse_listener:
			
			keyboard_listener.join()
			# will reach here once esc has been pressed.
			
	print("\n \n \n DONE \n \n \n")

	print("Writing actions to pickle file.")

	with open(ACTION_LIST_FILE, "wb") as f:
		pickle.dump(action_list.actions, f)