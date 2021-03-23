from db import Bible, App


class UX():

	bible = Bible()
	cxn = App()

	def __init__(self):
		pass

	def welcome(self):
		print("Welcome to the Terminal Bible App!")
		print("==================================\n")


	def readVerses(self):
		book = input("Please select the book you want to read from: ")
		chapter = input("Please select the chapter you want to read from: ")
		verse = input("Please select the verse you want to start from: ")

		book = self.bible.getBook(book)
		verse = "{chapter}.{verse}".format(chapter=chapter, verse=str(verse).zfill(3))


		passage = self.bible.getPassage(book, verse)
		self.cxn.logger(book, verse)

		print("\n")
		for v in passage:
			print(v)

		print("\n")
	
	def bookmarkVerses(self):
		self.cxn.bookmark()

	def viewBookmarkedVerses(self):
		verses = self.cxn.getBookmarked()
		for verse in verses:
			print(verse)

	def search(self):
		query = input("Enter search keyword: ")
		result = self.bible.finder(query)

		for rec in result['ando']:
			print(rec)

		for rec in result['oro']:
			print(rec)

	def printHelp(self):
		apphelp = '''
			Available options:
			==================
			q - to quit
			b - to bookmark the last verse read
			v - to view bookmarked verses
			h - to repeat this message 
			s - to search the bible 
			r - to read verse
			'''
		print(apphelp)