import pickle
from actions import ActionList, MoveAction, ClickAction, KeyAction, ACTION_LIST_FILE
import logging
import time
from potion_tracker import POTIONS_TRACKER_FILE, PotionsTracker

logging.basicConfig(level=logging.DEBUG)

def replay(action_list):
	len_action_list = len(action_list)
	for idx, action in enumerate(action_list):
		print(f"Executing action #{idx+1} of {len_action_list}. action: {action}. duration: {action.duration}")
		action.execute()

def get_action_list():
	with open(ACTION_LIST_FILE, 'rb') as f:
		action_list = pickle.load(f)

	return action_list

def get_potion_tracker():
	with open(POTIONS_TRACKER_FILE, 'rb') as f:
		potion_tracker = pickle.load(f)

	return potion_tracker

if __name__ == '__main__':
	action_list = get_action_list()
	potion_tracker = get_potion_tracker()

	NUM_REPLAYS = 12

	# replay_time_seconds = action_list.get_total_time()
	# total_time_minutes = (replay_time * NUM_REPLAYS) / 60.0
	
	logging.info(f"Beginning {NUM_REPLAYS} replays...")
	# logging.info(f"Each replay takes {replay_time} seconds.")
	# logging.info(f"Total runtime will be: {total_time_minutes} minutes.")

	for replay_num in range(1, NUM_REPLAYS+1):
		
		potion_tracker.sip_next_available_potion()

		logging.info(f"BEGINNING REPLAY ITERATION:{replay_num}...")
		replay(action_list)

		# provide 5-second buffer for final action to actually finish
		time.sleep(5.0)


