from primitives.potion_tracker import setup_potions_tracker
from primitives.get_quick_pray_location import get_quick_pray_location

PRAYER_POTS_FILENAME = 'prayer_pots.pkl'
RANGE_POTS_FILENAME = 'ranging_pots.pkl'
ABSORPTION_POTS_FILENAME = 'absorption_pots.pkl'
QUICK_PRAY_LOC_FILE = 'quick_pray_loc.pkl'

import logging
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
log_level = logging.INFO
logging.basicConfig(level=log_level, format=log_format)

# for use with prayer pots

# def setup():
# 	setup_potions_tracker(filename=RANGE_POTS_FILENAME, potion_type='range')
# 	setup_potions_tracker(filename=PRAYER_POTS_FILENAME, potion_type='prayer')

# for use with absorption pots

def setup():
	get_quick_pray_location(filename=QUICK_PRAY_LOC_FILE)
	setup_potions_tracker(filename=RANGE_POTS_FILENAME, potion_type='range')
	setup_potions_tracker(filename=ABSORPTION_POTS_FILENAME, potion_type='absorption')
	
	
if __name__ == '__main__':
	setup()