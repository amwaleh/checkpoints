from checkpoint1 import Space
import os

office =Space('Office',10,6)
living =Space('living',10,5)





def living_allocate(path):

	if (os.path.isfile(path)):

		d =living.get_from_file(path)
		
		i=0
		print ("====================== List of allocation Living =========================\n")
		for x in d:
			
			if 'Y' in x and 'FELLOW' in x:
				
				s = living.allocate_room((x[0] + " "+ x[1]))
				print (s[1])
				if s[0] == -1 : break
				d.remove(x)
			i +=1
		print ("People allocated = {}".format(i))
		print ("\n"*3)
		unallocated(d,living.type_of_room)
	else:
		print('FILE NOT FOUND %s' %path)

def office_allocate(path):

	d=office.get_from_file(path)
	print ("====================== List of allocation  Office=========================\n")
	i=0
	for x in d:
		
		s = living.allocate_room((x[0] + " "+ x[1]))
		print (s[1])
		if s[0] == -1 : break
		d.remove(x)
	i +=1
	print ("People allocated = {}".format(i))
	print ("\n"*3)
	unallocated(d,office.type_of_room)
	

def unallocated(list,room_type):
	print ("====================== List of unallocated ({})=========================\n".format(room_type))
	for z in list:
		print ("{}  {: ^10}  {:_>10} ".format (z[0],z[1],z[2]))




#living_allocate(d)
#office_allocate(s)

#office.pr(int_allocation()
#living.print_allocation()


#print living.print_allocation()

while True :
	print("\n\n 1: insert \n")
	print("0: Allocate Office")
	print("1: Allocate Living Space")
	print("2: Allocate both living and office")
	try:
		room_type = int(raw_input("allocate: "))
		if room_type in[0,1,2]: break
	except :
		print("ERROR: insert 0, 1, or 2")

while True:	
	print("\n 2:Choose \n")
	print("3: to insert Name directly")
	print("4: load names from a file")
	try:
		source  = int(raw_input("allocate: "))
		if source in [3 ,4] : break
	except :
		print("ERROR: insert 3 0r 4")

office =Space('Office',10,6)
living =Space('living',10,5)





if source == 3 :	
	while True:	
		
		inp = raw_input("Insert Name :")
		if inp !='':
			# exit code if input is 'exit'
			if inp == 'exit' : break
			# allocate room to person 
			if room_type == 0 :print (office.allocate_room(inp))
			if room_type == 1 : print (living.allocate_room(inp))
			if room_type == 2 : 
				print (office.allocate_room(inp))
				print (living.allocate_room(inp))
			# print allocated room
			


if source == 4:
	#try:
		file_path= raw_input(r"Insert full path of File :")
		if room_type == 0 : print (office_allocate(file_path))
		if room_type == 1 : print (living_allocate(file_path))
		if room_type == 2 : 
			print (office_allocate(file_path))
			print (living_allocate(file_path))

		
	#except :
		#print (" Error : File was not found / wrong path")
		

