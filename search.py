import logging as log
from threading import Thread

from pubsub import pub
from wx import CallAfter

import api_vagalume as api

API_KEY = ''

_openedDoc = None
_openedHtml = None
_openedSearch = None


class ThreadSearch(Thread):

    def __init__(self, words):
        Thread.__init__(self)
        self.setDaemon(True)
        self.words = words
        self.start()

    def run(self):
        docs = searchRoutine(self.words)
        if docs and docs != []:
            CallAfter(pub.sendMessage, 'docsPanel', docs=docs)
            CallAfter(pub.sendMessage, 'statusBarMsg', text='Tudo pronto!')
        elif docs == []:
            CallAfter(pub.sendMessage,
                'statusBarMsg', text='Nada Encontrado')
        else:
            CallAfter(pub.sendMessage,
                'statusBarMsg', text='Erro de conexão')

        CallAfter(pub.sendMessage, 'panelState', enable=True)


class ThreadRequest(Thread):
    
    def __init__(self, index):
        Thread.__init__(self)
        self.setDaemon(True)
        self.index = index
        self.start()

    def run(self):
        htmlDoc = viewerRoutine(_openedSearch[self.index])
        if htmlDoc:
            CallAfter(pub.sendMessage, 'viewPanel', htmlDoc=htmlDoc)
            CallAfter(pub.sendMessage, 'statusBarMsg', text='Tudo pronto!')
        else:
            CallAfter(pub.sendMessage,
                'statusBarMsg', text='Erro de conexão')

        CallAfter(pub.sendMessage, 'panelState', enable=True)


def searchRoutine(keyWords):
    log.info(f'busca por "{keyWords}"')

    search = api.search(keyWords, API_KEY)

    if search is None:
        log.info('problema de conexão')
        return None
    elif not search:
        log.info('a busca não retornou resultados')
        _toGlobal(search=[])
        return []
    else:
        _toGlobal(search=search)
        return search

def viewerRoutine(docSearch):
    if isinstance(docSearch, api.DocAlb):
        return None

    doc = _get(docSearch)
    html = _toHTML(doc)
    return html

def translateRoutine():
    if _openedDoc is None or isinstance(_openedDoc, api.Band):
        pub.sendMessage('statusBarMsg', text='Escolha uma música.')
        log.info('o objeto é nulo ou não é do tipo Song')
        return

    if _openedDoc.translate():
        html = _toHTML(_openedDoc)
        pub.sendMessage('viewPanel', htmlDoc=html)
    else:
        pub.sendMessage('statusBarMsg', text='Tradução indisponível')

# Daqui para baixo ainda não está terminado
def _get(docSearch):
    doc = _checkCache(docSearch)
    if doc:
        log.info('em cache')
        _toGlobal(doc=doc)
        return doc
    else:
        doc = docSearch.expand(API_KEY)
        if doc:
            _toCache(doc)
            _toGlobal(doc=doc)
            return doc
        else:
            return None

def _toHTML(obj):
    if isinstance(obj, api.Song):
        with open('html/templateSong.html', 'r', encoding="utf8") as file:
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
    elif isinstance(obj, api.Band):
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
        log.info('não implementado')
        return None

    _toGlobal(html=newHTML)
    return newHTML

def _toCache(obj):
    pass

def _checkCache(doc):
    return None

def _toGlobal(doc = None, html = None, search = None):
    global _openedDoc
    global _openedHtml
    global _openedSearch

    if doc is not None: _openedDoc = doc
    if html is not None: _openedHtml = html
    if search is not None: _openedSearch = search

def openedDoc():
    return _openedDoc

def openedSearch():
    return _openedSearch

def openedHtml():
    return _openedHtml