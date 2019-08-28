import api_vagalume as api
import logging as log

API_KEY = ''

def searchRoutine(keyWords):
    log.info(f'busca por "{keyWords}"')

    search = api.search(keyWords, API_KEY)

    if search is None:
        log.info('problema de conexão')
        return None
    elif not search:
        log.info('a busca não retornou resultados')
        return []
    else:
        return search

def viewerRoutine(docSearch):
    if isinstance(docSearch, api.DocAlb):
        return None

    doc = _get(docSearch)
    html = _toHTML(doc)
    return html

# Daqui para baixo ainda não está terminado
def _get(docSearch):
    doc = _checkCache(docSearch)
    if doc:
        log.info('em cache')
        return doc
    else:
        doc = docSearch.expand(API_KEY)
        if doc:
            _toCache(doc)
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

    return newHTML

def _toCache(obj):
    pass

def _checkCache(doc):
    return None
