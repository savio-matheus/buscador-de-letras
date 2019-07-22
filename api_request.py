import json
import requests

api_key = # Insira aqui sua api_key
api_url = 'https://api.vagalume.com.br/search.'

'''
Parâmetros:
	termosPesquisa: palavras-chave inseridas pelo usuário.
	buscaPor: define o filtro a ser usado na pesquisa;
	os filtros possíveis estão na lista "api_search".

Retorno:
	Objeto dicionário com os dados obtidos pela API.
'''
def busca(termosPesquisa, buscaPor): # Lembrete: criar condições para cada código http
	api_search = ['art?', 'excerpt?', 'artmus?', 'alb?']
	api_limit = '&limit=10'

	url = api_url + api_search[buscaPor] + api_key \
		+ '&q=' + termosPesquisa + api_limit

	while True:
		retorno = requests.get(url)
		if retorno.status_code == 200:
			break
		else:
			print('Tentando conexão...')

	retornoDict = json.loads(retorno.content)

	return retornoDict

'''
Parâmetros:
	musid: é o identificador da música a ser encontrada. É
	obtido a partir dos dados retornados pela busca().

Retorno:
	Objeto tipo dicionário contendo a letra e informações
	básica sobre a faixa.
'''
def retornaLetra(musid):
	url = api_url + 'php?musid=' + musid + '&' + api_key

	while True:
		retorno = requests.get(url)
		if retorno.status_code == 200:
			break
		else:
			print('Tentando conexão...')

	retornoDict = json.loads(retorno.content)

	return retornoDict

if __name__ == '__main__':
	print('Testando...')
	print(busca('American Boy', 2))
	print(retornaLetra('l3ade68b8gbe175fa3'))
# https://api.vagalume.com.br/search.php?musid=3ade68b6g4946fda3&apikey={key}