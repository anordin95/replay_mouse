from primitives.potion_tracker import setup_potions_tracker

PRAYER_POTS_FILENAME = 'prayer_pots.pkl'
RANGE_POTS_FILENAME = 'ranging_pots.pkl'
ABSORPTION_POTS_FILENAME = 'absorption_pots.pkl'

# def setup():
# 	setup_potions_tracker(filename=RANGE_POTS_FILENAME, potion_type='range')
# 	setup_potions_tracker(filename=PRAYER_POTS_FILENAME, potion_type='prayer')

def setup():
	setup_potions_tracker(filename=RANGE_POTS_FILENAME, potion_type='range')
	setup_potions_tracker(filename=ABSORPTION_POTS_FILENAME, potion_type='absorption')

if __name__ == '__main__':
	setup()