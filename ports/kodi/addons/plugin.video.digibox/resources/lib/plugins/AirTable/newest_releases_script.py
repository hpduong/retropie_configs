"""
    air_channels_script.py --- writes a local Newest releases xml
    Copyright (C) 2018, TonyH

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

"""




import requests,re
import json
import airtable
from airtable.airtable import Airtable
from airtable import airtable


open('newest_releases.xml','w')

def Pull_info():
    try:
        at = Airtable('app4O4BNC5yEy9wNa', 'Newest_releases', api_key='keyOHaxsTGzHU9EEh')
        match = at.get_all(maxRecords=700, sort=['title'])
        results = re.compile("link5': u'(.+?)'.+?link4': u'(.+?)'.+?link1': u'(.+?)'.+?link3': u'(.+?)'.+?link2': u'(.+?)'.+?title': u'(.+?)'.+?year': u'(.+?)'",re.DOTALL).findall(str(match))
        for link5,link4,link1,link3,link2,title,year in results:
            if "-*-" in link5:
                link5 = link5.replace("-*-","")
            if "-*-" in link4:
                link4 = link4.replace("-*-","")
            if "-*-" in link3:
                link3 = link3.replace("-*-","")
            if "-*-" in link2:
                link2 = link2.replace("-*-","")

            (thumbnail, fanart, imdb, summary) = pull_tmdb(title,year)           
            print_xml(link5,link4,link1,link3,link2,title,year,imdb,summary,fanart,thumbnail)

    except:pass


def print_xml(link5,link4,link1,link3,link2,title,year,imdb,summary,fanart,thumbnail):
    try:

        f = open('newest_releases.xml','a')
        f.write('<item>\n')
        f.write('\t<title>%s</title>\n' % title)
        f.write('\t<meta>\n')
        f.write('\t\t<contant>movie</content>\n')
        f.write('\t\t<imdb>%s</imdb>\n' % imdb)
        f.write('\t\t<title>%s</title>\n' % title)
        f.write('\t\t<year>%s</year>\n' % year)
        f.write('\t\t<thumbnail>%s</thumbnail>\n' % thumbnail)
        f.write('\t\t<fanart>%s</fanart>\n' % fanart)
        f.write('\t\t<summary>%s</summary>\n' % summary)
        f.write('\t</meta>\n')
        f.write('\t<link>\n')
        f.write('\t\t<sublink>%s</sublink>\n' % link1)
        f.write('\t\t<sublink>%s</sublink>\n' % link2)
        f.write('\t\t<sublink>%s</sublink>\n' % link3)
        f.write('\t\t<sublink>%s</sublink>\n' % link4)
        f.write('\t\t<sublink>%s</sublink>\n' % link5)
        f.write('\t\t<sublink>search</sublink>\n')
        f.write('\t\t<sublink>searchsd</sublink>\n')
        f.write('\t</link>\n')
        f.write('</item>\n')
        f.close()

    except:pass

def pull_tmdb(title,year):
    try:
        search_title = title.replace(" ", "%20")
        url = 'https://api.themoviedb.org/3/search/movie?api_key=586aa0e416c8d3350aee09a2ebc178ac&language=en-US&query=%s&page=1&include_adult=false&primary_release_year=%s' % (search_title, year)
        html = requests.get(url).content
        match = json.loads(html)
        result = (match['results'])
        page = (result[0])
        number = (page['id'])
        url3 = 'https://api.themoviedb.org/3/movie/%s?api_key=586aa0e416c8d3350aee09a2ebc178ac&language=en-US' % number
        html3 = requests.get(url3).content
        match3 = json.loads(html3)
        thumbnail = (match3['poster_path'])
        fanart = (match3['backdrop_path'])
        imdb = (match3['imdb_id'])
        summary = (match3['overview'])
        summary = summary.replace(u"\u2018", "'").replace(u"\u2019", "'")
        summary = summary.encode('utf8')
        thumbnail = "https://image.tmdb.org/t/p/original"+str(thumbnail)
        fanart = "https://image.tmdb.org/t/p/original"+str(fanart)
        return thumbnail,fanart,imdb,summary

    except:
        return "","","",""


Pull_info()


