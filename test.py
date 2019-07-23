import json
import requests

def redditRequest(limit):
	while True:
		requisicao = requests.get(
			'https://api.reddit.com/controversial?limit=' + str(limit))
		if requisicao.status_code == 200:
			break
		else: print('tentando novamente...')

	posts = json.loads(requisicao.content)
	listaPosts = []
	for data in posts['data']['children']:
		listaPosts.append((data['data']['ups'],
			data['data']['downs'], data['data']['permalink']))

	return listaPosts

if __name__ == '__main__':
	lista = redditRequest(20)
	for n in lista:
		print(n)
	print('estes são foram os posts', end='\n\n\n')
	scores = []
	for n in lista:
		scores.append(( n[0] + (n[1] * 2), n[2] ))

	maior = (0, 'link')
	for n in scores:
		if n[0] > maior[0]:
			maior = n

	print('Este é o que tem mais upvotes segundo a fórmula')
	print(maior)