import json
import requests

API_KEY = '' # api_key=...
API_URL = 'https://api.vagalume.com.br'
API_LIMIT = '&limit=10'

API_SEARCH = [
	'/search.art?',
	'/search.excerpt?',
	'/search.artmus?',
	'/search.alb?'
]

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
		finds = -1, lang = 'no info', title = ''):
		self.ident = ident
		self.url = url
		self.band = band
		self.lang = lang
		self.title = title
		self.finds = finds

	def search(keyWords, searchFor):
		url = API_URL + API_SEARCH[searchFor] + API_KEY \
				+ '&q=' + keyWords + API_LIMIT
		print(url)

		for n in range(0, 2):
			r = requests.get(url)
			if r.status_code == 200:
				break
			else:
				print('Cod.: ' + str(r.status_code))

		res = json.loads(r.content)

		if res['response']['numFound'] == 0:
			return Doc()

		docs = []
		if searchFor <= 2:
			for n in res['response']['docs']:
				ident = n['id']
				url = n['url']
				band = n['band']

				try:
					lang = n['langID']
					title = n['title']
					finds = 1
					docs.append(Doc(ident, url, band, finds, lang, title))
				except KeyError:
					finds = 0
					docs.append(Doc(ident, url, band, finds))

		else:
			for n in res['response']['docs']:
				ident = n['id']
				url = n['url']
				band = n['band']
				title = n['title']
				finds = 3
				docs.append(Doc(ident, url, band, finds, title = title))

		return docs

	def show(self):
		if self.finds == 0:
			print('Banda/artista: ' + self.band)

		elif self.finds == 1:
			print('Música:' + self.title)
			print('Banda/artista: ' + self.band)
			print('Idioma: ' + self.lang)

		elif self.finds == 3:
			print('Álbum: ' + self.title)
			print('Banda/artista: ' + self.band)

		elif self.finds == -1:
			print('Nada encontrado')

		else:
			print('Falha de conexão')

class Artist():
	def __init__(self, artUrl, name, imageUrl,
		genres, topLyrics, albums):

		self.url = API_URL + artUrl + 'index.js'
		self.name = name
		self.imageUrl = imageUrl
		self.genres = genres
		self.topLyrics = topLyrics
		self.albums = albums

	def find(doc):
		artUrl = doc.url
		url = API_URL + artUrl + 'index.js'

		# Melhore este pedaço
		for n in range(0, 2):
			r = requests.get(url)
			if r.status_code == 200:
				res = json.loads(r.content)
				break
			else:
				print('Cod.: ' + str(r.status_code))

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

		return Artist(
			artUrl, name, imageUrl,
			genres, topLyrics, albums
			)

	def show(self):
		strGenres = []
		for i in self.genres:
			strGenres.append(i['name'])

		strTopLyrics = []
		for i in self.topLyrics:
			strTopLyrics.append(i['desc'])

		strAlbums = []
		for i in self.albums:
			strAlbums.append(i['desc'])

		strGenres = ', '.join(strGenres)
		strTopLyrics = ', '.join(strTopLyrics)
		strAlbums = ', '.join(strAlbums)

		print('Banda/artista: ' + self.name)
		print('Gêneros: ' + strGenres)
		print('Mais procuradas: ' + strTopLyrics)
		print('Álbuns: ' + strAlbums)

class Music():
	def __init__(self, name, artName, url, lang, text, translUrl = '',
		translLang = 0, translText = '', translName = ''):
		
		self.name = name
		self.artName = artName
		self.url = url
		self.lang = lang
		self.text = text
		self.translUrl = translUrl
		self.translLang = translLang
		self.translText = translText
		self.translName = translName

	def find(doc):
		musId = doc.ident
		url = API_URL + '/search.php?' + 'musid=' + musId + '&' + API_KEY 
		print(url)

		for n in range(0, 2):
			r = requests.get(url)
			if r.status_code == 200:
				break
			else:
				print('Cod.: ' + str(r.status_code))

		res = json.loads(r.content)

		name = res['mus'][0]['name']
		artName = res['art']['name']
		url = res['mus'][0]['url']
		lang = res['mus'][0]['lang']
		text = res['mus'][0]['text']
		
		try:
			translUrl = \
				res['mus'][0]['translate'][0]['url']
		except KeyError:
			translUrl = ''
		try:
			translLang = \
				res['mus'][0]['translate'][0]['lang']
		except KeyError:
			translLang = 0
		try:
			translText = \
				res['mus'][0]['translate'][0]['text']
		except KeyError:
			translText = ''
		'''
		try:
			translName = \
				res['mus'][0]['translate'][0]['text'].input()
		except KeyError:
			translName = ''
		'''

		return Music(
			name, artName, url, lang, text, translUrl,
			translLang, translText, translName = ''
			)

	def show(self):
		print(self.name)
		print(self.artName)
		print(self.text)
		print(self.url)

	def showTransl(self):
		print(self.name)
		print(self.artName)
		print(self.translText)
		print(self.translUrl)

if __name__ == '__main__': # para testes
	API_KEY = input("Chave da api: ")

	termos = input('Sua busca: ')
	busca = Doc.search(termos, 1) # Busca por música

	musica = Music.find(busca[0])

	musica.show()
	print('\n\n')
	musica.showTransl()

"""
Lembrete:
 	tratar exceções
 	colocar "r = requests.get(url)" em função separada
 	obter o nome traduzido das músicas
 	buscar todas as traduções se tiver mais de uma (no momento,
 	obtém apenas em português)
"""
