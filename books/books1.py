import csv
import sys
class Books:

	def __init__(self):
		pass
	def GetAuthor(self, FileName, SortDirection):
		authorList = []
		with open(FileName, 'r', newline = '') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				newAuthor = []
				fullAuthor = str(row[2])
				newAuthor.append(fullAuthor)

				prevChar = 'a'
				authorLastName = ""
				authorName = ""
				for char in fullAuthor:
					if char == '(':
						newAuthor.append(authorLastName)
						if (authorName[:-1], authorLastName[:-1]) not in authorList:
							authorList.append((authorName[:-1], authorLastName[:-1]))
						newAuthor[0] = fullAuthor
						authorLastName = ""

					
					if prevChar == ' ':
						authorLastName = char
					else:
						authorLastName = authorLastName + char
					authorName = authorName + char
					prevChar = char
					if char == ")":
						authorName = ""
						authorLastName = ""
					if authorName == " and ":
						authorName = ""
		
		if SortDirection == "reverse":
			authorList.sort( reverse = True)
			print(sorted(authorList , key = lambda authorList: authorList[1] , reverse = True))
		else:
			authorList.sort()
			print(sorted(authorList , key = lambda authorList: authorList[1]))





	def GetTitle(self, FileName, SortDirection):
		TitleList = []
		with open(FileName, 'r', newline = '') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				TitleList.append(row[0])
		if SortDirection == "reverse":
			print(sorted((TitleList) , reverse =True))
		else:
			print(sorted(TitleList))




def main():


	if len(sys.argv) == 4:
		FileName = sys.argv[1]
		action = sys.argv[2]
		SortDirection = sys.argv[3]
	elif len(sys.argv) == 3:
		FileName = sys.argv[1]
		action = sys.argv[2]
		SortDirection = "forward"
	else:
		print("Bad number of args")
		quit()


	ourbook = Books()

	ourbook.GetAuthor(FileName, SortDirection)







if __name__ == "__main__":
	main()