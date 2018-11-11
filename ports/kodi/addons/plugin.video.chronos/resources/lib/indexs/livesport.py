import byb_modules as BYB
import koding
import sys
import xbmcplugin
from resources import settings
from resources.lib.modules import paths




def livesport_index():
	BYB.addDir('[COLOR gold]Scrapers[/COLOR]','',106,paths.icon,paths.fanart,'','','','')
	BYB.addDir('[COLOR gold]Direct Links[/COLOR]','',107,paths.icon,paths.fanart,'','','','')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def livesport_scrape_dir():
	from resources.lib.scrapers import streamshunter
	streamshunter = streamshunter.streamshunter()
	streamshunter.headers_get()
	for results in streamshunter.Dir:
		HeaderName = results.get('header_name','Header Name Missing')
		HeaderUrl = results.get('header_url','')
		if len(HeaderUrl) > 0:
			BYB.addDir('[COLOR aqua]%s[/COLOR]'%HeaderName,HeaderUrl,108,paths.icon,paths.fanart,'','','','')




def livesport_scrape_lists(url):
	from resources.lib.scrapers import streamshunter
	streamshunter = streamshunter.streamshunter()
	streamshunter.getmatch_and_streams(url)
	for results in streamshunter.Events:
		EventTime = results.get('event_time','Event Time Missing')
		EventName = results.get('event_name','Event Name Missing')
		PlayName  = results.get('playname','Link Name Missing')
		PlayLink  = results.get('playlink','')
		if len(PlayLink) > 0:
			FullName = '[COLOR red]%s[/COLOR] |[COLOR aqua] %s[/COLOR] |[COLOR lime] %s[/COLOR]'%(EventTime,EventName,PlayName)
			BYB.addDir_file(FullName,PlayLink,109,paths.icon,paths.fanart,'','','','')








