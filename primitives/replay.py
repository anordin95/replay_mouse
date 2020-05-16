import pickle
from primitives.actions import MoveAction, ClickAction, KeyAction
from primitives.action_list import ActionList
import logging
import time

logger = logging.getLogger(__name__)

def replay(action_list):
	replay_time_seconds = action_list.get_total_time()
	len_action_list = len(action_list)
	
	logger.info(f"Beginning action_list replay. Will take {replay_time_seconds} seconds.")

	for idx, action in enumerate(action_list.iter()):
		# import ipdb; ipdb.set_trace()
		print(f"Executing action #{idx+1} of {len_action_list}. action: {action}. duration: {action.duration}")
		action.execute()

	# provide some time for the final action to actually execute
	time.sleep(3.0)

if __name__ == '__main__':
	pass

