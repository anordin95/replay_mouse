import time

class ActionList:
	def __init__(self, start_time):
		self.start_time = start_time
		self.prev_action_time = 0.0

		self.actions = []

	def __len__(self):
		return len(self.actions)

	def iter(self):
		for action in self.actions:
			yield action

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