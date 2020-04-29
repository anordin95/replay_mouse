from pynput import keyboard, mouse
import time
import pickle
from actions import ActionList, MoveAction, ClickAction, KeyAction, ACTION_LIST_FILE
import pyautogui

RUNTIME = 120

def on_move(x, y):
	# print(f"move: {x}, {y}")
	# print(f"pyautogui: {pyautogui.position()}")
	action = MoveAction(x, y)
	action_list.add(action)

def on_click(x, y, button, pressed):
	if pressed:
		click_action = ClickAction(x, y)
		action_list.add(click_action)

		# print(f"clicked: {x}, {y}")

def on_press(key):
	if key == keyboard.Key.shift:
		print("press shift")
		action = KeyAction(key, is_press=True, is_release=False)
		action_list.add(action)

		# print("pressed shift!")

def on_release(key):
	if key == keyboard.Key.shift:
		action = KeyAction(key, is_press=False, is_release=True)
		action_list.add(action)

		# print("released shift")

def is_finished(start_time):
	return time.time() - start_time > RUNTIME

if __name__ == '__main__':
	mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
	keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

	mouse_listener.start()
	keyboard_listener.start()
	start_time = time.time()

	action_list = ActionList(start_time)
	while True:
		if is_finished(start_time):
			break
		print(f"Time remaining: {RUNTIME - (time.time() - start_time)}")
		time.sleep(0.5)

	print("Writing actions to pickle file.")

	with open(ACTION_LIST_FILE, "wb") as f:
		pickle.dump(action_list.actions, f)