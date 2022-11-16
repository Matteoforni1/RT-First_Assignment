from __future__ import print_function

import time
from sr.robot import *

a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

avoid_d_th = 0.85
avoid_a_th = 20.0""" float: Threshold for the release of a previously grabbed silver token """
""" floats: Thresholds for detecting blocks the robot must avoid """

release_d_th = 0.55
""" float: Threshold for the release of a previously grabbed silver token """

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
	"""
	Function for setting a linear velocity
    
	Args: speed (int): the speed of the wheels
	seconds (int): the time interval
	"""
	R.motors[0].m0.power = speed
	R.motors[0].m1.power = speed
	time.sleep(seconds)
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0

def turn(speed, seconds):
	"""
	Function for setting an angular velocity
    
	Args: speed (int): the speed of the wheels
	seconds (int): the time interval
	"""
	R.motors[0].m0.power = speed
	R.motors[0].m1.power = -speed
	time.sleep(seconds)
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0

def find_token(mark, holding, silver, gold):
	"""
	Function to find the closest token
	
	Parameters:
	mark (string): the type of token the robot should looking for ('silver' or 'gold')
	holding (int): a flag which allows to know if the robot is currently holding a token or not (the held token id if there's one, -1 otherwise)

	Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
	token_info (int): the id of the closest token (-1 if no token is detected)
	"""
	dist=100
	id = 0
	"""
	If the value of mark is silver, we look for a silver token
	"""
	if mark == 'silver':
		for token in R.see():
			
			"""
			If we see a golden token, while looking for a silver one, we control if we need to avoid it
			"""
			if token.info.marker_type is MARKER_TOKEN_GOLD:		# if the token is too close (and it's not the held one), we want to avoid it!
				
				if (token.dist < avoid_d_th) & (-avoid_a_th < token.rot_y < avoid_a_th):	
					
					if token.rot_y <= 0:	# we check in which direction the block should be avoided
						sign = 1
					else:
						sign = -1
					avoid(sign)
			"""
			If we see a silver token, we check if we've already coupled it with a golden one.
			We control in the silver vector, where we stored all the id of the silver token that we've already coupled
			"""
			if token.info.marker_type is MARKER_TOKEN_SILVER:
				if not token.info.code in silver:
					"""
					If the token isn't coupled yet, we check if it's the nearest one, among the visible tokens.
					If it's closer than dist (which is the nearest token, among the visible tokens we've already checked), we save its info.
					"""
					if token.dist < dist:
						token_info = token.info.code
						dist=token.dist
						rot_y=token.rot_y
				else:
					"""
					If the token is already coupled, we may want to avoid it, if it's too close
					"""
					if token.dist < avoid_d_th:
						if -avoid_a_th < token.rot_y < avoid_a_th:
							
							if token.rot_y <= 0:	# we check in which direction the block should be avoided
								sign = 1
							else:
								sign = -1
							avoid(sign)
	"""
	If the value of mark is gold, we look for a golden token
	"""			
	if mark == 'gold':
		for token in R.see():
			"""
			If we see a silver token, while looking for a golden one, we control if we need to avoid it
			"""
			if token.info.marker_type is MARKER_TOKEN_SILVER:
				if token.info.code != holding:			# if the token is too close (and it's not the held one), we want to avoid it!
					
					if (token.dist < avoid_d_th) & (-avoid_a_th < token.rot_y < avoid_a_th):		
						
						if token.rot_y <= 0:		# we check in which direction the block should be avoided
							sign = 1
						else:
							sign = -1
						avoid(sign)
			"""
			If we see a gold token, we check if we've already coupled it with a silver one.
			We control in the gold vector, where we stored all the id of the golden token that we've already coupled
			"""
			if token.info.marker_type is MARKER_TOKEN_GOLD:
				"""
				If the token isn't coupled yet, we check if it's the nearest one, among the visible tokens.
				If it's closer than dist (which is the nearest token, among the visible tokens we've already checked), we save its info.
				"""
				if not token.info.code in gold:
					if token.dist < dist:
						token_info = token.info.code
						dist=token.dist
						rot_y=token.rot_y
				
				else:			# If the token is already coupled, we may want to avoid it, if it's too close
					
					if (token.dist < avoid_d_th) & (-avoid_a_th < token.rot_y < avoid_a_th):
						
						if token.rot_y <= 0:	# we check in which direction the block should be avoided
							sign = 1
						else:
							sign = -1
						avoid(sign)
	if dist==100:		# If dist is still 100, no token has been seen, therefore we return -1 values, to communicate to the main that no token is in sight.
		return -1, -1, -1
	else:			# If a coupleable token has been found, we return info about that token
		return dist, rot_y, token_info


"""
Function designated to avoid a token

Parameters:
sign (int): a +1/-1 value, which tells in which direction the robot should turn
"""
def avoid(sign):
	turn(15*sign,0.5)
	drive(50,0.8)
	turn(-20*sign,0.5)


def main():
	silver_id_vector = []
	gold_id_vector = []
	holding_id = -1	# We initialize some variables and vectors
	mark = 'silver'	# We also set the value of mark to silver
	while (1):
		dist, rot_y, token_id = find_token(mark, holding_id, silver_id_vector, gold_id_vector)  # we look for tokens
		if dist==-1:	# We don't see any token, so we turn, to look in another direction
			print("I don't see any token!!")
			turn(-10,1)
		elif dist <d_th: # We're close to an uncoupled token
			if mark == 'silver':
				print("Found it!")
				R.grab() # if we are close to the token, we grab it.
				print("Gotcha!") 
				mark = 'gold'	# We change the value of mark, so we can look for the golden token
				holding_id = token_id
				silver_id_vector.append(token_id)	# We save the token id into the silver vector
				
		elif (dist <release_d_th) & (mark == 'gold') & (holding_id != -1):	# We found a golden token, while we were looking for one!
			print('Found the other one!')
			R.release() # if we are close to a golden token, we release the silver token next to it.
			print('Done it!')
			mark = 'silver'
			gold_id_vector.append(token_id)	# We save the token id into the gold vector
			holding_id = -1
			drive(-60,3)	# We drive away for the coupled blocks
			
		elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
			print("Ah, here we are!.")
			drive(45, 0.5)
			
		elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
			print("Left a bit...")
			turn(-2, 0.5)
			
		elif rot_y > a_th:
			print("Right a bit...")
			turn(+2, 0.5)
			
		if (len(gold_id_vector) == 6) & (len(silver_id_vector) == 6):	# We coupled all the gold tokens with silver ones, so we can terminate the execution!
			print('We did it!')
			return
main()
