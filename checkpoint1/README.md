# checkpoints 1
# Dojo Room Allocat

This module is used to Randomly allocate space to a defined set of rooms
 that can hold a defined number of people.

# Usage

## SPace Class
	Space class module in the checkpoint1.py is used to model the rooms
	
	Space (Number of People, Room_Name, Number_of_Rooms)

##The class takes three optional params
	Number_of_people = maximum number a room can take.
	Room_Name 	= The Name you want to allocate the room e.g. Office, Living etc
	Number_of_Rooms =Number of rooms you want your building to have. 

#To create Room:
1.instatiate the class
	
	class = Space()

	

	This will create an Object with 1 space per room and will load rooms from the 'room.txt' file 

or 
	
	class = Space(3, 'mountain', 2)
	

This will create Object with 2 rooms prefixed with the Room_Param e.h Mountain 1 and mountain 2 as the room Name



#Room Allocation
	1.Room Allocation can be done manually by calling the room_allocate() function
	 class.room_allocate('John Smith')

	This will randomly chose a vacant room and allocate the name 
	
	2. Rooms can also be allocated from a file by evoking the get_from_file() function
	 class.get_from_file(r"allocation.txt")

	This method returns alist of all the file
check the allocation.txt for formatting
# Development

https://github.com/andela-amwaleh/checkpoints

			
