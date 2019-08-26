import json
import requests
import logging as log

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

class DocBand():

    def __init__(self, id_, url, band):
        self.id_ = id_
        self.url = url
        self.band = band

    def expand(self, API_KEY):
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

        return Band(
            ident, artUrl, name, imageUrl,
            genres, topLyrics, albums, res
            )

    def toString(self):
        stringList = []
        stringList.append('(art)')
        stringList.append(self.band)
        return stringList


class DocSong():

    def __init__(self, id_, url, band, title, lang):
        self.id_ = id_
        self.url = url
        self.band = band
        self.title = title
        self.lang = lang

    def expand(self, API_KEY):
        musId = self.id_
        res = _request(
            API_URL
            + '/search.php?'
            + 'musid='
            + musId
            + '&' \
            + 'apikey='
            + API_KEY
            )
        if res == None:
            return res

        name = res['mus'][0]['name']
        artName = res['art']['name']
        url = res['mus'][0]['url']
        lang = res['mus'][0]['lang']
        text = res['mus'][0]['text']

        if lang > 9: lang = 0

        return Song(name, artName, url, lang, text, musId, res)

    def toString(self):
        stringList = []
        stringList.append('(mus)')
        stringList.append('(%s)' % LANGUAGES[self.lang])
        stringList.append(self.title)
        stringList.append(self.band)
        return stringList


class DocAlb():

    def __init__(self, id_, url, band, title):
        self.id_ = id_
        self.url = url
        self.band = band
        self.title = title

    def expand(self, API_KEY):
        log.info('not implemented')
        return Album()

    def toString(self):
        stringList = []
        stringList.append('(alb)')
        stringList.append(self.title)
        stringList.append(self.band)
        return stringList


class Song:

    def __init__(self, title, artName, url, lang, text, musId, raw):
        self.title = title
        self.artName = artName
        self.url = url
        self.ident = musId
        self.lang = lang
        self.text = text
        self.raw = raw

    def translate(self, langID = 1):
        if self.raw['mus'][0].get('translate'):
            for raw in self.raw['mus'][0]['translate']:
                if raw.get('lang') == langID:
                    translUrl = raw.get('url')
                    translText = raw.get('text')
                    self.url = translUrl
                    self.lang = langID
                    self.text = translText
                    return
            
        log.info("There's no translation in the choosen language")

    def toString(self):
        print(self.lang)
        stringList = [
            self.title,
            self.artName,
            LANGUAGES[self.lang],
            self.text,
            self.url
            ]
        return stringList


class Band:

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


class Album:
    def __init__(self):
        pass

    def toString(self):
        return 'not implemented'


def _request(url):
    log.info('URL: ' + url)
    try:
        api_response = requests.get(url)
        if api_response.status_code == 200:
            return json.loads(api_response.content)
        else:
            log.error('Cod.: ' + str(r.status_code))
            return None
    except:
        log.error('Connection error')
        return None

def _docsFactory(res):
    docs = []
    for res in res:
        if res['response']['numFound'] == 0:
            continue
            
        for dict_ in res['response']['docs']:
            id_ = dict_.get('id')
            url = dict_.get('url')
            band = dict_.get('band')
            title = dict_.get('title')
            lang = dict_.get('langID')

            if title and lang:
                if lang > 9: lang = 0
                docs.append(DocSong(id_, url, band, title, lang))
            elif title:
                docs.append(DocAlb(id_, url, band, title))
            else:
                docs.append(DocBand(id_, url, band))
    return docs

def search(keyWords, API_KEY):
    API_SEARCH = [
        '/search.excerpt?',
        '/search.art?',
        #'/search.artmus?',
        '/search.alb?'
    ]
    res = list()
    for i in range(3):
        dict_ = _request(
            API_URL
            + API_SEARCH[i]
            + 'apikey='
            + API_KEY
            + '&q='
            + keyWords
            + API_LIMIT
            )

        if dict_:
            res.append(dict_)
    
    if not res:
        return None
    else:
        return _docsFactory(res)
