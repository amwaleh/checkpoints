from checkpoint1 import Space
import unittest
import os

class TestMyFunctions(unittest.TestCase):

	
	def test_living_allocate (self):

		office = Space(1,'rooms',3)
		self.assertEqual(office.max_people, 1)
		self.assertEqual(office.num_rooms, 3)
		os.remove(office.path)

	def test_defaults(self):

		office = Space(1,'rooms')
		self.assertEqual(office.max_people, 1)
		self.assertEqual(office.num_rooms, 1)
		os.remove(office.path)
	# check if the list created is a dict
	def test_generate_room(self) :
		Space
		office = Space(3,'rooms',4)
		# check if a dictioanry containing rooms has been created
		self.assertTrue(type(office.room_list), type({}))
		# Check the rooms created are equal to specified rooms
		self.assertEqual(office.num_rooms, len(office.room_list))
		os.remove(office.path)

	def test_allocate_room(self):
		office = Space(1,'prooms')
		#check if dictionary has been created
		self.assertTrue(type(office.room_list), type({}))
		# check if number passed is corrected 
		self.assertEqual(office.num_rooms, 1)
		#check if the list of room coincides with the number of rooms generated
		self.assertEqual(len(office.room_list), 1)
		#check if naming convention is right and it exists 
		self.assertTrue('prooms 0' in office.room_list.keys(), True)
		#check if the list created has empty list
		self.assertListEqual(office.room_list['prooms 0'], [])
		#allocate a room 
		name = 'david'
		r_alloc = (office.allocate_room(name))
		#check if name assigned is returned 
		self.assertIn(name,r_alloc,)
		#remove test file

		os.remove(office.path)

	def test_get_from_file(self):
		office = Space(1,'prooms', 1)
		d = office.get_from_file('data/sample.txt')
		#check if the number list items equals number of lines ina file 
		with open('data/sample.txt' ) as f:
			total = sum(1 for _ in f)
		self.assertTrue(type(d),type([]))of 
		#check that the lit has equal number lines and 
		self.assertTrue(len(d), total)





		


if __name__ == '__main__' :
	unittest.main(exit = False)