'''
	Phase 2 of the Books homework assignment for CS 257, Jeff Ondich
	This program runs a variety of unit tests for booksdatasource.py
	Created by Eric Stadelman and Johnny Reichman, 9/21/18
'''
import csv
import booksdatasource
import unittest

class BooksDataSourceTest(unittest.TestCase):

	def setUp(self):
		self.books_data = booksdatasource.BooksDataSource("books.csv", 
			"authors.csv", "books_authors.csv")


	def tearDown(self):
		pass


	#tests for book()
	def test_book_found(self):
		self.assertEqual(self.books_data.book(6), "6,Good Omens,1990")

	def test_book_invalid(self):
		self.assertRaises(ValueError, self.books_data.book, -1)


	#tests for books()
	def test_books_author_id(self):
		self.assertEqual(self.books_data.books(author_id = 6), "5,Emma,1815")

	def test_books_author_id_invalid(self):
		self.assertRaises(ValueError, self.books_data.books, author_id = -1)

	def test_books_search_text(self):
		self.assertEqual(self.books_data.books(search_text = "moby dick"), 
			"13,Moby Dick,1851")

	def test_books_start_year(self):
		self.assertEqual(self.books_data.books(start_year = 2016), 
			"35,The Power,2016")

	def test_books_end_year(self):
		self.assertEqual(self.books_data.books(end_year = 1813), 
			"18,Pride and Predudice,1813\n20,Sense and Sensibility,1813")

	def test_books_sort_by_year(self):
		self.assertEqual(self.books_data.books(search_text = "bl", 
			sort_by = "year"), "43,Bleak House,1852\n3,Blackout,2010")

	def test_books_multiple_parameters(self):
		self.assertEqual(self.books_data.books(start_year = 2016, 
			end_year = 2016, search_text = "power"),"35,The Power,2016")

	def test_books_none_found(self):
		self.assertEqual(self.books_data.books(start_year = 3000), "")

	def test_books_no_parameters(self):
		book_list = []
		with open("books.csv", 'r', newline = '') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				book_list.append(row)
			book_list.sort(key = lambda book_list: book_list[2])
			book_list.sort(key = lambda book_list: book_list[1])
			self.assertEqual(self.books_data.authors() , book_list)


	#tests for author()
	def test_author_found(self):
		self.assertEqual(self.books_data.author(5), "5,Gaiman,Neil,1960,NULL")

	def test_author_invalid(self):
		self.assertRaises(ValueError, self.books_data.author, -1)


	#tests for authors()
	def test_authors_book_id(self):
		self.assertEqual(self.books_data.authors(book_id = 0), 
			"0,Willis,Connie,1945,NULL")

	def test_authors_search_text(self):
		self.assertEqual(self.books_data.authors(search_text = "will"), 
			"17,Cather,Willa,1873,1947\n0,Willis,Connie,1945,NULL")

	def test_authors_end_year(self):
		self.assertEqual(self.books_data.authors(end_year = 1776), 
			"4,Austen,Jane,1775,1817")

	def test_authors_start_year_end_year(self):
	 	self.assertEqual(self.books_data.authors(start_year = 1810, 
	 		end_year = 1812), 
	 	"4,Austen,Jane,1775,1817\n23,Dickens,Charles,1812,1870")

	def test_authors_for_book_same_year(self):
		self.assertEqual(self.books_data.authors(start_year = 1913, 
			end_year = 1913), "O Pioneers!")

	def test_authors_sort_by_year(self):
	 	self.assertEqual(self.books_data.authors(search_text = "Je", 
	 		sort_by = "birth_year"), 
	 	"21,Jerome,Jerome K.,1859,1927\n20,Jemisen,N.K.,1972,NULL")

	def test_authors_multiple_parameters(self):
	 	self.assertEqual(self.books_data.authors(start_year = 1775, 
	 		end_year = 1776, search_text = "Jane"),"4,Austen,Jane,1775,1817")

	def test_authors_none_found(self):
	 	self.assertEqual(self.books_data.authors(end_year = -3000), "")

	def test_authors_book_invalid(self):
		self.assertRaises(ValueError, self.books_data.authors, book_id = -1)

	def test_authors_no_parameters(self):
		author_list = []
		with open("authors.csv", 'r', newline = '') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				author_list.append(row)
			author_list.sort(key = lambda author_list: author_list[3])
			author_list.sort(key = lambda author_list: author_list[2])
			author_list.sort(key = lambda author_list: author_list[1])
			self.assertEqual(self.books_data.authors() , author_list)


	#tests for books_for_author()
	def test_books_for_author_one_found(self):
		self.assertEqual(self.books_data.books_for_author(10), "10,Main Street,1920")

	def test_books_for_author_two_found(self):
		self.assertEqual(self.books_data.books_for_author(2), 
			"2,Beloved,1987\n22,Sula,1973")

	def test_books_for_author_invalid(self):
		self.assertRaises(ValueError, self.books_data.books_for_author, -1)


	#tests for authors_for_book()
	def test_authors_for_book_one_found(self):
		self.assertEqual(self.books_data.authors_for_book(0) , 
			"0,Willis,Connie,1945,NULL")

	def test_authors_for_book_two_found(self):
		self.assertEqual(self.books_data.authors_for_book(6) , 
			"6,Gaiman,Neil,1960,Null\n6,Pratchett,Terry,1948,2018")

	def test_authors_for_book_invalid(self):
		self.assertRaises(ValueError, self.books_data.authors_for_book, -1)


if __name__ == '__main__':
    unittest.main()

