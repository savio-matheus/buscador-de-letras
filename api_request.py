import json
import requests

api_key = 'apikey=' # Insira aqui sua api_key
api_url = 'https://api.vagalume.com.br'


'''
Parâmetros:
	keyWords: palavras-chave inseridas pelo usuário.
	filterNum: define o filtro a ser usado na pesquisa;
	os filtros possíveis estão na lista "api_search".
	(Por enquanto, a busca por álbuns não funciona).

Retorno:
	Objeto dicionário com os dados obtidos pela API.
'''
def search(keyWords, filterNum):
	api_search = ['/search.art?', '/search.excerpt?',
		'/search.artmus?', '/search.alb?']
	api_limit = '&limit=10'

	url = api_url + api_search[filterNum] + api_key \
		+ '&q=' + keyWords + api_limit

	while True:
		r = requests.get(url)
		if r.status_code == 200:
			break
		else:
			print('Tentando conexão...')

	jsonDict = {'search' : api_search[filterNum]}
	jsonDict = json.loads(r.content)

	# Adiciona uma chave para o tipo de busca realizada.
	# Essa informação será útil para determinar que conteúdo
	# podemos extrair desses dados.
	jsonDict.update( {'searchMode' : api_search[filterNum]} )

	return jsonDict


'''
Parâmetros:
	Objeto dicionário retornado pela search().

Retorno:
	Uma lista contendo os resultados da busca, um
	dicionário para cada.
'''
def listSearchResults(jsonDict):
	results = []
	for i in jsonDict['response']['docs']:
		results.append(i)

	return results


'''
Parâmetros:
	musId ou artName: é o identificador do conteúdo a ser encontrado.

Retorno:
	Objeto tipo dicionário contendo as informações recebidas.

	music = {
		'artist' : artista,
		'artUrl' : url do artista,
		'musicName' : nome da música,
		'musicUrl' : url da música,
		'textOriginal' : letras da música original,
		'musicUrlTransl' : url da música traduzida,
		'musicTextTransl' : letras da música traduzida
	}
'''
def returnMusic(musId):
	url = api_url + '/search.php?musid=' + musId + '&' + api_key

	while True:
		r = requests.get(url)
		if r.status_code == 200:
			break
		else:
			print('Tentando conexão...')

	jsonDict = json.loads(r.content)

	music = {}

	music.update( {'artist' : jsonDict['art']['name']} )
	music.update( {'artUrl' : jsonDict['art']['url']} )
	music.update( {'musicName' : jsonDict['mus'][0]['name']} )
	music.update( {'musicUrl' : jsonDict['mus'][0]['url']} )
	music.update( {'textOriginal' : jsonDict['mus'][0]['text'] } )

	try:
		music.update( {'musicUrlTransl' :
			jsonDict['mus'][0]['translate'][0]['url']} )
		music.update( {'musicTextTransl' :
			jsonDict['mus'][0]['translate'][0]['text']} )
	except KeyError:
		print('Não há tradução disponível')

	return music


'''
Retorno:
	artist = {
		'name' : nome da banda ou artista,
		'imageUrl' : url da imagem (é mesmo é?),
		'genres' : [lista de gêneros musicais];
		'(top)lyrics' : [lista de músicas e suas infos];
		'albums' : [lista de albuns e suas infos].
	}
'''
def returnArtist(artName):
	url = api_url + artName + 'index.js'

	while True:
		r = requests.get(url)
		if r.status_code == 200:
			break
		else:
			print('Tentando conexão...')

	jsonDict = json.loads(r.content)

	artist = {}
	artist.update( {'name' : jsonDict['artist']['desc']} )
	artist.update( {'imageUrl' : jsonDict['artist']['pic_medium']} )

	artist.update( {'genres' : []} )
	for n in jsonDict['artist']['genre']:
		artist['genres'].append( n['name'] )

		if len(artist['genres']) == 5:
			break

	artist.update( {'toplyrics' : []} )
	for n in jsonDict['artist']['toplyrics']['item']:
		artist['toplyrics'].append( {
			'id' : n['id'],
			'name' : n['desc']
			} )

	artist.update( {'lyrics' : []} )
	for n in jsonDict['artist']['lyrics']['item']:
		artist['lyrics'].append( {
			'id' : n['id'],
			'name' : n['desc']
			} )

	artist.update( {'albums' : jsonDict['artist']['albums']['item']} )

	return artist


if __name__ == '__main__':
	print('Nope')

'''
Lembretes:
	Criar condições para cada código http;
	Receber outros dados, como discografia e imagens;
'''
