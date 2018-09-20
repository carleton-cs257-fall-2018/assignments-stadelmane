'''
	Phase 2 of the Books homework assignment for CS 257, Jeff Ondich
	This program runs a variety of unit tests for booksdatasource.py
	Created by Eric Stadelman and Johnny Reichman, 9/19/18
'''

import booksdatasource
import unittest

class BooksDataSourceTest(unittest.TestCase):

	def setUp(self):
		self.books_data = booksdatasource.BooksDataSource("books.csv", "authors.csv", "books_authors.csv")


	def tearDown(self):
		pass


	#tests for book()
	def test_book_found(self):
		self.assertEqual(self.books_data.book(6), "6,Good Omens,1990")

	def test_book_unfound(self):
		self.assertRaises(ValueError, self.books_data.book, 1000)

	def test_book_invalid(self):
		self.assertRaises(ValueError, self.books_data.book, "g")




	#tests for books()
	def test_books_author_unfound(self):
		self.assertRaises(ValueError, self.books_data.books, author_id = 1000)

	def test_books_invalid(self):
		self.assertRaises(ValueError, self.books_data.books, author_id = "g")



	#tests for author()
	def test_author_found(self):
		self.assertEqual(self.books_data.author(5) , "5,Gaiman,Neil,1960,NULL")

	def test_author_unfound(self):
		self.assertRaises(ValueError, self.books_data.author, 1000)

	def test_author_invalid(self):
		self.assertRaises(ValueError, self.books_data.author, "g")


	#tests for authors()
	def test_authors_book_unfound(self):
		self.assertRaises(ValueError, self.books_data.authors, book_id = 1000)

	def test_authors_invalid(self):
		self.assertRaises(ValueError, self.books_data.authors, book_id = "g")




	#tests for books_for_author()
	def test_books_for_author_one_found(self):
		self.assertEqual(self.books_data.books_for_author(10), "10,Main Street,1920")

	def test_books_for_author_two_found(self):
		self.assertEqual(self.books_data.books_for_author(2), "2,Beloved,1987\n22,Sula,1973")

	def test_books_for_author_none_found(self):
		self.assertRaises(ValueError, self.books_data.books_for_author, 1000)



	#tests for authors_for_book()
	def test_authors_for_book_one_found(self):
		self.assertEqual(self.books_data.authors_for_book(0) , "0,Willis,Connie,1945,NULL")

	def test_authors_for_book_two_found(self):
		self.assertEqual(self.books_data.authors_for_book(6) , "6,Gaiman,Neil,1960,Null\n6,Pratchett,Terry,1948,2018")

	def test_authors_for_book_none_found(self):
		self.assertRaises(ValueError, self.books_data.authors_for_book, 1000)




if __name__ == '__main__':
    unittest.main()

