# -*- coding: utf-8 -*-
import byb_modules as BYB
import koding
import sys
import xbmcplugin
from resources import settings
from resources.lib.modules import paths
from resources.lib.scrapers import arconaitv


scraper = arconaitv.arconaitv()

def index():
	RunScrapers()
	for results in scraper.sources:
		title = results.get('Name','Name Missing')
		title = title.encode('utf-8')
		playlink = results.get('playlink','')
		icon = results.get('img',paths.icon)
		BYB.addDir_file(title,playlink,110,icon,paths.fanart,'','','','')






def RunScrapers():
	scraper.actvrand()
	scraper.arcontv()

