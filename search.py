import api_vagalume as api
import logging as log

API_KEY = ''

def searchRoutine(keyWords):
	log.info(f'busca por "{keyWords}"')

	search = list()
	searchArt = api.search(keyWords, 0, API_KEY)
	searchExcerpt = api.search(keyWords, 1, API_KEY)
	searchArtmus = api.search(keyWords, 2, API_KEY)
	#searchAlb = api.search(keyWords, 3, API_KEY) # Busca por álbum

	if searchArt: search.extend(searchArt)
	else: search = None
	if searchExcerpt: search.extend(searchExcerpt)
	else: search = None
	if searchArtmus: search.extend(searchArtmus)
	else: search = None
	#if searchAlb: search.extend(searchAlb)
	#else: search = None

	if search == []:
		log.info('a busca não retornou resultados')
		return search
	elif not search:
		log.info('problema de conexão')
		return search
	else:
		search = _removeDuplicates(search)
		return search

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
		log.info('em cache')
		return _toHTML(song, 'song')
	else:
		song = docObj.expand(API_KEY)
		if song:
			_toCache(song)
			song = _toHTML(song, 'song')
			return song
		else:
			return None

def _getArtist(docObj):
	art = _checkCache(docObj)
	if art:
		log.info('em cache')
		return _toHTML(art, 'artist')
	else:
		art = docObj.expand(API_KEY)
		if art:
			_toCache(art)
			art = _toHTML(art, 'artist')
			return art
		else:
			return None

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
