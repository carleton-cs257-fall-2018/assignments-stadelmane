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
		self.assertEqual(self.books_data.book(6), {"id": 6, "title": "Good Omens","publication_year": 1990})

	def test_book_invalid(self):
		self.assertRaises(ValueError, self.books_data.book, -1)


	#tests for books()
	def test_books_author_id(self):
		self.assertEqual(self.books_data.books(author_id = 6), 
			[{'id': 6, 'title': 'Good Omens','publication_year': 1990} , 
	{'id': 26, 'title': 'Thief of Time','publication_year': 1996}])

	def test_books_author_id_invalid(self):
		self.assertRaises(ValueError, self.books_data.books, author_id = -1)

	def test_books_search_text(self):
		self.assertEqual(self.books_data.books(search_text = "moby dick"), 
			[{"id": 13, "title": "Moby Dick", "publication_year": 1851}])

	def test_books_start_year(self):
		self.assertEqual(self.books_data.books(start_year = 2016), 
			[{'id': 35, 'title': 'The Power','publication_year': 2016}])

	def test_books_end_year(self):
		self.assertEqual(self.books_data.books(end_year = 1813), 
			[{'id': 18, 'title': 'Pride and Prejudice', 'publication_year': 1813}, 
			{'id': 20, 'title': 'Sense and Sensibility', 'publication_year': 1813}])

	def test_books_sort_by_year(self):
		self.assertEqual(self.books_data.books(search_text = "bl", 
			sort_by = "year"), 
		[{'id': 43, 'title': 'Bleak House', 'publication_year': 1852}, 
		{'id': 3, 'title': 'Blackout', 'publication_year': 2010}])

	def test_books_multiple_parameters(self):
		self.assertEqual(self.books_data.books(start_year = 2016, 
			end_year = 2016, search_text = "power"),
		[{'id': 35, 'title': 'The Power', 'publication_year': 2016}])

	def test_books_none_found(self):
		self.assertEqual(self.books_data.books(start_year = 3000), [])

	def test_books_no_parameters(self):
		intended_list = sorted(self.books_data.book_list, key = lambda 
			k: k["publication_year"])
		intended_list.sort(key = lambda k: k["title"])
		self.assertEqual(self.books_data.books() , intended_list)


	#tests for author()
	def test_author_found(self):
		self.assertEqual(self.books_data.author(5), 
			{'id': 5, 'last_name': 'Gaiman', 'first_name': 'Neil', 
			'birth_year': 1960, 'death_year': 'NULL'})

	def test_author_invalid(self):
		self.assertRaises(ValueError, self.books_data.author, -1)


	#tests for authors()
	def test_authors_book_id(self):
		self.assertEqual(self.books_data.authors(book_id = 0), 
			[{'id': 0, 'last_name': 'Willis', 'first_name': 'Connie', 
			'birth_year': 1945, 'death_year': 'NULL'}])

	def test_authors_search_text(self):
		self.assertEqual(self.books_data.authors(search_text = "will"), 
			[{'id': 17, 'last_name': 'Cather', 'first_name': 'Willa', 
			'birth_year': 1873, 'death_year': 1947}, {'id': 0, 
			'last_name': 'Willis', 'first_name': 'Connie', 
			'birth_year': 1945, 'death_year': 'NULL'}])

	def test_authors_end_year(self):
		self.assertEqual(self.books_data.authors(end_year = 1776), [{'id': 4,
		 'last_name': 'Austen', 'first_name': 'Jane',
		  'birth_year': 1775, 'death_year': 1817}])

	def test_authors_start_year_end_year(self):
	 	self.assertEqual(self.books_data.authors(start_year = 1810, 
	 		end_year = 1812), [{'id': 4, 'last_name': 'Austen', 
	 	'first_name': 'Jane','birth_year': 1775, 'death_year': 1817},
	 	 {'id': 23,'last_name': 'Dickens', 'first_name': 'Charles',
	 		 'birth_year': 1812, 'death_year': 1870}])

	def test_authors_for_book_same_year(self):
		self.assertEqual(self.books_data.authors(start_year = 1913, 
			end_year = 1913), [{'id': 21, 'last_name': 'Jerome', 
		'first_name': 'Jerome K.', 'birth_year': 1859, 'death_year': 1927}, 
		{'id': 17, 'last_name': 'Cather', 'first_name': 'Willa', 
		'birth_year': 1873, 'death_year': 1947}, {'id': 8, 
		'last_name': 'Wodehouse', 'first_name': 'Pelham Grenville', 
		'birth_year': 1881, 'death_year': 1975}, {'id': 3, 
		'last_name': 'Lewis', 'first_name': 'Sinclair', 'birth_year': 1885, 
		'death_year': 'NULL'}, {'id': 10, 'last_name': 'Lewis', 'first_name': 
		'Sinclair', 'birth_year': 1885, 'death_year': 1951}, {'id': 1, 
		'last_name': 'Christie', 'first_name': 'Agatha', 'birth_year': 1890, 
		'death_year': 1976}, {'id': 19, 'last_name': 'DuMaurier', 
		'first_name': 'Daphne', 'birth_year': 1907, 'death_year': 1989}])

	def test_authors_sort_by_year(self):
	 	self.assertEqual(self.books_data.authors(search_text = "Je", 
	 		sort_by = "birth_year"), [{'id': 21, 'last_name': 'Jerome',
	 		 'first_name': 'Jerome K.', 'birth_year': 1859,
	 		 'death_year': 1927},{'id': 20, 'last_name': 'Jemisen',
	 		 'first_name': 'N.K.', 'birth_year': 1972, 'death_year': 'NULL'}])

	def test_authors_multiple_parameters(self):
	 	self.assertEqual(self.books_data.authors(start_year = 1775, 
	 		end_year = 1776, search_text = "Jane"),
	 	[{'id': 4, 'last_name': 'Austen', 'first_name': 'Jane', 
	 	'birth_year': 1775, 'death_year': 1817}])

	def test_authors_none_found(self):
	 	self.assertEqual(self.books_data.authors(end_year = -3000), [])

	def test_authors_book_invalid(self):
		self.assertRaises(ValueError, self.books_data.authors, book_id = -1)

	def test_authors_no_parameters(self):
		intended_list = sorted(self.books_data.author_list, key = lambda 
			k: k["first_name"])
		intended_list.sort(key = lambda k: k["last_name"])
		intended_list.sort(key = lambda k: k["birth_year"])
		self.assertEqual(self.books_data.authors() , intended_list)


	#tests for books_for_author()
	def test_books_for_author_one_found(self):
		self.assertEqual(self.books_data.books_for_author(10), [{'id': 10, 
			'title': 'Main Street', 'publication_year': 1920}])

	def test_books_for_author_two_found(self):
		self.assertEqual(self.books_data.books_for_author(2), 
			[{'id': 2, 'title': 'Beloved', 'publication_year': 1987}, 
			{'id': 22, 'title': 'Sula', 'publication_year': 1973}])

	def test_books_for_author_invalid(self):
		self.assertRaises(ValueError, self.books_data.books_for_author, -1)


	#tests for authors_for_book()
	def test_authors_for_book_one_found(self):
		self.assertEqual(self.books_data.authors_for_book(0) ,[{'id': 0, 
			'last_name': 'Willis', 'first_name': 'Connie', 'birth_year': 1945,
			 'death_year': 'NULL'}])

	def test_authors_for_book_two_found(self):
		self.assertEqual(self.books_data.authors_for_book(6) , [{'id': 5, 
			'last_name': 'Gaiman', 'first_name': 'Neil', 'birth_year': 1960, 
			'death_year': 'NULL'}, {'id': 6, 'last_name': 'Pratchett', 
			'first_name': 'Terry', 'birth_year': 1948, 'death_year': 2015}])

	def test_authors_for_book_invalid(self):
		self.assertRaises(ValueError, self.books_data.authors_for_book, -1)


if __name__ == '__main__':
    unittest.main()

