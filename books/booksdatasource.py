#!/usr/bin/env python3
'''
    booksdatasource.py
    Jeff Ondich, 18 September 2018

    For use in some assignments at the beginning of Carleton's
    CS 257 Software Design class, Fall 2018.
'''
import csv

class BooksDataSource:
    '''
    A BooksDataSource object provides access to data about books and authors.
    The particular form in which the books and authors are stored will
    depend on the context (i.e. on the particular assignment you're
    working on at the time).

    Most of this class's methods return Python lists, dictionaries, or
    strings representing books, authors, and related information.

    An author is represented as a dictionary with the keys
    'id', 'last_name', 'first_name', 'birth_year', and 'death_year'.
    For example, Jane Austen would be represented like this
    (assuming her database-internal ID number is 72):

        {'id': 72, 'last_name': 'Austen', 'first_name': 'Jane',
         'birth_year': 1775, 'death_year': 1817}

    For a living author, the death_year is represented in the author's
    Python dictionary as None.

        {'id': 77, 'last_name': 'Murakami', 'first_name': 'Haruki',
         'birth_year': 1949, 'death_year': None}

    Note that this is a simple-minded representation of a person in
    several ways. For example, how do you represent the birth year
    of Sophocles? What is the last name of Gabriel García Márquez?
    Should we refer to the author of "Tom Sawyer" as Samuel Clemens or
    Mark Twain? Are Voltaire and Molière first names or last names? etc.

    A book is represented as a dictionary with the keys 'id', 'title',
    and 'publication_year'. For example, "Pride and Prejudice"
    (assuming an ID of 132) would look like this:

        {'id': 193, 'title': 'A Wild Sheep Chase', 'publication_year': 1982}

    '''

    def __init__(self, books_filename, authors_filename, books_authors_link_filename):
       
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
        #stored as a list of dictionaries with the keys: 'book_id' and 'author_id'
        with open(books_authors_link_filename, 'r', newline = '') as match_file:
            self.match_list = []
            match_reader = csv.reader(match_file)
            for row in match_reader:
                new_match = {
                  "book_id": int(row[0]),
                  "author_id": int(row[1])
                }
                self.match_list.append(new_match)


    #Returns the book with the specified ID.
    def book(self, book_id):
         
        return self.book_list[book_id]

    #Returns a list of all the books in this data source matching all of the specified non-None criteria.
    def books(self, *, author_id=None, search_text=None, start_year=None, end_year=None, sort_by='title'):
        
        found_books = self.book_list
        if(author_id != None):
            found_books = self.books_for_author(author_id)

        if(search_text != None):
            book_index = 0
            while(book_index < len(found_books)):
                if(search_text.lower() not in found_books[book_index].get("title").lower()):
                    found_books.remove(found_books[book_index])
                    book_index-= 1
                book_index += 1


        if (start_year != None):
            book_index = 0
            while(book_index < len(found_books)):
                if(found_books[book_index].get("publication_year") < start_year):
                    found_books.remove(found_books[book_index])
                    book_index -= 1
                book_index += 1

        if (end_year != None):
            book_index = 0
            while(book_index < len(found_books)):
                if(found_books[book_index].get("publication_year") > end_year):
                    found_books.remove(found_books[book_index])
                    book_index -= 1
                book_index += 1


        if sort_by != "year":
            found_books = sorted(found_books, key = lambda k: k["publication_year"])
            found_books = sorted(found_books, key = lambda k: k["title"])

        if sort_by == "year":
            found_books = sorted(found_books, key = lambda k: k["title"])
            found_books = sorted(found_books, key = lambda k: k["publication_year"])

        return found_books



    def author(self, author_id):
        ''' Returns the author with the specified ID. (See the BooksDataSource comment for a
            description of how an author is represented.) '''
        return self.author_list[author_id]

    def authors(self, *, book_id=None, search_text=None, start_year=None, end_year=None, sort_by='birth_year'):
        ''' Returns a list of all the authors in this data source matching all of the
            specified non-None criteria.

                book_id - only returns authors of the specified book
                search_text - only returns authors whose first or last names contain
                    (case-insensitively) the search text
                start_year - only returns authors who were alive during or after
                    the specified year
                end_year - only returns authors who were alive during or before
                    the specified year

            Note that parameters with value None do not affect the list of authors returned.
            Thus, for example, calling authors() with no parameters will return JSON for
            a list of all the authors in the data source.

            The list of authors is sorted in an order depending on the sort_by parameter:

                'birth_year' - sorts by birth_year, breaking ties with (case-insenstive) last_name,
                    then (case-insensitive) first_name
                any other value - sorts by (case-insensitive) last_name, breaking ties with
                    (case-insensitive) first_name, then birth_year
        
            See the BooksDataSource comment for a description of how an author is represented.
        '''
        found_authors = self.author_list
        if(book_id != None):
            found_authors = self.authors_for_book(book_id)

        if(search_text != None):
            author_index = 0
            while(author_index < len(found_authors)):
                if(search_text.lower() not in found_authors[author_index].get("last_name").lower()
                    and search_text.lower() not in found_authors[author_index].get("first_name").lower()):
                    found_authors.remove(found_authors[author_index])
                    author_index-= 1
                author_index += 1


        if (start_year != None):
            author_index = 0
            while(author_index < len(found_authors)):
                if(found_authors[author_index].get("death_year") != "NULL" and 
                	found_authors[author_index].get("death_year") < start_year):
                    found_authors.remove(found_authors[author_index])
                    author_index -= 1
                author_index += 1

        if (end_year != None):
            author_index = 0
            while(author_index < len(found_authors)):
                if(found_authors[author_index].get("birth_year") > end_year):
                	found_authors.remove(found_authors[author_index])
                	author_index -= 1
                author_index += 1


        if sort_by != "birth_year":
            found_authors = sorted(found_authors, key = lambda k: k["birth_year"])
            found_authors = sorted(found_authors, key = lambda k: k["first_name"])
            found_authors = sorted(found_authors, key = lambda k: k["last_name"])

        if sort_by == "year":
            found_authors = sorted(found_authors, key = lambda k: k["first_name"])
            found_authors = sorted(found_authors, key = lambda k: k["last_name"])
            found_authors = sorted(found_authors, key = lambda k: k["birth_year"])

        return found_authors



    # Note for my students: The following two methods provide no new functionality beyond
    # what the books(...) and authors(...) methods already provide. But they do represent a
    # category of methods known as "convenience methods". That is, they provide very simple
    # interfaces for a couple very common operations.
    #
    # A question for you: do you think it's worth creating and then maintaining these
    # particular convenience methods? Is books_for_author(17) better than books(author_id=17)?

    def books_for_author(self, author_id):
        ''' Returns a list of all the books written by the author with the specified author ID.
            See the BooksDataSource comment for a description of how an book is represented. '''
        authors_works = []
        for match in self.match_list:
            if match.get("author_id") == author_id:
                authors_works.append(self.book(match.get("book_id")))


        return authors_works

    def authors_for_book(self, book_id):
        ''' Returns a list of all the authors of the book with the specified book ID.
            See the BooksDataSource comment for a description of how an author is represented. '''

        books_contributors = []
        for match in self.match_list:
            if match.get("book_id") == book_id:
                books_contributors.append(self.author(match.get("author_id")))
        return books_contributors




def main():
    test_book_list = BooksDataSource("books.csv", "authors.csv", "books_authors.csv")

    print(test_book_list.books(author_id = 6))







if __name__ == "__main__":
    main()

