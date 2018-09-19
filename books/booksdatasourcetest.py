'''
	Phase 2 of the Books homework assignment for CS 257, Jeff Ondich
	This program runs a variety of unit tests for booksdatasource.py
	Created by Eric Stadelman and Johnny Reichman, 9/19/18
'''

import booksdatasource
import unittest

class BooksDataSourceTest(unittest.TestCase):

	def setUp(self):
		self.books_data =... 
		booksdatasource.BooksDataSource("books.csv", 
			"authors.csv", "books_authors.csv")


	def tearDown(self):
		pass

	#The test cases will go here
		#a few that work
		#a few that don't
		#a few that aren't even close to working



if __name__ == '__main__':
    unittest.main()

