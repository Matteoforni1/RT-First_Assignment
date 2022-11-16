# First Assignment - Research Track 1
## Summary:

This document contains the information required for the first assignment, which include:

- How the code works
- Pseudocode
- How to run the code
- Possible improvements

## How the code works:

The code is divided into five different functions (main included):

- The turn function is used to turn the robot left or right (depending on the input parameter)
- The drive function is used to drive the robot forward or backward (depending on the input parameter)
- The find token function is used to find one of the nearest token around and to prepare the robot trajectory, in order to go for it
- the avoid function is used to avoid undesired tokens (for example: we want to avoid other silver tokens, while we're already holding one, in order to avoid to drag other blocks away with the robot)
- The main function uses the previous four functions to make the code work. The details will be discussed in the next lines...


The robot starting position is in the upper-left corner.
The robot starts looking for near silver tokens; when it finds one, the drive, turn and avoid functions are used to guide the robot to it. When the token is reached, the robot grabs it and starts looking for gold tokens; when it finds one, it does the same procedure as described before to reach it. Then, it drops the silver token next to the found gold token.
The id of the silver and gold tokens are saved in two vectors. Then, we restart looking for silver token, not considering tokens whose ids are present in the two vectors, because they're already coupled!
This entire procedure is repeated over and over, until all tokens are coupled (we look if the dimension of the gold and silver vector coincides with the total number of tokens, which is six in this case).
Then the execution terminates.

## Pseudocode:

In this section, there is the full pseudocode of my program:

import libraries

FUNCTION drive(speed,seconds)
	
	set both motors' power to speed
	sleep for seconds
	reset both motors' power to 0
	
END FUNCTION

	
FUNCTION turn(speed,seconds)

	set thw two motors' power to +speed and -speed respectively 
	sleep for seconds
	reset both motors' power to 0
	
END FUNCTION 


FUNCTION find_token(mark,holding,silver,gold)
	
	initialize dist to 100
	initialize id to 0
	
	IF mark is 'silver'
		
		FOR every visible token
			
			IF the visible token is gold
			
				IF dist is less than avoid_d_th AND rot_y is between +/- avoid_a_th
				
					IF the angle is negative (or 0)
					
						set sign to +1 (clockwise rotation)
						
					ELSE 
					
						set sign to -1 (counterclockwise rotation)
						
					END IF
						
					call the avoid function, passing sign as a parameter
					
				END IF
				
			END IF
			
			IF the visible token is silver
			
				IF the token's code is not present in the silver vector
				
					IF the distance from the token is less than dist
					
						set token_info to token.info.code
						set dist to token.dist
						set rot_y to token.rot_y
						
					END IF
					
				ELSE
					
					IF dist is less than avoid_d_th AND rot_y is between +/- avoid_a_th
				
						IF the angle is negative (or 0)
					
							set sign to +1 (clockwise rotation)
						
						ELSE 
					
							set sign to -1 (counterclockwise rotation)
						
						END IF
						
						call the avoid function, passing sign as a parameter
					
					END IF
				END IF
				
			END IF
			
		END FOR
		
	END IF
	
	IF mark is 'gold'
		
		FOR every visible token
			
			IF the visible token is silver
			
				IF the silver token is not the one we are holding
			
					IF dist is less than avoid_d_th AND rot_y is between +/- avoid_a_th
				
						IF the angle is negative (or 0)
					
							set sign to +1 (clockwise rotation)
						
						ELSE 
					
							set sign to -1 (counterclockwise rotation)
						
						END IF
						
						call the avoid function, passing sign as a parameter
					
					END IF
					
				END IF
				
			END IF
			
			IF the visible token is gold
			
				IF the token's code is not present in the gold vector
				
					IF the distance from the token is less than dist
					
						set token_info to token.info.code
						set dist to token.dist
						set rot_y to token.rot_y
						
					END IF
					
				ELSE
					
					IF dist is than avoid_d_th AND rot_y is between +/- avoid_a_th
				
						IF the angle is negative (or 0)
					
							set sign to +1 (clockwise rotation)
						
						ELSE 
					
							set sign to -1 (counterclockwise rotation)
						
						END IF
						
						call the avoid function, passing sign as a parameter
					
					END IF
				END IF
				
			END IF
			
		END FOR
		
	END IF
	
	IF dist is equal to 100 (has not changed during the execution of the function)
	
		RETURN fixed values (three -1)
		
	ELSE
		
		RETURN information about the found token (dist,rot_y,token_id)
		
	END IF
	
END FUNCTION


FUNCTION AVOID(sign)
	
	call the turn function, passing as parameters 15*sign and 0.5
	call the drive function, passing as parameters 50 and 0.8
	call the turn function, passing as parameters -20*sign and 0.5
	
END FUNCTION


FUNCTION MAIN()

	set mark to 'silver'
	set holding_id to -1
	
	WHILE(True)
	
		call the find_token function, passing as parameters: mark, holding_id and the two vectors
		get from the find_token function: dist, rot_y and token_id
		
		IF dist is equal to -1 (no visible valid token)
		
			call the turn function, passing as parameters -10 and 1
			
		ELSE IF dist is smaller than d_th
		
			IF mark is 'silver
			
				use the grab() method of the robot class, to grab the token
				set mark to 'gold'
				set holding_id to token_id
				append the token_id value into the silver vector
			
			END IF
			
		ELSE IF dist is less than release_d_th AND mark is 'gold' AND holding_id is not -1
		
			use the release() method of the robot class, to release the token
			set mark to 'silver'
			set holding_id to -1
			append the token_id value into the gold vector
			call the drive function, passing as parameters -60 and 3
			
		ELSE IF rot_y is between +/- a_th
		
			call the drive function, passing as parameters 45 and 0.5
			
		ELSE IF rot_y is less than -a_th
		
			call the turn function, passing as parameters -2 and 0.5
			
		ELSE IF rot_y is more than a_th
		
			call the turn function, passing as parameters +2 and 0.5
		
		END IF
		
		IF the length of the gold vector is six
		
			return (we terminate the execution)
		
		END IF
	
	END WHILE
	
END FUNCTION

## How to run the code:

The code is written in Python and in particular, Python2 is needed on your computer, in order to run this project.
Moreover, the following libraries are also needed to run the code: the [pygame](http://pygame.org/) library, the [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331) library and the [PyYAML](https://pypi.python.org/pypi/PyYAML) library.
You can download the .py files from the repository. Then, the code is executable by going in the folder where you've put the downloaded files and executing the following command:

```bash
$ python run.py assignment.py
```
(or whatever name you've given to the downloaded files).
During the execution, no input from the user is required.

## Possible improvements:

There is some possible improvement to implement into this code:

- By starting from the center of the map, the robot could turn 360° degrees and map all silver and gold token in some distance vectors, such that the robot is able to optimize its performance, knowing which golden token is closer to each silver one. This would probably reduce the time of execution.
- By turning 360° degrees, the robot could also count the number of blocks present on the entire map; in this way, the code wuold work for every number of silver and gold tokens: the code, with some modification, would terminate after he verify that there is no longer any uncoupled silver or golden token.
- The avoid function is used, as it was said before, to avoid dragging more silver tokens next to gold ones. This has been done for a particular reason: if two or more silver tokens are next to each others, when we use the grab method, there is a possibility that the grabbed token isn't the one that has yet to be coupled, but the one already coupled. This would lead to some problems. With the starting arrangement of the blocks, the avoid function is sufficient to avoid this problem, but, in order to avoid this problem in a more generalized way (i.e: for a different arrangement), a function which check if the grabbed token is already coupled or not could be implemented.
