import logging
import time
import pickle
import random

from primitives.potion_tracker import PotionsTracker
from primitives.click_location import ClickLocation
from primitives.replay import replay
from primitives.actions import ClickAction
from nmz_setup import (PRAYER_POTS_FILENAME, 
					RANGE_POTS_FILENAME, 
					ABSORPTION_POTS_FILENAME, 
					QUICK_PRAY_LOC_FILE,
					ROCK_CAKE_ACTION_LIST_FILE)

logging.basicConfig(level=logging.INFO)

# 1 point drained every 3 seconds with protect from melee
# 17 prayer bonus makes it once every 4.7 seconds
# ref: https://oldschool.tools/calculators/prayer-drain
PRAYER_DRAIN_PER_SECOND = 1.0 / 4.7
PRAYER_GAIN_PER_SIP = 18.0
PRAYER_LVL_SIP_AT = 0.0

# 1 range lvl drained every 60 seconds
RANGE_LVL_DRAIN_PER_SECOND = 1.0 / 60.0
# RANGE_LVL_DRAIN_PER_SECOND = 1.0 / 5.0
RANGE_LVL_GAIN_PER_SIP = 15.0
RANGE_LVL_SIP_AT = 6.0

# Drink 1 absorption pot every 193 seconds
# Based on observation of 1-monster hitting at a time.
SIP_ABSORTION_EVERY_X_SECONDS = 190.0
# SIP_ABSORTION_EVERY_X_SECONDS = 20.0

PRAYER_CLICK_PERIOD = 30.0

ROCK_CAKE_GUZZLE_PERIOD = 250.0

def load_pickle_file(filename):
	with open(filename, 'rb') as f:
		obj = pickle.load(f)

	return obj

def double_click_quick_pray(location: ClickLocation):
	click_spot_x, click_spot_y = location.get_perturbated_click_location()
	
	action = ClickAction(click_spot_x, click_spot_y, 'left')
	duration_min, duration_max = 300, 700
	duration = random.randint(duration_min, duration_max) / 1000.0
	action.duration = duration
	action.execute()

	# second click is faster
	action = ClickAction(click_spot_x, click_spot_y, 'left')
	duration_min, duration_max = 20, 50
	duration = random.randint(duration_min, duration_max) / 1000.0
	action.duration = duration
	action.execute()

def guzzle_rock_cake(rock_cake_action_list):
	
	replay(rock_cake_action_list)

def is_done(finished_absorptions_time):
	'''
	This at-best provides a rough estimate.

	I'd prefer it under-estimates finish time, to prevent
	random game clicking outside of nmz.

	'''
	if finished_absorptions_time is None:
		return False

	# I will begin nmz with 400 absorptions points taking roughly:
	beginning_absorption_time = SIP_ABSORTION_EVERY_X_SECONDS * 8

	# I subtract 10 minutes to be extra conservative.
	beginning_absorption_time -= 8 * 60

	# This provides the amount of time after the final absorption sip
	# that should be waited. Then, we expect to die shortly thereafter.
	stall_time = beginning_absorption_time

	if time.time() > finished_absorptions_time + stall_time:
		logging.info("Ending script! ")
		return True

	return False	

def main():
	# prayer_pot_sip_period = (PRAYER_GAIN_PER_SIP - PRAYER_LVL_SIP_AT) / PRAYER_DRAIN_PER_SECOND
	absorption_pot_sip_period = SIP_ABSORTION_EVERY_X_SECONDS
	range_pot_sip_period = (RANGE_LVL_GAIN_PER_SIP - RANGE_LVL_SIP_AT) / RANGE_LVL_DRAIN_PER_SECOND
	prayer_click_period = PRAYER_CLICK_PERIOD
	guzzle_period = ROCK_CAKE_GUZZLE_PERIOD

	logging.info(f"Sip an absorption pot every : {absorption_pot_sip_period} seconds.")
	logging.info(f"Sip a range pot every: {range_pot_sip_period} seconds.")
	logging.info(f"Double click quick pray every: {prayer_click_period} seconds.")
	logging.info(f"Guzzling rock cake every: {guzzle_period} seconds.")
	# prayer_potion_tracker = load_pickle_file(PRAYER_POTS_FILENAME)
	absorption_potion_tracker = load_pickle_file(ABSORPTION_POTS_FILENAME)
	range_potion_tracker = load_pickle_file(RANGE_POTS_FILENAME)
	quick_pray_location = load_pickle_file(QUICK_PRAY_LOC_FILE)
	rock_cake_action_list = load_pickle_file(ROCK_CAKE_ACTION_LIST_FILE)

	start_time = time.time()
	# next_prayer_sip_time = start_time + prayer_pot_sip_period
	next_absorption_sip_time = start_time + absorption_pot_sip_period
	# sip range pot immediately
	next_range_sip_time = start_time + 0.0
	next_quick_pray_time = start_time + prayer_click_period
	next_rock_cake_guzzle_time = start_time + guzzle_period

	while True:
		# random sleep_time will make sip times erratic, yet still according to correct rate.
		sleep_time = (10.0 * random.random()) + 1.0
		time.sleep(sleep_time)

		is_absorption_sip_success, is_pray_sip_success, is_range_sip_success = True, True, True

		# if time.time() > next_prayer_sip_time:
		# 	is_pray_sip_success = prayer_potion_tracker.sip_next_available_potion()
		# 	next_prayer_sip_time += prayer_pot_sip_period
		# 	logging.info(f"Next prayer sip time: {time.ctime(next_prayer_sip_time)}")
		
		if time.time() > next_quick_pray_time:
			double_click_quick_pray(quick_pray_location)
			next_quick_pray_time += prayer_click_period
			logging.info(f"Next pray click time: {time.ctime(next_quick_pray_time)}")
		
		if time.time() > next_range_sip_time: 
			is_range_sip_success = range_potion_tracker.sip_next_available_potion()
			next_range_sip_time += range_pot_sip_period
			logging.info(f"Next range sip time: {time.ctime(next_range_sip_time)}")

		if time.time() > next_rock_cake_guzzle_time:
			guzzle_rock_cake(rock_cake_action_list)
			next_rock_cake_guzzle_time += guzzle_period
			logging.info(f"Next rock-cake guzzle time: {time.ctime(next_rock_cake_guzzle_time)}")

		finished_absorptions_time = None
		if time.time() > next_absorption_sip_time:
			is_absorption_sip_success = absorption_potion_tracker.sip_next_available_potion()
			if is_absorption_sip_success:
				next_absorption_sip_time += absorption_pot_sip_period
				logging.info(f"Next absorption sip time: {time.ctime(next_absorption_sip_time)}")			
			else:
				finished_absorptions_time = time.time()
				next_absorption_sip_time = float('inf')
				logging.critical("Out of absorption potions to sip.")
		
		if is_done(finished_absorptions_time):
			break



if __name__ == '__main__':
	main()
