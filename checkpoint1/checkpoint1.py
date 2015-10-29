import random 		# for randomizing lists
import os  			# for finding files and path
import ast  		# for convertion of strings to dictionary

class Space(object):
		
	def __init__(self, type_of_room, num_rooms = 10, max_people = 1):
		# generate rooms according to type and capacity

	
		self.max_people = max_people
		self.num_rooms = num_rooms
		self.type_of_room = type_of_room
		self.rooms = [self.type_of_room + ' %d' %x for x in range(self.num_rooms)]
		
		# load room file file else generate 
		# check if file exists
		if (os.path.isfile(self.type_of_room + ".txt")):
			file = open (self.type_of_room + ".txt", 'r')
			self.room_list =file.read()
			file.close
			''' the list gotten from file is in string format we need 
				to convert it to dictionary type by using ast.literal_eval()
				Check if the file has any data errors i.e 
			''' 

			if len(self.room_list) > 0:
			#try:
				self.room_list = ast.literal_eval(self.room_list)
			else:
				#print ('error occured')
				self.room_list = {}
				
		else:
			# Generates dictionary with keys as name of room (type_of_room) as prefix
			# start with empty dictionary
			# assign each key a list of occupants
			self.room_list = {}
			for room in self.rooms :
				self.room_list[room] = []
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
				# print alocated room
				# save details to file				
				# return room allocated
				self.save_list()
				return [key, room[key][0]]
		 # return list with -1 and  message if all rooms have been allocated
		return [-1, "{}  Rooms Fully Occupied".format(self.type_of_room)]

	def save_list(self):
		#check if file exists
		f_name = self.type_of_room +'.txt'
		file = open(f_name, 'w')
		#save data,room_name in textfile as a string
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

	def get_from_file(self,path):
		file_list =[]
		file = open(path, 'r')
		for line in file :
				
			# remove tabs using string expression
			file_list.append(line.split())
			# split using comma and store in list
			#read list check if its a student
			#if ('N' in l) : print('register')
			#check if flag N is on 
			# allocate room
			# ignore staff and student with y 
		file.close
		return file_list
