import logging
import time
import pickle
import random

from potion_tracker import PotionsTracker
from nmz_setup import PRAYER_POTS_FILENAME, RANGE_POTS_FILENAME

logging.basicConfig(level=logging.DEBUG)

# 1 point drained every 3 seconds with protect from melee
# 17 prayer bonus makes it once every 4.7 seconds
# ref: https://oldschool.tools/calculators/prayer-drain
PRAYER_DRAIN_PER_SECOND = 1.0 / 4.7
PRAYER_GAIN_PER_SIP = 18.0
PRAYER_LVL_SIP_AT = 0.0

# 1 range lvl drained every 60 seconds
RANGE_LVL_DRAIN_PER_SECOND = 1.0 / 60.0
RANGE_LVL_GAIN_PER_SIP = 15.0
RANGE_LVL_SIP_AT = 6.0

def get_potion_tracker(filename):
	with open(filename, 'rb') as f:
		potion_tracker = pickle.load(f)

	return potion_tracker

def replay():
	prayer_pot_sip_period = (PRAYER_GAIN_PER_SIP - PRAYER_LVL_SIP_AT) / PRAYER_DRAIN_PER_SECOND
	range_pot_sip_period = (RANGE_LVL_GAIN_PER_SIP - RANGE_LVL_SIP_AT) / RANGE_LVL_DRAIN_PER_SECOND

	logging.info(f"Sip a prayer pot every : {prayer_pot_sip_period} seconds.")
	logging.info(f"Sip a range pot every: {range_pot_sip_period} seconds.")

	prayer_potion_tracker = get_potion_tracker(PRAYER_POTS_FILENAME)
	range_potion_tracker = get_potion_tracker(RANGE_POTS_FILENAME)

	start_time = time.time()
	next_prayer_sip_time = start_time + prayer_pot_sip_period
	next_range_sip_time = start_time + range_pot_sip_period

	while True:
		# random sleep_time will make sip times erratic, yet still according to correct rate.
		sleep_time = (5.0 * random.random()) + 1.0
		time.sleep(sleep_time)			

		
		is_pray_sip_success, is_range_sip_success = True, True

		if time.time() > next_prayer_sip_time:
			is_pray_sip_success = prayer_potion_tracker.sip_next_available_potion()
			next_prayer_sip_time += prayer_pot_sip_period
			logging.info(f"Next prayer sip time: {time.ctime(next_prayer_sip_time)}")

		if time.time() > next_range_sip_time: 
			is_range_sip_success = range_potion_tracker.sip_next_available_potion()
			next_range_sip_time += range_pot_sip_period
			logging.info(f"Next range sip time: {time.ctime(next_range_sip_time)}")

		if is_range_sip_success == False or is_pray_sip_success == False:
			logging.info("Out of potions. Finishing...")
			break


if __name__ == '__main__':
	replay()
