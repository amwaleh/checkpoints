import random 		# for randomizing lists
import os  			# for finding files and path
import ast  		# for convertion of strings to dictionary

class Space(object):
		
	def __init__(self, max_people = 1, type_of_room = 'file', num_rooms = 1):
		# generate rooms according to type and capacity

	
		self.max_people = max_people
		self.num_rooms = num_rooms
		self.type_of_room = type_of_room
		self.rooms = [self.type_of_room + ' %d' %x for x in range(self.num_rooms)]
		self.path = "data/" + self.type_of_room + ".txt"
		
		# load room file file else generate 
		# check if file exists
		if (os.path.isfile(self.path)):
			file = open (self.path, 'r')
			self.room_list =file.read()
			file.close
			''' the list gotten from file is in string format we need 
				to convert it to dictionary type by using ast.literal_eval()
				Check if the file has any data errors i.e 
			''' 

			if len(self.room_list) > 0:
			
				self.room_list = ast.literal_eval(self.room_list)
			else:
				
				self.room_list = {}
				
		else:
			# If a value for type of room 
			if self.type_of_room !='file':
				# Generates dictionary with keys as name of room (type_of_room) as prefix
				# Start with empty dictionary
				# Assign each key a list of occupants
				self.room_list = {}
				for room in self.rooms :
					self.room_list[room] = []
				self.save_list()

			else:
				# Generate list from Room.txt
				self.room_list = {}
				# Use the get_from_file to generate list
				data = self.get_from_file('room.txt')
				#Generate dictionary with names from list
				for line in data :
					
					self.room_list[line[0]] = []
				self.num_rooms = len(self.room_list)
				# Save the list :)
				self.save_list()
				


		
	def allocate_room(self, name_person):
		# assign name to room list
		# shuffle the room names and randomly allocate to person
		self.name_person = name_person
		room = self.room_list
		keys = list(room.keys())

		# shuffle rooms  each time allocate_room is called
		random.shuffle(keys)

		for key in keys :
			if self.num_rooms > 0 and len(room[key]) < self.max_people:
				room[key].append(name_person)

				# Print allocated room
				# Save details to file				
				# Return room allocated and persons name
				self.save_list()
				return [key, name_person]

		# Return list with -1 and  message if all rooms have been allocated
		return [-1, "{}  Rooms Fully Occupied".format(self.type_of_room)]

	def save_list(self):
		# Check if file exists
		file = open(self.path, 'w')

		# Save data,room_name in textfile as a string
		file.write (str(self.room_list))
		file.close


	def print_allocation(self):
		report=''
		for room in sorted(self.room_list.iterkeys()) :
			report +=room + "\n"
			for person in self.room_list[room]:
				report += person +", "

			report += "\n \n"
		return report

	# Return status of the room by availing a list of occupants and free spaces 
	def print_status(self):
		empty_spaces = 0
		status=''
		for room in sorted(self.room_list.iterkeys()) :
			
			status += " {} |occupants= {} | Max-Pax = {} | free space = {}\n".format(room, len(self.room_list[room]),
																					self.max_people, 
																					(self.max_people - len(self.room_list[room])))
			empty_spaces += self.max_people - len(self.room_list[room])

		# Return a list of empty spaces and a string of the summary			
		return [empty_spaces,status]


	def get_from_file(self,path):
		file_list =[]
		file = open(path, 'r')

		for line in file :
			# Remove tabs using string expression
			file_list.append(line.split())
		file.close
		# Return a list
		return file_list

	def get_room_occupants(self, room_name):
		return self.room_list[room_name]
