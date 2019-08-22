import api_vagalume as api

API_KEY = ''

def searchDocs(keyWords):
	search = list()
	search.extend( api.search(keyWords, 0, API_KEY) )
	search.extend( api.search(keyWords, 1, API_KEY) )
	search.extend( api.search(keyWords, 2, API_KEY) )
	#search.extend( api.search(keyWords, 3, API_KEY) ) # Busca por álbum

	if search and search != []:
		search = _removeDuplicates(search)
		return search
	else:
		return None

# Daqui para baixo ainda não está terminado
def _removeDuplicates(docsList):
	return docsList

def _getSong(docObj):
	song = _checkCache(docObj)
	if song:
		return song
	else:
		song = docObj.expand(API_KEY)
		song = toHTML(song)
		_toCache(song)
		return song

def _getArtist(docObj):
	art = isCached(docObj)
	if art:
		return art
	else:
		art = docObj.expand(API_KEY)
		art = toHTML(art)
		_toCache(art)
		return art

def _toHTML(obj):
	if type(obj) == type( api.Song() ):
		with open('html/templateSong.html', 'r') as file:
			templateHTML = file.read()

		stringList = obj.toString()
		stringList[3] = text.replace('\n', '<br>')
		newHTML = templateHTML.format(
			stringList[0],
			stringList[1],
			stringList[2],
			stringList[3],
			stringList[4]
			)
	else:
		with open('html/templateArtist.html', 'r', encoding="utf8") as file:
			templateHTML = file.read()
	
		stringList = art.toString()
		
		genres = str()
		for i in stringList[2]:
			string = i + '<br>'
			genres += string

		topLyrics = str()
		for i in stringList[3]:
			string = i + '<br>'
			topLyrics += string

		albums = str()
		for i in stringList[4]:
			string = i + '<br>'
			albums += string

		newHTML = templateHTML.format(
			stringList[0],
			stringList[1],
			genres,
			topLyrics,
			albums,
			stringList[5]
		)

	toCache(newHTML, obj)

	return newHTML

def _toCache(html, obj):
	with open('html/' + obj.ident + '.html', 'w', encoding='utf-8') as file:
		file.write(html)

def _checkCache(docObj):
	return None

def viewerRoutine(docObj):
	pass
