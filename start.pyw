import gui
import search
import logging

def setLogger():
	logging.basicConfig(level=logging.INFO,
		format='[%(levelname)s]: %(funcName)s em %(module)s.py - %(message)s')

def main():
	setLogger()
	if search.API_KEY == '':
		logging.warning('nenhuma chave de api encontrada')
	gui.main()
	logging.info('finalizado')

main()
