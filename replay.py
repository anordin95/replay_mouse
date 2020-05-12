import pickle
from actions import ActionList, MoveAction, ClickAction, KeyAction, ACTION_LIST_FILE

def replay(action_list):
	len_action_list = len(action_list)
	for idx, action in enumerate(action_list):
		print(f"Executing action #{idx+1} of {len_action_list}. action: {action}. duration: {action.duration}")
		action.execute()

def get_action_list():
	with open(ACTION_LIST_FILE, 'rb') as f:
		action_list = pickle.load(f)

	return action_list

def shorten_action_list(action_list):

	'''
	The goal is to increase the speed with which the action_list
	may be replayed.

	Currently, the listener is so acute, that it takes much longer
	to replay a series of mouse events than it takes to record them.

	This method will selectively remove MoveAction's only from the
	action_list in hopes of speeding up the script.
	'''
	
	# keep every nth move action
	frequency = 6

	counter = 0
	short_action_list = []

	for action in action_list:
		if not isinstance(action, MoveAction):
			short_action_list.append(action)
			continue

		if counter % frequency == 0:
			short_action_list.append(action)

		counter += 1

	return short_action_list



if __name__ == '__main__':
	action_list = get_action_list()
	# print(f"Original length: {len(action_list)}")
	
	# short_action_list = shorten_action_list(action_list)
	# print(f"New length: {len(short_action_list)}")
	
	# 40 minutes
	for i in range(30):
		
		print(f"BEGINNING REPLAY ITERATION:{i+1}...")

		replay(action_list)


