# -*- coding: utf-8 -*-

'''
    VistaTV Scraper

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
    thanks to MuadDib, FilmNet, Sirius & the others iv missed
'''


import re,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import dom_parser2
from resources.lib.modules import source_utils

import requests
def url_ok(url):
    r = requests.head(url)
    if r.status_code == 200 or r.status_code == 301:
        return True
    else: return False

def HostChcker():
    if url_ok("https://my-project-free.tv"):
        useurl = 'https://my-project-free.tv/'

    elif url_ok("https://projectfree.unblocked.lol"):
        useurl = 'https://projectfree.unblocked.lol/'

    else: useurl = 'http://localhost/'
    
    return useurl


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['project-free-tv.ch','project-free-tv.ag', 'myprojectfreetv.net']
        self.base_link = HostChcker()
        self.search_link = '/search-tvshows/?free=%s'


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            t = url['tvshowtitle']
            query = t + ' Season ' + season
            url = self.search_link % (cleantitle.geturl(query).replace('-','%20'))
            q = urlparse.urljoin(self.base_link, url)
            print q
            r = client.request(q)
            r = dom_parser2.parse_dom(r, 'tr')
            r = dom_parser2.parse_dom(r, 'a', req='href')
            r = [(i.attrs['href'], i.content.lower()) for i in r if i]
            r = [i[0] for i in r if cleantitle.get(i[1].split('season')[0]) == cleantitle.get(t)]
            link = r[0]

            #episode/the-walking-dead-season-8-episode-6/
            link = link[:-1] if link.endswith('/') else link
            t = link.split('/')[-1]
            url = '/episode/' + t + '-episode-%d/' % int(episode)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)
            print url

            r = client.request(url)
            links = re.findall('''<td><a href=['"](.+?)['"].+?rel="nofollow"><img.+?['"]>(.+?)</a>''', r, re.DOTALL)
            print links

            for i in links:
                print i
                try:
                    url = urlparse.urljoin(self.base_link, i[0])
                    if not 'watch' in url: continue

                    quality = 'SD'
                    valid, host = source_utils.is_host_valid(i[1].replace('&nbsp;\r\n',''), hostDict)
                    if not valid: continue

                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        if 'watch' in url:
            url = client.request(url)
            url = client.parseDOM(url, 'IFRAME', ret='SRC')[0]

        return url


