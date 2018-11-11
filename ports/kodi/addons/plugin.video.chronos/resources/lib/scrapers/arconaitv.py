from BeautifulSoup import BeautifulSoup
from resources.lib.modules.jsunpack import unpack as packets
import re
import requests

class arconaitv():

    sources = []

    def __init__(self):
        self.base_url   = 'http://arconaitv.me/'
        self.index_url  = 'index.php#shows'
        self.random_url = 'stream.php?id=random'
        self.heads      = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'}
        self.referer    = '|Referer=http://arconaitv.me&User-Agent=Mozilla%2F5.0%20(Windows%20NT%206.1%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F59.0.3071.115%20Safari%2F537.36'

    def actvrand(self):
        html3 = requests.get(self.base_url+self.random_url,headers=self.heads).content
        pp    = packets(html3)
        match = re.compile("'https:(.+?)'").findall(pp)
        for plink in match:
            plink = plink.replace('\\','').replace('m3u8/','m3u8')
            src   = 'https:'+plink+self.referer
            img   = ''
        self.sources.append({'Name':'Random Pick','playlink':src,'img':img})




    def arcontv(self):
        html  = BeautifulSoup(requests.get(self.base_url+self.index_url).content)
        conts = html.findAll('div', attrs= {'class':'box-content'})
        for cont in conts:
            links = cont.findAll('a')
            for link in links:
                if link.has_key('href'):
                    href = self.base_url+link['href']
                if link.has_key('title'):
                    name = link['title']
                pics = link.findAll('img')
                for pic in pics:
                    img   = self.base_url+pic['src']
                    html3 = requests.get(href,headers=self.heads).content
                    pp    = packets(html3)
                    match = re.compile("'https:(.+?)'").findall(pp)
                    for plink in match:
                        plink = plink.replace('\\','').replace('m3u8/','m3u8')
                        src   = 'https:'+plink+self.referer
                        self.sources.append({'Name':name,'playlink':src,'img':img})




if __name__ == '__main__':
    arconaitv().arcontv()