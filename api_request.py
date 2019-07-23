import json
import requests

api_key = 'apikey=' # Insira aqui sua api_key
api_url = 'https://api.vagalume.com.br/search.'


'''
Parâmetros:
	keyWords: palavras-chave inseridas pelo usuário.
	filterNum: define o filtro a ser usado na pesquisa;
	os filtros possíveis estão na lista "api_search".

Retorno:
	Objeto dicionário com os dados obtidos pela API.
'''
def search(keyWords, filterNum):
	api_search = ['art?', 'excerpt?', 'artmus?', 'alb?']
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
	musid: é o identificador da música a ser encontrada.

Retorno:
	Objeto tipo dicionário contendo a letra e informações
	básicas sobre a faixa.

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
	url = api_url + 'php?musid=' + musId + '&' + api_key

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


if __name__ == '__main__':
	print('Testando...')

	keyWords = input()
	filterWord = int(input())

	busca = search(keyWords, filterWord)
	resultados = listSearchResults(busca)
	lyric = returnMusic(resultados[0]['id'])

	print(lyric['textOriginal'])

	try:
		print('\n\n\n\n\n' + lyric['musicTextTransl'])
	except KeyError:
		print('\n\n\nNão há tradução disponível')

'''
Lembretes:
	Criar condições para cada código http;
	Receber outros dados, como discografia e imagens;
'''
