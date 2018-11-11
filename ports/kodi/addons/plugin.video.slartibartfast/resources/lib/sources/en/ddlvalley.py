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

import re,urllib,urlparse,time,datetime

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import cfscrape
from resources.lib.modules import dom_parser2
from resources.lib.modules import workers

class source:
    def __init__(self):
        self.priority = 1
        self.release = 1
        self.language = ['en']
        self.domains = ['ddlvalley.me','ddlvalley.unblocked.vc']
        self.base_link = 'http://www.ddlvalley.me/'
        self.search_link = '/search/%s/'
        self.search_link1 = '/?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            clean_title = cleantitle.geturl(title).replace('-','+')
            url = urlparse.urljoin(self.base_link, self.search_link % clean_title)
            url = {'url': url, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


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
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        self._sources = []    
        try:
            if url == None: return self._sources
            if debrid.status() == False: raise Exception()

            data = urlparse.parse_qs(url)

            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            self.show  = True if 'tvshowtitle' in data else False
            self.hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            query = '%s' % (data['tvshowtitle']) if\
                'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            
            url = self.search_link % urllib.quote_plus(query)
            ref = urlparse.urljoin(self.base_link, self.search_link1 % urllib.quote_plus(query))
            url = urlparse.urljoin(self.base_link, url)
            self.scraper = cfscrape.create_scraper()
            self.scraper.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
            self.scraper.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
            self.scraper.headers['Referer'] = 'http://www.ddlvalley.me/'
            self.scraper.headers['Host'] = 'www.ddlvalley.me'
            self.scraper.headers['Upgrade-Insecure-Requests'] = '1'
            sess = self.scraper.get(self.base_link)
            self.scraper.headers['Cookie'] = ''
            for key, value in self.scraper.cookies.iteritems(): 
                self.scraper.headers['Cookie'] += '%s=%s;'%(key, value)
            dts = datetime.datetime.utcnow() + datetime.timedelta(days=1)
            self.scraper.headers['Cookie'] += 'noprpkedvhozafiwrcnt=1; noprpkedvhozafiwrexp=%s'%dts.strftime("%a, %d %b %Y %H:%M:%S GMT")
            self.scraper.headers['Referer'] = ref
            r = self.scraper.get(url).content
            u = r
            
            next_page = True
            num = 1
            while next_page:
                try:
                    np = re.findall('<link rel="next" href="([^"]+)', u)[0]
                    u = self.scraper.get(np).content
                    r += u
                except: next_page = False

            items = dom_parser2.parse_dom(r, 'h2')
            items = [dom_parser2.parse_dom(i.content, 'a', req=['href','rel','title','data-wpel-link']) for i in items]
            items = [(i[0].content, i[0].attrs['href']) for i in items]
            items = [(i[0], i[1]) for i in items if cleantitle.get_simple(i[0].split(self.hdlr)[0].lower()) == cleantitle.get_simple(title.lower())]
            threads = []
            for i in items: threads.append(workers.Thread(self._get_sources, i[0], i[1], hostDict, hostprDict))
            for i in threads:
                i.start(); time.sleep(0.5)
            
            alive = [x for x in threads if x.is_alive() == True]
            while alive:
                alive = [x for x in threads if x.is_alive() == True]
                time.sleep(0.5)
            return self._sources
        except:
            return self._sources
            
    def _get_sources(self, name, url, hostDict, hostprDict):
        try:
            hostDict = hostDict + hostprDict
            name = client.replaceHTMLCodes(name)
            r = self.scraper.get(url).content
            links = dom_parser2.parse_dom(r, 'a', req=['href','rel','data-wpel-link','target'])
            links = [i.attrs['href'] for i in links]
            if self.show:
                links = [i for i in links if self.hdlr.lower() in i.lower()]
                
            for url in links:
                try:
                    if self.hdlr in name:
                        fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*)(\.|\)|\]|\s)', '', name.upper())
                        fmt = re.split('\.|\(|\)|\[|\]|\s|\-', fmt)
                        fmt = [i.lower() for i in fmt]

                        if any(i.endswith(('subs', 'sub', 'dubbed', 'dub')) for i in fmt): raise Exception()
                        if any(i in ['extras'] for i in fmt): raise Exception()

                        if '1080p' in fmt: quality = '1080p'
                        elif '720p' in fmt: quality = '720p'
                        else: quality = 'SD'
                        if any(i in ['dvdscr', 'r5', 'r6'] for i in fmt): quality = 'SCR'
                        elif any(i in ['camrip', 'tsrip', 'hdcam', 'hdts', 'dvdcam', 'dvdts', 'cam', 'telesync', 'ts'] for i in fmt): quality = 'CAM'

                        info = []

                        if '3d' in fmt: info.append('3D')

                        try:
                            size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+) (?:GB|GiB|MB|MiB))', name)[-1]
                            div = 1 if size.endswith(('GB', 'GiB')) else 1024
                            size = float(re.sub('[^0-9|/.|/,]', '', size))/div
                            size = '%.2f GB' % size
                            info.append(size)
                        except:
                            pass

                        if any(i in ['hevc', 'h265', 'x265'] for i in fmt): info.append('HEVC')

                        info = ' | '.join(info)

                        if not any(x in url for x in ['.rar', '.zip', '.iso']):
                            url = client.replaceHTMLCodes(url)
                            url = url.encode('utf-8')

                            host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                            host = client.replaceHTMLCodes(host)
                            host = host.encode('utf-8')
                            if host in hostDict:
                                self._sources.append({'source': host, 'quality': quality, 'language': 'en',
                                                      'url': url, 'info': info, 'direct': False, 'debridonly': True})
                except:
                    pass
            check = [i for i in self._sources if not i['quality'] == 'CAM']
            if check: self._sources = check
        except:
            pass
            
    def resolve(self, url):
        return url
