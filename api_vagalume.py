import json
import requests

API_URL = 'https://api.vagalume.com.br'
API_LIMIT = '&limit=10'

LANGUAGES = [
	'no info',
    'pt-br',
    'en',
    'es',
    'fr',
    'de',
    'it',
    'nl',
    'jp',
    'pt'
]

class Doc():
	def __init__(self, ident = 0, url = '', band = '',
		typeDoc = '', lang = 0, title = ''):
		self.typeDoc = typeDoc
		self.ident = ident
		self.url = url
		self.band = band
		self.lang = lang
		self.title = title

	def expand(self, API_KEY):
		if self.typeDoc == 'song':
			musId = self.ident
			url = API_URL + '/search.php?' + 'musid=' + musId + '&' \
				+ 'apikey=' + API_KEY

			res = _request(url)
			if res == None:
				return res

			name = res['mus'][0]['name']
			artName = res['art']['name']
			url = res['mus'][0]['url']
			lang = res['mus'][0]['lang']
			text = res['mus'][0]['text']

			return Song(name, artName, url, lang, text, musId, res)
		elif self.typeDoc == 'artist':
			artUrl = self.url
			url = API_URL + artUrl + 'index.js'

			res = _request(url)
			if res == None:
				return res

			name = res['artist']['desc']
			imageUrl = res['artist']['pic_medium']

			genres = []
			for n in res['artist']['genre']:
				genres.append(n)
				if len(genres) == 3: break

			topLyrics = []
			for n in res['artist']['toplyrics']['item']:
				topLyrics.append(n)
				if len(topLyrics) == 5: break

			albums = []
			for n in res['artist']['albums']['item']:
				albums.append(n)

			ident = res['artist']['id']

			return Artist(
				ident, artUrl, name, imageUrl,
				genres, topLyrics, albums, res
				)
		elif self.typeDoc == 'album':
			pass
		else:
			return None

	def toString(self):
		stringList = []
		if self.typeDoc == 'artist':
			stringList.append('(art)')
			stringList.append(self.band)

		elif self.typeDoc == 'song':
			stringList.append('(mus)')
			try:
				stringList.append('(%s)' % LANGUAGES[self.lang])
			except IndexError:
				stringList.append('(%s)' % LANGUAGES[0])

			stringList.append(self.title)
			stringList.append(self.band)

		elif self.typeDoc == 'album':
			stringList.append('(alb)')
			stringList.append(self.title)
			stringList.append(self.band)
		return stringList


class Artist():
	def __init__(self, ident, artUrl, name, imageUrl,
		genres, topLyrics, albums, raw):
		self.ident = ident
		self.url = artUrl
		self.name = name
		self.imageUrl = imageUrl
		self.genres = genres
		self.topLyrics = topLyrics
		self.albums = albums
		self.raw = raw

	def toString(self):
		strGenres = []
		for i in self.genres:
			strGenres.append(i['name'])

		strTopLyrics = []
		for i in self.topLyrics:
			strTopLyrics.append(i['desc'])

		strAlbums = []
		for i in self.albums:
			strAlbums.append(i['desc'])

		stringList = [
			self.name,
			self.imageUrl,
			strGenres,
			strTopLyrics,
			strAlbums,
			self.url
		]
		return stringList


class Song():
	def __init__(self, title, artName, url, lang, text, musId, raw):
		self.title = title
		self.artName = artName
		self.url = url
		self.ident = musId
		self.lang = lang
		self.text = text
		self.raw = raw

	def translate(self, langID = 1): # Ainda incompleta
		url = API_URL + '/search.php?' + 'musid=' + self.ident + '&' \
				+ 'apikey=' + API_KEY
		res = _request(url)
		if res == None:
			return
		try:
			translUrl = res['mus'][0]['translate'][0]['url']
			translText = res['mus'][0]['translate'][0]['text']
			#lines = translText.splitlines()
			#translTitle = requests.sub(r'\[|\]|\n', '', lines[0]).strip()

			#self.title = translTitle
			self.url = translUrl
			self.lang = langID
			self.text = translText
		except KeyError:
			print("There's no translation in the choosen language")

	def toString(self):
		print(self.lang)
		stringList = [
			self.title,
			self.artName,
			LANGUAGES[0],
			self.text,
			self.url
			]
		return stringList


def _request(url):
	print(url)
	try:
		api_response = requests.get(url)
		if api_response.status_code == 200:
			return json.loads(api_response.content)
		else:
			print('Cod.: ' + str(r.status_code))
			return None
	except:
		print('Connection error')
		return None

def search(keyWords, searchFor, API_KEY):
	API_SEARCH = [
		'/search.art?', #0
		'/search.excerpt?', #1
		'/search.artmus?', #2
		'/search.alb?' #3
	]
	url = API_URL + API_SEARCH[searchFor] + 'apikey=' + API_KEY \
			+ '&q=' + keyWords + API_LIMIT

	res = _request(url)
	if res == None:
		return res

	if res['response']['numFound'] == 0:
		return []

	docs = []
	if searchFor <= 2:
		for n in res['response']['docs']:
			ident = n['id']
			url = n['url']
			band = n['band']

			try:
				lang = n['langID']
				title = n['title']
				finds = 'song'
				docs.append( Doc(ident, url, band, finds, lang, title) )
			except KeyError:
				finds = 'artist'
				docs.append( Doc(ident, url, band, finds) )
	else:
		for n in res['response']['docs']:
			ident = n['id']
			url = n['url']
			band = n['band']
			title = n['title']
			finds = 'album'
			docs.append(Doc(ident, url, band, finds, title = title))

	return docs
