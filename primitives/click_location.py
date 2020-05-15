import pyautogui
import time
from getkey import getkey
import random
import logging

logger = logging.getLogger(__name__)

class ClickLocation:

	def __init__(self, x, y, margin_for_error_px = 2):

		self.x = x
		self.y = y
		self.margin_for_error_px = margin_for_error_px

	def get_original_location(self):
		return self.original_location

	def get_perturbated_click_location(self):
		lower_bound_x = int(self.x - self.margin_for_error_px)
		upper_bound_x = int(self.x + self.margin_for_error_px)
		new_x = random.randint(lower_bound_x, upper_bound_x)

		lower_bound_y = int(self.y - self.margin_for_error_px)
		upper_bound_y = int(self.y + self.margin_for_error_px)
		new_y = random.randint(lower_bound_y, upper_bound_y)

		logger.info(f"Original location: {self.x, self.y}. Clicking location: {new_x, new_y}")

		return new_x, new_y

