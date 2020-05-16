def move_mouse_randomly(duration):
	'''
	randomly move mouse for a period less than duration.

	args:
		duration: time to run

	returns:
		time_elapsed: actual time
	'''
	logger.info("Beginning move_mouse_randomly.")
	
	start = time.time()
	num_moves = min(int(duration), 10)
	
	logger.info(f"Moving mouse {num_moves} times.")

	# purposely yet roughly chosen 
	# as few hundred pixels away from border
	x_min, x_max = 420, 1614
	y_min, y_max = 318, 874

	# min and max wait in milliseconds.
	wait_min, wait_max = 300, 700
	
	has_clicked = False
	
	for move in range(num_moves):
		
		# right-click sometimes but at least once.
		if random.random() > 0.85 or not has_clicked:
			logger.info("Random right click button.")
			pyautogui.click(button='right')
			has_clicked = True

		x = random.randint(x_min, x_max)
		y = random.randint(y_min, y_max)
		
		duration = random.randint(wait_min, wait_max) / 1000.0

		pyautogui.moveTo(x,
						y, 
						duration=duration, 
						tween=pyautogui.easeInOutQuad,
		)

	time_elapsed = time.time() - start

	return time_elapsed