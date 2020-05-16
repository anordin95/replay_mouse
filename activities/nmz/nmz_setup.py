from primitives.potion_tracker import setup_potions_tracker
from primitives.get_quick_pray_location import get_quick_pray_location
from primitives.record import record

PRAYER_POTS_FILENAME = 'prayer_pots.pkl'
RANGE_POTS_FILENAME = 'ranging_pots.pkl'
ABSORPTION_POTS_FILENAME = 'absorption_pots.pkl'
QUICK_PRAY_LOC_FILE = 'quick_pray_loc.pkl'
ROCK_CAKE_ACTION_LIST_FILE = 'rock_cake_action_list.pkl'

import logging
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
log_level = logging.INFO
logging.basicConfig(level=log_level, format=log_format)

# for use with prayer pots

# def setup():
# 	setup_potions_tracker(filename=RANGE_POTS_FILENAME, potion_type='range')
# 	setup_potions_tracker(filename=PRAYER_POTS_FILENAME, potion_type='prayer')

# for use with absorption pots

logger = logging.getLogger('__name__')

def setup():
	logger.info("Record guzzling a rock cake. When done, press esc.")
	record(use_potions=False, filename=ROCK_CAKE_ACTION_LIST_FILE)
	get_quick_pray_location(filename=QUICK_PRAY_LOC_FILE)
	setup_potions_tracker(filename=RANGE_POTS_FILENAME, potion_type='range')
	setup_potions_tracker(filename=ABSORPTION_POTS_FILENAME, potion_type='absorption')
	

	
if __name__ == '__main__':
	setup()