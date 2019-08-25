import api_vagalume as api

API_KEY = ''

def searchRoutine(keyWords):
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

def viewerRoutine(docObj):
	if docObj.typeDoc == 'song':
		html = _getSong(docObj)
	elif docObj.typeDoc == 'artist':
		html = _getArtist(docObj)
	else:
		pass # reservado para o caso álbum

	return html

# Daqui para baixo ainda não está terminado
def _removeDuplicates(docsList):
	return docsList

def _getSong(docObj):
	song = _checkCache(docObj)
	if song:
		return _toHTML(song, 'song')
	else:
		song = docObj.expand(API_KEY)
		_toCache(song)
		song = _toHTML(song, 'song')
		return song

def _getArtist(docObj):
	art = _checkCache(docObj)
	if art:
		return _toHTML(art, 'artist')
	else:
		art = docObj.expand(API_KEY)
		_toCache(art)
		art = _toHTML(art, 'artist')
		return art

def _getAlbum(docObj):
	pass

def _toHTML(obj, objType):
	if objType == 'song':
		with open('html/templateSong.html', 'r') as file:
			templateHTML = file.read()

		stringList = obj.toString()
		stringList[3] = stringList[3].replace('\n', '<br>')
		newHTML = templateHTML.format(
			stringList[0],
			stringList[1],
			stringList[2],
			stringList[3],
			stringList[4]
			)
	elif objType == 'artist':
		with open('html/templateArtist.html', 'r', encoding="utf8") as file:
			templateHTML = file.read()
	
		stringList = obj.toString()
		
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
	else:
		pass

	return newHTML

def _toCache(obj):
	pass

def _checkCache(docObj):
	return None
