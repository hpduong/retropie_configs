import koding
import re
import urllib 
import urllib2
from bs4 import BeautifulSoup
import requests



class streamshunter():

	domain = ['streamshunter.tv']
	

	def __init__(self):
		self.base_url = 'http://streamshunter.tv/'
		self.Dir = []
		self.Events = []
		self.PlayLink = []
		self.cookieJar = 'streamshunter'


	def headers_get(self):
		print self.base_url
		html = koding.Open_URL(url=self.base_url,timeout=20,cookiejar=self.cookieJar)
		match =  re.compile('<div class="header-menu-item">.+?<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(html)
		for header_url,header_name in match:
			header_url = header_url.lstrip('/')
			header_url = self.base_url+header_url
			html2 = koding.Open_URL(url=header_url,timeout=20,cookiejar=self.cookieJar)
			if not '<center>There are no events</center>' in html2:
				self.Dir.append({'header_name':header_name,'header_url':header_url})
		print self.Dir
			
	def getmatch_and_streams(self,header_url):
		html = koding.Open_URL(url=header_url,timeout=20,cookiejar=self.cookieJar)
		match = re.compile('<tbody>(.+?)</tbody>',re.DOTALL).findall(html)
		for block in match:
			match2 = re.compile('<tr>(.+?)</div>',re.DOTALL).findall(str(block))
			for block2 in match2:
				match3 = re.compile("<span class='dt.+?>(.+?)</span><h4 id='eventname'><a href=.+?>(.+?)</a></h4>",re.DOTALL).findall(str(block2))
				for event_time,event_name in match3:
					match4 = re.compile("<a href='(http.+?)'.+?>(.+?)</a",re.DOTALL).findall(str(block2))
					for playlink,playname in match4:
						#print event_name,event_time,playname,playlink
						playlink = self.findStream(playlink)
						if playlink != None:
							if playlink not in self.PlayLink:
								self.PlayLink.append(playlink)
								self.Events.append({'event_time':event_time,'event_name':event_name,'playname':playname,'playlink':playlink})
						#print event_time,event_name,playlink,playname
		print self.Events
		koding.dolog('Return from streamshunter scrape=%s %s'%(header_url,self.Events),line_info=True)


	def findStream(self,u):
		try:
			page = requests.get(u).text
			soup = BeautifulSoup(page,"html.parser")
			frames = soup.findAll('iframe')
			streamframe = frames[-1]['src']
			channelNum = None
			if 'hdgameslive.com' in streamframe:
				channelNum = re.findall('\d+',streamframe)
				channelNum = int(channelNum[0]) if channelNum else None
				return self.getMount(channelNum)
		except:
			return None

	def getMount(self,channelNumber):
	    if not channelNumber: return None
	    #print("Mount")
	    fs='http://www.sycamoresports.net/mount/chapo%d/index.m3u8|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'%channelNumber
	    #fs = urllib.quote_plus(fs)
	    return fs




if __name__ == '__main__':
	streamhunter().getmatch_and_streams(header_url='http://streamshunter.tv/soccer')