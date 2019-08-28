import logging as log

from pubsub import pub

import api_vagalume as api

API_KEY = ''

_openedDoc = None
_openedHtml = None
_openedSearch = None

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
    if html is not None: _openedHtml = doc
    if search is not None: _openedSearch = search
