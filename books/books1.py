#Program designed to read CSV files containing book information
#Created by Johnny Reichman and Eric Stadelman for CS 257, Jeff Ondich

import csv
import sys

class Books:

	def __init__(self):
		pass

	#displays list of authors
	def get_author(self, input_file, sort_direction):
		author_list = []
		with open(input_file, 'r', newline = '') as csvfile:
			reader = csv.reader(csvfile)

			#parses through author discriptions to create an array of tuples:
			#each element of the array is of the form [full_name, last_name]
			for row in reader:
				author_description = str(row[2])
				prev_letter = ''
				last_name = ""
				full_name = ""

				for letter in author_description:

					#adds the author to the list, no duplicates
					if letter == '(':
						if (full_name[:-1], 
							last_name[:-1]) not in author_list:
							author_list.append((full_name[:-1], 
												last_name[:-1]))
						last_name = ""

					#resets last_name if a space is encountered
					if prev_letter == ' ':
						last_name = letter
					else:
						last_name = last_name + letter

					full_name = full_name + letter
					if full_name == " and ":
						full_name = ""

					#resets full, last name if ')' is encountered(>1 author)
					if letter == ")":
						full_name = ""
						last_name = ""

					prev_letter = letter

		#sorts and prints the author list					
		if sort_direction == "reverse":
			author_list.sort( reverse = True)
			author_list.sort(key = lambda author_list: author_list[1], 
				reverse = True)
		else:
			author_list.sort()
			author_list.sort(key = lambda author_list: author_list[1])
		
		for author in author_list:
			print(author[0])



	#displays list of book titles
	def get_title(self, input_file, sort_direction):
		title_list = []
		with open(input_file, 'r', newline = '') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				title_list.append(row[0])
		if sort_direction == "reverse":
			title_list.sort(reverse = True)
		else:
			title_list.sort()
		for title in title_list:
			print(title)
			

def main():

	#error check for number of arguments
	if len(sys.argv) == 4:
		input_file = sys.argv[1]
		action = sys.argv[2]
		sort_direction = sys.argv[3]
	elif len(sys.argv) == 3:
		input_file = sys.argv[1]
		action = sys.argv[2]
		sort_direction = "forward"
	else:
		print("Invalid number of arguments", file=sys.stderr)
		quit()

	#error check for sort direction
	if(sort_direction not in ["forward", "reverse"]):
		print("Unknown sort direction: ", sort_direction)
		quit()

	ourbook = Books()

	#displays requested list, along with error check for action
	if(action == "books"):
		ourbook.get_title(input_file, sort_direction)
	elif(action == "authors"):
		ourbook.get_author(input_file, sort_direction)
	else:
		print("Unknown action command: ", action)
		quit()


if __name__ == "__main__":
	main()