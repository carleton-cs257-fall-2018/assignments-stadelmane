#!/usr/bin/env python3
'''
	booksdatasource.py
	Interface by Jeff Ondich, 18 September 2018
	Implementation by Johnny Reichman and Eric Stadelman, 25 September 2018

	For use in some assignments at the beginning of Carleton's
	CS 257 Software Design class, Fall 2018.
'''
import csv

class BooksDataSource:
	
	#initialization creates a book_list, author_list, and match_list
	def __init__(self, books_filename, authors_filename, 
		books_authors_link_filename):
	   
		#stores book data as a list of dictionaries with the keys:
		#'id', 'title', and 'publication_year'
		with open(books_filename, 'r', newline = '') as books_file:
			self.book_list = []
			books_reader = csv.reader(books_file)
			for row in books_reader:
				new_book = {
				  "id": int(row[0]),
				  "title": row[1],
				  "publication_year": int(row[2])
				}
				self.book_list.append(new_book)


		#stores author data as a list of dictionaries with the keys:
		#'id', 'last_name', 'first_name', and 'death_year'
		with open(authors_filename, 'r', newline = '') as authors_file:
			self.author_list = []
			authors_reader = csv.reader(authors_file)
			for row in authors_reader:
				if(row[4] != "NULL"):
					death_year = int(row[4])
				else:
					death_year = row[4]
				new_author = {
				"id": int(row[0]),
				"last_name": row[1],
				"first_name": row[2],
				"birth_year": int(row[3]),
				"death_year": death_year
				}
				self.author_list.append(new_author)


		#stores match data to help link books with their authors
		#as a list of dictionaries with the keys: 'book_id' and 'author_id'
		with open(books_authors_link_filename, 'r',newline = '') as link_file:
			self.match_list = []
			match_reader = csv.reader(link_file)
			for row in match_reader:
				new_match = {
				  "book_id": int(row[0]),
				  "author_id": int(row[1])
				}
				self.match_list.append(new_match)


	#Returns the book with the specified ID.
	def book(self, book_id):
		if(book_id < 0 or book_id >= len(self.book_list)):
			raise ValueError('not a valid book_id: ', book_id)
		return self.book_list[book_id]

	#Returns a list of all the books in this data source matching all of 
	#the specified non-None criteria.
	def books(self, *, author_id=None, search_text=None, start_year=None, 
					   end_year=None, sort_by='title'):
		
		found_books = self.book_list

		#filtering by author_id, if applicable
		if(author_id != None):
			found_books = self.books_for_author(author_id)

		#filtering by search_text, if applicable
		if(search_text != None):
			book_index = 0
			while(book_index < len(found_books)):
				if(search_text.lower() not in 
						found_books[book_index].get("title").lower()):
					found_books.remove(found_books[book_index])
					book_index-= 1
				book_index += 1

		#filtering by start_year, if applicable
		if (start_year != None):
			book_index = 0
			while(book_index < len(found_books)):
				if(found_books[book_index].get("publication_year") < 
						start_year):
					found_books.remove(found_books[book_index])
					book_index -= 1
				book_index += 1

		#filtering by end_year, if applicable
		if (end_year != None):
			book_index = 0
			while(book_index < len(found_books)):
				if(found_books[book_index].get("publication_year") > 
						end_year):
					found_books.remove(found_books[book_index])
					book_index -= 1
				book_index += 1


		if sort_by != "year":
			found_books = sorted(found_books, 
								 key = lambda k: k["publication_year"])
			found_books = sorted(found_books, key = lambda k: k["title"])

		if sort_by == "year":
			found_books = sorted(found_books, key = lambda k: k["title"])
			found_books = sorted(found_books, 
								 key = lambda k: k["publication_year"])

		return found_books

	#Returns the author with the specified ID.
	def author(self, author_id):
		if(author_id < 0 or author_id >= len(self.author_list)):
			raise ValueError('not a valid author_id: ', author_id)
		return self.author_list[author_id]


	#Returns a list of all the authors in this data source matching all of
	#the specified non-None criteria.
	def authors(self, *, book_id=None, search_text=None, start_year=None, 
						 end_year=None, sort_by='birth_year'):

		found_authors = self.author_list

		#filtering by book_id, if applicable
		if(book_id != None):
			found_authors = self.authors_for_book(book_id)

		#filtering by search_text, if applicable
		if(search_text != None):
			author_index = 0
			while(author_index < len(found_authors)):
				if(search_text.lower() not in 
						found_authors[author_index].get("last_name").lower()
						and search_text.lower() not in 
						found_authors[author_index].get("first_name").lower()):
					found_authors.remove(found_authors[author_index])
					author_index-= 1
				author_index += 1

		#filtering by start_year, if applicable
		if (start_year != None):
			author_index = 0
			while(author_index < len(found_authors)):
				if(found_authors[author_index].get("death_year") != "NULL" and
						found_authors[author_index].get("death_year") < 
						start_year):
					found_authors.remove(found_authors[author_index])
					author_index -= 1
				author_index += 1

		#filtering by end_year, if applicable
		if (end_year != None):
			author_index = 0
			while(author_index < len(found_authors)):
				if(found_authors[author_index].get("birth_year") > end_year):
					found_authors.remove(found_authors[author_index])
					author_index -= 1
				author_index += 1


		if sort_by != "birth_year":
			found_authors = sorted(found_authors, 
								   key = lambda k: k["birth_year"])
			found_authors = sorted(found_authors, 
								   key = lambda k: k["first_name"])
			found_authors = sorted(found_authors, 
								   key = lambda k: k["last_name"])

		if sort_by == "year":
			found_authors = sorted(found_authors, 
								   key = lambda k: k["first_name"])
			found_authors = sorted(found_authors, 
								   key = lambda k: k["last_name"])
			found_authors = sorted(found_authors, 
				    			   key = lambda k: k["birth_year"])

		return found_authors


	#Returns a list of all the books written by the author with the specified 
	#author ID.
	def books_for_author(self, author_id):
		if(author_id < 0 or author_id >= len(self.author_list)):
			raise ValueError('not a valid author_id: ', author_id)

		authors_works = []
		for match in self.match_list:
			if match.get("author_id") == author_id:
				authors_works.append(self.book(match.get("book_id")))
		
		return authors_works


	#Returns a list of all the authors of the book with the specified book ID.
	def authors_for_book(self, book_id):
		if(book_id < 0 or book_id >= len(self.book_list)):
			raise ValueError('not a valid book_id: ', book_id)

		books_contributors = []
		for match in self.match_list:
			if match.get("book_id") == book_id:
				books_contributors.append(self.author(match.get("author_id")))
		
		return books_contributors


def main():
	test_book_list = BooksDataSource("books.csv", "authors.csv", "books_authors.csv")

	print(test_book_list.authors_for_book(-4))







if __name__ == "__main__":
	main()

