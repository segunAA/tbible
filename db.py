from sqlalchemy import create_engine
from datetime import datetime

class Bible():
	
	reader = create_engine("sqlite:///ampc.sqlite3")

	def __init__(self):
		pass

	def getBook(self, book):
		sql = '''	SELECT osis, human, chapters 
				FROM books 
				WHERE human = '{book}' OR osis='{book}' 
				LIMIT 1
		'''.format(book=book)

		return self.reader.execute(sql).fetchall()[0].osis if len(self.reader.execute(sql).fetchall()) > 0 else False
				

	def getPassage(self, book, verse):
		id = self.getVerseID(book, verse)
		sql = '''	SELECT * FROM verses LIMIT {id}, 10
		'''.format(id=(id-1))

		return self.reader.execute(sql).fetchall()

	def getVerseID(self, book, verse):
		sql = '''	SELECT id FROM verses WHERE book='{book}' AND verse='{verse}'
		'''.format(book=book, verse=verse)
		return self.reader.execute(sql).fetchone().id

	def finder(self, query):
		
		and_expanded = 'AND'.join([" unformatted LIKE '%{}%' ".format(a.strip()) for a in query.split() if len(a) > 3])
		or_expanded = 'OR'.join([" unformatted LIKE '%{}%' ".format(a.strip()) for a in query.split() if len(a) > 3])

		and_sql = "SELECT * FROM verses WHERE {query} ORDER BY id LIMIT 10".format(query=and_expanded)		
		or_sql = "SELECT * FROM verses WHERE {query} ORDER BY id LIMIT 10".format(query=or_expanded)		


		return dict(
					ando=self.reader.execute(and_sql).fetchall(), 
					oro=self.reader.execute(or_sql).fetchall()
		)



class App():

	connector = create_engine("sqlite:///tbible.db")

	def __init__(self):
		sql = '''	CREATE TABLE IF NOT EXISTS 
					cache (
						id INTEGER PRIMARY KEY, 
						created_at TEXT, 
						book TEXT, 
						verse TEXT, 
						success TEXT
		)
		'''
		
		self.connector.execute(sql)

		sql = '''	CREATE TABLE IF NOT EXISTS 
					bookmark (
						id INTEGER PRIMARY KEY, 
						created_at TEXT, 
						book TEXT, 
						verse TEXT
		)
		'''

		self.connector.execute(sql)

	def bookmark(self):
		sql = "SELECT book, verse FROM cache ORDER BY id DESC LIMIT 1"
		memory = self.connector.execute(sql).fetchone()

		#check if book mark exists
		sql = "SELECT id FROM bookmark WHERE book='{book}' AND verse='{verse}'".format(book=memory.book, verse=memory.verse)
		records = self.connector.execute(sql).fetchall()
		recs = len(records)

		if recs == 0:
			sql = "INSERT INTO bookmark (created_at, book, verse) VALUES ('{now}', '{book}', '{verse}')".format(now=datetime.now(), book=memory.book, verse=memory.verse)
			self.connector.execute(sql)

	def getBookmarked(self):
		sql = "SELECT * FROM bookmark ORDER BY id DESC LIMIT 20"
		verses = self.connector.execute(sql).fetchall()
		return verses

	def logger(self, book, verse):
		sql = '''	INSERT INTO cache (created_at, book, verse) 
					VALUES ('{now}', '{book}', '{verse}')
		'''.format(now=datetime.now(), book=book, verse=verse)
		self.connector.execute(sql)

