from db import Bible, App
from ui import UX

ux = UX()
# bible = Bible()
# passage = bible.reader.execute("SELECT * FROM verses LIMIT 10")

cxn = App()

def app():
	# for verse in passage:
	# 	print(verse)
	ux.welcome()
	while True:

		action = input(": ")

		if action == "q": 
			break 
		elif action == 's':
			ux.search()			
		elif action == 'r':
			ux.readVerses()			
		elif action == 'v':
			ux.viewBookmarkedVerses()			
		elif action == 'b':
			ux.bookmarkVerses()			
		elif action == "h": 
			ux.printHelp()
		else:
			ux.printHelp()

if __name__ == "__main__":
	app()