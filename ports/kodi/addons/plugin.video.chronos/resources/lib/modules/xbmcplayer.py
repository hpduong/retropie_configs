import xbmc
import urllib
import koding



class xbmc_player():

	def __init__(self):
		self.f4m = ['.ts','.m3u8','.f4m']
		self.Play = xbmc.Player()
		self.SportdevilToPlay = ('http://sstream.net/','http://mamahd.in','http://cricfree.sc')
		self.f4mToPlay = ('.ts','.m3u8','.f4m')


	def UrlDefine(self,url):
		if not url.startswith('http') and not url.startswith('plugin:'):
			url = 'http:%s'%(url)
		if url.startswith(self.SportdevilToPlay):
			url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+url
		if url.endswith('.ts'):
			url =  'plugin://plugin.video.f4mTester/?url='+urllib.quote_plus(url)+'&amp;streamtype=TSDOWNLOADER'
		if url.endswith('.m3u8'):
			url =  'plugin://plugin.video.f4mTester/?url='+urllib.quote_plus(url)+'&amp;streamtype=HLSRETRY'
		if url.endswith('.f4m'):
			url = 'plugin://plugin.video.f4mTester/?url='+urllib.quote_plus(url)
		if '|' in url and any(x in url for x in self.f4m):
			_url = url.split('|')[0]
			if _url.endswith('.ts'):
				url =  'plugin://plugin.video.f4mTester/?url='+urllib.quote_plus(url)+'&amp;streamtype=TSDOWNLOADER'
			if _url.endswith('.m3u8'):
				url =  'plugin://plugin.video.f4mTester/?url='+urllib.quote_plus(url)+'&amp;streamtype=HLSRETRY'
			if _url.endswith('.f4m'):
				url = 'plugin://plugin.video.f4mTester/?url='+urllib.quote_plus(url)
		else:
			url = url
		koding.dolog('UrlDefine= %s'%url,line_info=True)
		return url

	def PlayMethod(self,url):
		if url.startswith('plugin://plugin'):
			playmethod='plugin'
		elif url.startswith('http'):
			playmethod = 'http'
		else:
			xbmc_executebuiltin.Notify(message='url format not correct',times=5000)
			koding.dolog('url format not correct %s'%url,line_info=True)
			playmethod = 'false'
		koding.dolog('PlayMethod = %s  %s'%(playmethod,url),line_info=True)
		return url,playmethod

	def pluginplay(self,url):
		try:
			xbmc.executebuiltin('XBMC.RunPlugin('+url+')')
		except:pass
		try:
			self.Play.play(url)
		except:pass

	def httpplay(self,url):
		hmf = resolveurl.HostedMediaFile(url)
		koding.dolog('resolveurl HostedMediaFile = %s'%hmf.valid_url(),line_info=True)
		if hmf.valid_url() == True:
			stream_url = hmf.resolve()
		else:
			stream_url=stream_url
		try:
			xbmc.Player().play(stream_url)
		except:
			koding.dolog('httpplay method raised a error url = %s'%stream_url,line_info=True)
			Notification = 'XBMC.Notification(Unable to play via httpplay method,'','',5000)'
			xbmc.executebuiltin(str(Notification))

	def play(self,url):
		url = xbmc_player().UrlDefine(url)
		url,playmethod = xbmc_player().PlayMethod(url)
		if not playmethod == 'false':
			if playmethod == 'plugin':
				koding.dolog('plugin PlayMethod = %s  %s'%(playmethod,url),line_info=True)
				xbmc_player().pluginplay(url)
			elif playmethod == 'http':
				koding.dolog('http PlayMethod = %s  %s'%(playmethod,url),line_info=True)
				xbmc_player().httpplay(url)
			else:
				xbmc_executebuiltin.Notify(message='PlayMethod not correct',times=5000)
				koding.dolog('PlayMethod not correct  %s'%url,line_info=True)
				pass
		else:pass 
