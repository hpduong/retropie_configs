# -*- coding: utf-8 -*-




import os,sys,urlparse

from resources.lib.modules import control
from resources.lib.modules import trakt
from resources.lib.modules import cache
import xbmc
import xbmcaddon
import xbmcgui

sysaddon = sys.argv[0] ; syshandle = int(sys.argv[1]) ; control.moderator()

artPath = control.artPath() ; addonFanart = control.addonFanart()

imdbCredentials = False if control.setting('imdb.user') == '' else True

traktCredentials = trakt.getTraktCredentialsInfo()

traktIndicators = trakt.getTraktIndicatorsInfo()

queueMenu = control.lang(32065).encode('utf-8')

addon_id = 'script.asylum.Greeting'


ADDON = xbmcaddon.Addon(id=addon_id)
		
		
class navigator:
	def root(self):
		if ADDON.getSetting('username')=='true':
			xbmc.executebuiltin('RunAddon("script.asylum.Greeting")')

		self.addDirectoryItem(32001, 'movieNavigator', 'movmain.gif', 'DefaultMovies.jpg')
		self.addDirectoryItem(32002, 'tvNavigator', 'tvshowsmain.gif', 'DefaultTVShows.jpg')
		if not control.setting('lists.widget') == '0':
			self.addDirectoryItem(32003, 'mymovieNavigator', 'movmain.gif', 'DefaultVideoPlaylists.jpg')
			self.addDirectoryItem(32004, 'mytvNavigator', 'tvshowsmain.gif', 'DefaultVideoPlaylists.jpg')

		self.addDirectoryItem(32008, 'toolNavigator', 'tools2.gif', 'DefaultAddonProgram.jpg')

		downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting('movie.download.path'))[0]) > 0 or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
		if downloads == True:
			self.addDirectoryItem(32009, 'downloadNavigator', 'downloads2.gif', 'DefaultFolder.jpg')

		self.addDirectoryItem(32010, 'searchNavigator', 'search2.gif', 'DefaultFolder.jpg')

		self.endDirectory()


	def movies(self, lite=False):
		self.addDirectoryItem('Movie Themes', 'movthemeNavigator', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Top 1000 Movies', 'HRmovieNavigator', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Bottom 1000 Movies', 'bottommoviesNavigator', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('B rated', 'movies&url=brated', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('MMMMMMMMMMMMMMMMM Brains', 'movies&url=zombie', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('anime', 'movies&url=anime', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		#self.addDirectoryItem('Networks 2', 'networks2Navigator', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem(32011, 'movieGenres', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem(32012, 'movieYears', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem(32013, 'moviePersons', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem(32014, 'movieLanguages', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem(32015, 'movieCertificates', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem(32017, 'movies&url=trending', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem(32018, 'movies&url=popular', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem(32019, 'movies&url=views', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem(32020, 'movies&url=boxoffice', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem(32021, 'movies&url=oscars', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem(32022, 'movies&url=theaters', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem(32005, 'movies&url=featured', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('superhero', 'movies&url=superhero', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Stars By Birth Signs', 'Birthsigns', 'signs.gif', 'DefaultTVShows.png')

		
		if lite == False:
			if not control.setting('lists.widget') == '0':
				self.addDirectoryItem(32003, 'mymovieliteNavigator', 'movmain.gif', 'DefaultVideoPlaylists.jpg')

			self.addDirectoryItem('Actor Search', 'moviePerson', 'search2.gif', 'DefaultMovies.jpg')
			self.addDirectoryItem(32010, 'movieSearch', 'search2.gif', 'DefaultMovies.jpg')

		self.endDirectory()



	def mymovies(self, lite=False):
		self.accountCheck()

		if traktCredentials == True and imdbCredentials == True:
			self.addDirectoryItem(32032, 'movies&url=traktcollection', 'movmain.gif', 'DefaultMovies.jpg', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
			self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'movmain.gif', 'DefaultMovies.jpg', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))
			self.addDirectoryItem(32034, 'movies&url=imdbwatchlist', 'movmain.gif', 'DefaultMovies.jpg', queue=True)

		elif traktCredentials == True:
			self.addDirectoryItem(32032, 'movies&url=traktcollection', 'movmain.gif', 'DefaultMovies.jpg', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
			self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'movmain.gif', 'DefaultMovies.jpg', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))

		elif imdbCredentials == True:
			self.addDirectoryItem(32032, 'movies&url=imdbwatchlist', 'movmain.gif', 'DefaultMovies.jpg', queue=True)
			self.addDirectoryItem(32033, 'movies&url=imdbwatchlist2', 'movmain.gif', 'DefaultMovies.jpg', queue=True)

		if traktCredentials == True:
			self.addDirectoryItem(32035, 'movies&url=traktfeatured', 'movmain.gif', 'DefaultMovies.jpg', queue=True)

		elif imdbCredentials == True:
			self.addDirectoryItem(32035, 'movies&url=featured', 'movmain.gif', 'DefaultMovies.jpg', queue=True)

		if traktIndicators == True:
			self.addDirectoryItem(32036, 'movies&url=trakthistory', 'movmain.gif', 'DefaultMovies.jpg', queue=True)

		self.addDirectoryItem(32039, 'movieUserlists', 'movmain.gif', 'DefaultMovies.jpg')

		if lite == False:
			self.addDirectoryItem(32031, 'movieliteNavigator', 'movmain.gif', 'DefaultMovies.jpg')
			self.addDirectoryItem('Actor Search', 'moviePerson', 'search2.gif', 'DefaultMovies.jpg')
			self.addDirectoryItem(32010, 'movieSearch', 'search2.gif', 'DefaultMovies.jpg')

		self.endDirectory()

	def HRrated(self, lite=False):
		self.addDirectoryItem('Action', 'movies&url=Action', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Adventure', 'movies&url=Adventure', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Animation', 'movies&url=Animation', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Comedy', 'movies&url=Comedy', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Crime', 'movies&url=Crime', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Drama', 'movies&url=Drama', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Family', 'movies&url=Family', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Fantasy', 'movies&url=Fantasy', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('History', 'movies&url=History', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Horror', 'movies&url=Horror', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Mystery', 'movies&url=Mystery', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Romance', 'movies&url=Romance', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Science Fiction', 'movies&url=ScienceFiction', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Sport', 'movies&url=Sport', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Thriller', 'movies&url=Thriller', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('War', 'movies&url=War', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Western', 'movies&url=Western', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.endDirectory()

	def bottommovies(self, lite=False):
		self.addDirectoryItem('Action', 'movies&url=Action2', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Adventure', 'movies&url=Adventure2', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Animation', 'movies&url=Animation2', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Comedy', 'movies&url=Comedy2', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Crime', 'movies&url=Crime2', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Drama', 'movies&url=Drama2', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Family', 'movies&url=Family2', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Fantasy', 'movies&url=Fantasy2', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('History', 'movies&url=History2', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Horror', 'movies&url=Horror2', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Mystery', 'movies&url=Mystery2', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Romance', 'movies&url=Romance2', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Science Fiction', 'movies&url=ScienceFiction2', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Sport', 'movies&url=Sport2', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Thriller', 'movies&url=Thriller2', 'movmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('War', 'movies&url=War2', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Western', 'movies&url=Western2', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.endDirectory()

	def networks2(self, lite=False):
		self.addDirectoryItem('fox', 'movies&url=fox', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Sony', 'movies&url=Sony', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('DreamWorks', 'movies&url=DreamWorks', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('MGM', 'movies&url=MGM', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Paramount', 'movies&url=Paramount', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Universal', 'movies&url=Universal', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('disney', 'movies&url=disney', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('warner', 'movies&url=warner', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('IMDb', 'movies&url=IMDb', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Amazon', 'movies&url=Amazon', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')

	def networks2tv(self, lite=False):
		self.addDirectoryItem('fox', 'tvshows&url=fox', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Sony', 'tvshows&url=Sony', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('DreamWorks', 'tvshows&url=DreamWorks', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('MGM', 'tvshows&url=MGM', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Paramount', 'tvshows&url=Paramount', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Universal', 'tvshows&url=Universal', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('disney', 'tvshows&url=disney', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('warner', 'tvshows&url=warner', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('IMDb', 'tvshows&url=IMDb', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Amazon', 'tvshows&url=Amazon', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Amazon Prime', 'tvshows&url=Amazonp', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Without A Box', 'tvshows&url=WithoutABox', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')	
		self.endDirectory()

	def tvshows(self, lite=False):
		self.addDirectoryItem('anime', 'tvshows&url=anime', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Networks 2', 'networks2tvNavigator', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem(32016, 'tvusNetworks', 'tvshowsmain.gif', 'DefaultTVShows.png')
		self.addDirectoryItem('themed out Tv', 'tvthemeNavigator', 'tvshowsmain.gif', 'DefaultTVShows.png')	
	
		self.addDirectoryItem('Top 1000 T.V Shows', 'toptvNavigator', 'tvshowsmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem(32011, 'tvGenres', 'tvshowsmain.gif', 'DefaultTVShows.png')
		self.addDirectoryItem(32014, 'tvLanguages', 'tvshowsmain.gif', 'DefaultTVShows.png')
		self.addDirectoryItem('Stars By Birth Signs', 'Birthsigns', 'signs.gif', 'DefaultTVShows.png')
		self.addDirectoryItem(32015, 'tvCertificates', 'tvshowsmain.gif', 'DefaultTVShows.png')
		self.addDirectoryItem(32017, 'tvshows&url=trending', 'tvshowsmain.gif', 'DefaultRecentlyAddedEpisodes.png')
		self.addDirectoryItem(32018, 'tvshows&url=popular', 'tvshowsmain.gif', 'DefaultTVShows.png')
		self.addDirectoryItem(32023, 'tvshows&url=rating', 'tvshowsmain.gif', 'DefaultTVShows.png')
		self.addDirectoryItem(32019, 'tvshows&url=views', 'tvshowsmain.gif', 'DefaultTVShows.png')
		self.addDirectoryItem(32024, 'tvshows&url=airing', 'tvshowsmain.gif', 'DefaultTVShows.png')
        #self.addDirectoryItem(32025, 'tvshows&url=active', 'returning-tvshows.png', 'DefaultTVShows.png')
		self.addDirectoryItem(32026, 'tvshows&url=premiere', 'tvshowsmain.gif', 'DefaultTVShows.png')
		self.addDirectoryItem(32006, 'calendar&url=added', 'tvshowsmain.gif', 'DefaultRecentlyAddedEpisodes.png', queue=True)
		self.addDirectoryItem(32027, 'calendars', 'tvshowsmain.gif', 'DefaultRecentlyAddedEpisodes.png')
		self.addDirectoryItem('superhero', 'tvshows&url=superhero', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')

		if lite == False:
			if not control.setting('lists.widget') == '0':
				self.addDirectoryItem(32004, 'mytvliteNavigator', 'tvshowsmain.gif', 'DefaultVideoPlaylists.jpg')

			self.addDirectoryItem('Actor Search', 'tvPerson', 'search2.gif', 'DefaultTVShows.jpg')
			self.addDirectoryItem(32010, 'tvSearch', 'search2.gif', 'DefaultTVShows.jpg')

		self.endDirectory()

	def toptvshows(self, lite=False):
		self.addDirectoryItem('Action', 'tvshows&url=Action', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Adventure', 'tvshows&url=Adventure', 'tvshowsmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Animation', 'tvshows&url=Animation', 'tvshowsmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Comedy', 'tvshows&url=Comedy', 'tvshowsmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Crime', 'tvshows&url=Crime', 'tvshowsmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Drama', 'tvshows&url=Drama', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Family', 'tvshows&url=Family', 'tvshowsmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Fantasy', 'tvshows&url=Fantasy', 'tvshowsmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('History', 'tvshows&url=History', 'tvshowsmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Horror', 'tvshows&url=Horror', 'tvshowsmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Horror', 'tvshows&url=', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Mystery', 'tvshows&url=Mystery', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Romance', 'tvshows&url=Romance', 'tvshowsmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Science Fiction', 'tvshows&url=ScienceFiction', 'tvshowsmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Sport', 'tvshows&url=Sport', 'tvshowsmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Thriller', 'tvshows&url=Thriller', 'tvshowsmain.gif', 'DefaultMovies.png')
		self.addDirectoryItem('War', 'tvshows&url=War', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Western', 'tvshows&url=Western', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')

		self.endDirectory()

	def Birthsigns(self, lite=False):
		#self.addDirectoryItem('Aquarius', 'Aquarius', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Pisces', 'Pisces', 'signs.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Aries', 'Aries', 'signs.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Taurus', 'Taurus', 'signs.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Gemini', 'Gemini', 'signs.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Cancer', 'Cancer', 'signs.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Leo', 'Leo', 'signs.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Virgo', 'Virgo', 'signs.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Libra', 'Libra', 'signs.gif', 'DefaultMovies.png')
		self.addDirectoryItem('scorpio', 'scorpio', 'signs.gif', 'DefaultMovies.png')
		self.addDirectoryItem('Sagittarius', 'Sagittarius', 'signs.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('Capricorn', 'Capricorn', 'signs.gif', 'DefaultRecentlyAddedMovies.png')
		self.endDirectory()

	def themes(self):
		self.addDirectoryItem('action hero', 'tvshows&url=actionhero', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('alternate history', 'tvshows&url=alternatehistory', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('ambiguous ending', 'tvshows&url=ambiguousending', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('americana', 'tvshows&url=americana', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('anti hero', 'tvshows&url=antihero', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('avant garde', 'tvshows&url=avantgarde', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('b movie', 'tvshows&url=bmovie', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('bank heist', 'tvshows&url=bankheist', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('based on book', 'tvshows&url=basedonbook', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('based on play', 'tvshows&url=basedonplay', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('based on comic', 'tvshows&url=basedoncomic', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('based on comic book', 'tvshows&url=basedoncomicbook', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('based on novel', 'tvshows&url=basedonnovel', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('based on novella', 'tvshows&url=basedonnovella', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('based on short story', 'tvshows&url=basedonshortstory', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('battle', 'tvshows&url=battle', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('betrayal', 'tvshows&url=betrayal', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('biker', 'tvshows&url=biker', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('black comedy', 'tvshows&url=blackcomedy', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('blockbuster', 'tvshows&url=blockbuster', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('breaking the fourth wall', 'tvshows&url=breakingthefourthwall', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('business', 'tvshows&url=business', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('caper', 'tvshows&url=caper', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('car accident', 'tvshows&url=caraccident', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('car chase', 'tvshows&url=carchase', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('car crash', 'tvshows&url=carcrash', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('character name in title', 'tvshows&url=characternameintitle', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('characters point of view camera shot', 'tvshows&url=characterspointofviewcamerashot', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('chick flick', 'tvshows&url=chickflick', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('coming of age', 'tvshows&url=comingofage', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('competition', 'tvshows&url=competition', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('conspiracy', 'tvshows&url=conspiracy', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('corruption', 'tvshows&url=corruption', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('criminal mainmind', 'tvshows&url=criminalmainmind', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('cult', 'tvshows&url=cult', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('cult film', 'tvshows&url=cultfilm', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('cyberpunk', 'tvshows&url=cyberpunk', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('dark hero', 'tvshows&url=darkhero', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('deus ex machina', 'tvshows&url=deusexmachina', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('dialogue driven', 'tvshows&url=dialoguedriven', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('dialogue driven story', 'tvshows&url=dialoguedrivenstory', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('directed by star', 'tvshows&url=directedbystar', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('director cameo', 'tvshows&url=directorcameo', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('double cross', 'tvshows&url=doublecross', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('dream sequence', 'tvshows&url=dreamsequence', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('dystopia', 'tvshows&url=dystopia', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('ensemble cast', 'tvshows&url=ensemblecast', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('epic', 'tvshows&url=epic', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('espionage', 'tvshows&url=espionage', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('experimental', 'tvshows&url=experimental', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('experimental film', 'tvshows&url=experimentalfilm', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('fairy tale', 'tvshows&url=fairytale', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('famous line', 'tvshows&url=famousline', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('famous opening theme', 'tvshows&url=famousopeningtheme', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('famous score', 'tvshows&url=famousscore', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('fantasy sequence', 'tvshows&url=fantasysequence', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('farce', 'tvshows&url=farce', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('father daughter relationship', 'tvshows&url=fatherdaughterrelationship', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('father son relationship', 'tvshows&url=fathersonrelationship', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('femme fatale', 'tvshows&url=femmefatale', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('fictional biography', 'tvshows&url=fictionalbiography', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('flashback', 'tvshows&url=flashback', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('futuristic', 'tvshows&url=futuristic', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('good versus evil', 'tvshows&url=goodversusevil', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('heist', 'tvshows&url=heist', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('hero', 'tvshows&url=hero', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('high school', 'tvshows&url=highschool', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('husband wife relationship', 'tvshows&url=husbandwiferelationship', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('idealism', 'tvshows&url=idealism', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('independent film', 'tvshows&url=independentfilm', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('investigation', 'tvshows&url=investigation', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('kidnapping', 'tvshows&url=kidnapping', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('knight', 'tvshows&url=knight', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('kung fu', 'tvshows&url=kungfu', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('macguffin', 'tvshows&url=macguffin', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('medieval times', 'tvshows&url=medievaltimes', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('mockumentary', 'tvshows&url=mockumentary', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('monster', 'tvshows&url=monster', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('mother daughter relationship', 'tvshows&url=motherdaughterrelationship', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('mother son relationship', 'tvshows&url=mothersonrelationship', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('multiple actors playing same role', 'tvshows&url=multipleactorsplayingsamerole', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('multiple endings', 'tvshows&url=multipleendings', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('multiple perspectives', 'tvshows&url=multipleperspectives', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('multiple storyline', 'tvshows&url=multiplestoryline', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('multiple time frames', 'tvshows&url=multipletimeframes', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('murder', 'tvshows&url=murder', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('musical number', 'tvshows&url=musicalnumber', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('neo noir', 'tvshows&url=neonoir', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('neorealism', 'tvshows&url=neorealism', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('ninja', 'tvshows&url=ninja', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('no background score', 'tvshows&url=nobackgroundscore', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('no music', 'tvshows&url=nomusic', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('no opening credits', 'tvshows&url=noopeningcredits', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('no title at beginning', 'tvshows&url=notitleatbeginning', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('nonlinear timeline', 'tvshows&url=nonlineartimeline', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('on the run', 'tvshows&url=ontherun', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('one against many', 'tvshows&url=oneagainstmany', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('one man army', 'tvshows&url=onemanarmy', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('opening action scene', 'tvshows&url=openingactionscene', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('organized crime', 'tvshows&url=organizedcrime', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('parenthood', 'tvshows&url=parenthood', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('parody', 'tvshows&url=parody', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('plot twist', 'tvshows&url=plottwist', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('police corruption', 'tvshows&url=policecorruption', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('police detective', 'tvshows&url=policedetective', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('post apocalypse', 'tvshows&url=postapocalypse', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('postmodern', 'tvshows&url=postmodern', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('psychopath', 'tvshows&url=psychopath', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('race against time', 'tvshows&url=raceagainsttime', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('redemption', 'tvshows&url=redemption', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('remake', 'tvshows&url=remake', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('rescue', 'tvshows&url=rescue', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('road movie', 'tvshows&url=roadmovie', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('robbery', 'tvshows&url=robbery', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('robot', 'tvshows&url=robot', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('rotoscoping', 'tvshows&url=rotoscoping', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('satire', 'tvshows&url=satire', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('self sacrifice', 'tvshows&url=selfsacrifice', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('serial killer', 'tvshows&url=serialkiller', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('shakespeare', 'tvshows&url=shakespeare', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('shootout', 'tvshows&url=shootout', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('show within a show', 'tvshows&url=showwithinashow', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('slasher', 'tvshows&url=slasher', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('southern gothic', 'tvshows&url=southerngothic', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('spaghetti western', 'tvshows&url=spaghettiwestern', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('spirituality', 'tvshows&url=spirituality', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('spoof', 'tvshows&url=spoof', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('steampunk', 'tvshows&url=steampunk', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('subjective camera', 'tvshows&url=subjectivecamera', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('superhero', 'tvshows&url=superhero', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('supernatural', 'tvshows&url=supernatural', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('surprise ending', 'tvshows&url=surpriseending', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('swashbuckler', 'tvshows&url=swashbuckler', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('sword and sandal', 'tvshows&url=swordandsandal', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('tech noir', 'tvshows&url=technoir', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('time travel', 'tvshows&url=timetravel', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('title spoken by character', 'tvshows&url=titlespokenbycharacter', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('told in flashback', 'tvshows&url=toldinflashback', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('vampire', 'tvshows&url=vampire', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('virtual reality', 'tvshows&url=virtualreality', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('voice over narration', 'tvshows&url=voiceovernarration', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('whistleblower', 'tvshows&url=whistleblower', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('wilhelm scream', 'tvshows&url=wilhelmscream', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('wuxia', 'tvshows&url=wuxia', 'tvshowsmain.gif', 'DefaultRecentlyAddedMovies.png')



		self.endDirectory()


	def movthemes(self, lite=False):
		self.addDirectoryItem('action hero', 'movies&url=actionhero', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('alternate history', 'movies&url=alternatehistory', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('ambiguous ending', 'movies&url=ambiguousending', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('americana', 'movies&url=americana', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('anti hero', 'movies&url=antihero', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('avant garde', 'movies&url=avantgarde', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('b movie', 'movies&url=bmovie', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('bank heist', 'movies&url=bankheist', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('based on book', 'movies&url=basedonbook', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('based on play', 'movies&url=basedonplay', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('based on comic', 'movies&url=basedoncomic', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('based on comic book', 'movies&url=basedoncomicbook', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('based on novel', 'movies&url=basedonnovel', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('based on novella', 'movies&url=basedonnovella', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('based on short story', 'movies&url=basedonshortstory', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('battle', 'movies&url=battle', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('betrayal', 'movies&url=betrayal', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('biker', 'movies&url=biker', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('black comedy', 'movies&url=blackcomedy', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('blockbuster', 'movies&url=blockbuster', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('breaking the fourth wall', 'movies&url=breakingthefourthwall', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('business', 'movies&url=business', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('caper', 'movies&url=caper', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('car accident', 'movies&url=caraccident', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('car chase', 'movies&url=carchase', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('car crash', 'movies&url=carcrash', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('character name in title', 'movies&url=characternameintitle', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('characters point of view camera shot', 'movies&url=characterspointofviewcamerashot', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('chick flick', 'movies&url=chickflick', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('coming of age', 'movies&url=comingofage', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('competition', 'movies&url=competition', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('conspiracy', 'movies&url=conspiracy', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('corruption', 'movies&url=corruption', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('criminal mainmind', 'movies&url=criminalmainmind', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('cult', 'movies&url=cult', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('cult film', 'movies&url=cultfilm', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('cyberpunk', 'movies&url=cyberpunk', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('dark hero', 'movies&url=darkhero', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('deus ex machina', 'movies&url=deusexmachina', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('dialogue driven', 'movies&url=dialoguedriven', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('dialogue driven story', 'movies&url=dialoguedrivenstory', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('directed by star', 'movies&url=directedbystar', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('director cameo', 'movies&url=directorcameo', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('double cross', 'movies&url=doublecross', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('dream sequence', 'movies&url=dreamsequence', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('dystopia', 'movies&url=dystopia', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('ensemble cast', 'movies&url=ensemblecast', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('epic', 'movies&url=epic', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('espionage', 'movies&url=espionage', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('experimental', 'movies&url=experimental', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('experimental film', 'movies&url=experimentalfilm', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('fairy tale', 'movies&url=fairytale', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('famous line', 'movies&url=famousline', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('famous opening theme', 'movies&url=famousopeningtheme', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('famous score', 'movies&url=famousscore', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('fantasy sequence', 'movies&url=fantasysequence', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('farce', 'movies&url=farce', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('father daughter relationship', 'movies&url=fatherdaughterrelationship', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('father son relationship', 'movies&url=fathersonrelationship', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('femme fatale', 'movies&url=femmefatale', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('fictional biography', 'movies&url=fictionalbiography', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('flashback', 'movies&url=flashback', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('futuristic', 'movies&url=futuristic', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('good versus evil', 'movies&url=goodversusevil', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('heist', 'movies&url=heist', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('hero', 'movies&url=hero', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('high school', 'movies&url=highschool', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('husband wife relationship', 'movies&url=husbandwiferelationship', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('idealism', 'movies&url=idealism', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('independent film', 'movies&url=independentfilm', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('investigation', 'movies&url=investigation', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('kidnapping', 'movies&url=kidnapping', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('knight', 'movies&url=knight', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('kung fu', 'movies&url=kungfu', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('macguffin', 'movies&url=macguffin', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('medieval times', 'movies&url=medievaltimes', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('mockumentary', 'movies&url=mockumentary', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('monster', 'movies&url=monster', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('mother daughter relationship', 'movies&url=motherdaughterrelationship', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('mother son relationship', 'movies&url=mothersonrelationship', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('multiple actors playing same role', 'movies&url=multipleactorsplayingsamerole', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('multiple endings', 'movies&url=multipleendings', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('multiple perspectives', 'movies&url=multipleperspectives', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('multiple storyline', 'movies&url=multiplestoryline', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('multiple time frames', 'movies&url=multipletimeframes', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('murder', 'movies&url=murder', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('musical number', 'movies&url=musicalnumber', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('neo noir', 'movies&url=neonoir', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('neorealism', 'movies&url=neorealism', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('ninja', 'movies&url=ninja', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('no background score', 'movies&url=nobackgroundscore', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('no music', 'movies&url=nomusic', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('no opening credits', 'movies&url=noopeningcredits', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('no title at beginning', 'movies&url=notitleatbeginning', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('nonlinear timeline', 'movies&url=nonlineartimeline', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('on the run', 'movies&url=ontherun', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('one against many', 'movies&url=oneagainstmany', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('one man army', 'movies&url=onemanarmy', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('opening action scene', 'movies&url=openingactionscene', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('organized crime', 'movies&url=organizedcrime', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('parenthood', 'movies&url=parenthood', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('parody', 'movies&url=parody', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('plot twist', 'movies&url=plottwist', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('police corruption', 'movies&url=policecorruption', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('police detective', 'movies&url=policedetective', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('post apocalypse', 'movies&url=postapocalypse', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('postmodern', 'movies&url=postmodern', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('psychopath', 'movies&url=psychopath', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('race against time', 'movies&url=raceagainsttime', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('redemption', 'movies&url=redemption', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('remake', 'movies&url=remake', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('rescue', 'movies&url=rescue', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('road movie', 'movies&url=roadmovie', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('robbery', 'movies&url=robbery', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('robot', 'movies&url=robot', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('rotoscoping', 'movies&url=rotoscoping', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('satire', 'movies&url=satire', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('self sacrifice', 'movies&url=selfsacrifice', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('serial killer', 'movies&url=serialkiller', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('shakespeare', 'movies&url=shakespeare', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('shootout', 'movies&url=shootout', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('show within a show', 'movies&url=showwithinashow', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('slasher', 'movies&url=slasher', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('southern gothic', 'movies&url=southerngothic', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('spaghetti western', 'movies&url=spaghettiwestern', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('spirituality', 'movies&url=spirituality', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('spoof', 'movies&url=spoof', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('steampunk', 'movies&url=steampunk', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('subjective camera', 'movies&url=subjectivecamera', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('superhero', 'movies&url=superhero', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('supernatural', 'movies&url=supernatural', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('surprise ending', 'movies&url=surpriseending', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('swashbuckler', 'movies&url=swashbuckler', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('sword and sandal', 'movies&url=swordandsandal', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('tech noir', 'movies&url=technoir', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('time travel', 'movies&url=timetravel', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('title spoken by character', 'movies&url=titlespokenbycharacter', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('told in flashback', 'movies&url=toldinflashback', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('vampire', 'movies&url=vampire', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('virtual reality', 'movies&url=virtualreality', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('voice over narration', 'movies&url=voiceovernarration', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('whistleblower', 'movies&url=whistleblower', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('wilhelm scream', 'movies&url=wilhelmscream', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')
		self.addDirectoryItem('wuxia', 'movies&url=wuxia', 'movmain.gif', 'DefaultRecentlyAddedMovies.png')



		self.endDirectory()

	def mytvshows(self, lite=False):
		self.accountCheck()

		if traktCredentials == True and imdbCredentials == True:
			self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'tvshowsmain.gif', 'DefaultTVShows.jpg', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
			self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'tvshowsmain.gif', 'DefaultTVShows.jpg', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
			self.addDirectoryItem(32034, 'tvshows&url=imdbwatchlist', 'tvshowsmain.gif', 'DefaultTVShows.jpg')

		elif traktCredentials == True:
			self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'tvshowsmain.gif', 'DefaultTVShows.jpg', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
			self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'tvshowsmain.gif', 'DefaultTVShows.jpg', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))

		elif imdbCredentials == True:
			self.addDirectoryItem(32032, 'tvshows&url=imdbwatchlist', 'tvshowsmain.gif', 'DefaultTVShows.jpg')
			self.addDirectoryItem(32033, 'tvshows&url=imdbwatchlist2', 'tvshowsmain.gif', 'DefaultTVShows.jpg')

		if traktCredentials == True:
			self.addDirectoryItem(32035, 'tvshows&url=traktfeatured', 'tvshowsmain.gif', 'DefaultTVShows.jpg')

		elif imdbCredentials == True:
			self.addDirectoryItem(32035, 'tvshows&url=trending', 'tvshowsmain.gif', 'DefaultMovies.jpg', queue=True)

		if traktIndicators == True:
			self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'tvshowsmain.gif', 'DefaultTVShows.jpg', queue=True)
			self.addDirectoryItem(32037, 'calendar&url=progress', 'tvshowsmain.gif', 'DefaultRecentlyAddedEpisodes.jpg', queue=True)
			self.addDirectoryItem(32038, 'calendar&url=mycalendar', 'tvshowsmain.gif', 'DefaultRecentlyAddedEpisodes.jpg', queue=True)

		self.addDirectoryItem(32040, 'tvUserlists', 'tvshowsmain.gif', 'DefaultTVShows.jpg')

		if traktCredentials == True:
			self.addDirectoryItem(32041, 'episodeUserlists', 'tvshowsmain.gif', 'DefaultTVShows.jpg')

		if lite == False:
			self.addDirectoryItem(32031, 'tvliteNavigator', 'tvshowsmain.gif', 'DefaultTVShows.jpg')
			self.addDirectoryItem('Actor Search', 'tvPerson', 'search2.gif', 'DefaultTVShows.jpg')
			self.addDirectoryItem(32010, 'tvSearch', 'search2.gif', 'DefaultTVShows.jpg')

		self.endDirectory()

		
	def tools(self):
		self.addDirectoryItem(32043, 'openSettings&query=0.0', 'tools2.gif', 'DefaultAddonProgram.jpg')
		self.addDirectoryItem(32044, 'openSettings&query=3.1', 'tools2.gif', 'DefaultAddonProgram.jpg')
		self.addDirectoryItem(32045, 'openSettings&query=1.0', 'tools2.gif', 'DefaultAddonProgram.jpg')
		self.addDirectoryItem(32046, 'openSettings&query=6.0', 'tools2.gif', 'DefaultAddonProgram.jpg')
		self.addDirectoryItem(32047, 'openSettings&query=2.0', 'tools2.gif', 'DefaultAddonProgram.jpg')
		self.addDirectoryItem(32556, 'libraryNavigator', 'lib.gif', 'DefaultAddonProgram.jpg')
		self.addDirectoryItem(32048, 'openSettings&query=5.0', 'tools2.gif', 'DefaultAddonProgram.jpg')
		self.addDirectoryItem(32049, 'viewsNavigator', 'tools2.gif', 'DefaultAddonProgram.jpg')
		self.addDirectoryItem(32050, 'clearSources', 'tools2.gif', 'DefaultAddonProgram.jpg')
		self.addDirectoryItem(32052, 'clearCache', 'tools2.gif', 'DefaultAddonProgram.jpg')

		self.endDirectory()

	def library(self):
		self.addDirectoryItem(32557, 'openSettings&query=4.0', 'lib.gif', 'DefaultAddonProgram.jpg')
		self.addDirectoryItem(32558, 'updateLibrary&query=tool', 'lib.jpg', 'DefaultAddonProgram.jpg')
		self.addDirectoryItem(32559, control.setting('library.movie'), 'movmain.gif', 'DefaultMovies.jpg', isAction=False)
		self.addDirectoryItem(32560, control.setting('library.tv'), 'tvshowsmain.gif', 'DefaultTVShows.jpg', isAction=False)

		if trakt.getTraktCredentialsInfo():
			self.addDirectoryItem(32561, 'moviesToLibrary&url=traktcollection', 'lib.gif', 'DefaultMovies.jpg')
			self.addDirectoryItem(32562, 'moviesToLibrary&url=traktwatchlist', 'lib.gif', 'DefaultMovies.jpg')
			self.addDirectoryItem(32563, 'tvshowsToLibrary&url=traktcollection', 'lib.gif', 'DefaultTVShows.jpg')
			self.addDirectoryItem(32564, 'tvshowsToLibrary&url=traktwatchlist', 'lib.gif', 'DefaultTVShows.jpg')

		self.endDirectory()

	def downloads(self):
		movie_downloads = control.setting('movie.download.path')
		tv_downloads = control.setting('tv.download.path')

		if len(control.listDir(movie_downloads)[0]) > 0:
			self.addDirectoryItem(32001, movie_downloads, 'movmain.gif', 'DefaultMovies.jpg', isAction=False)
		if len(control.listDir(tv_downloads)[0]) > 0:
			self.addDirectoryItem(32002, tv_downloads, 'tvshowsmain.gif', 'DefaultTVShows.jpg', isAction=False)

		self.endDirectory()


	def search(self):
		self.addDirectoryItem(32001, 'movieSearch', 'search2.gif', 'DefaultMovies.jpg')
		self.addDirectoryItem(32002, 'tvSearch', 'search2.gif', 'DefaultTVShows.jpg')
		self.addDirectoryItem('Actor Search', 'moviePerson', 'search2.gif', 'DefaultMovies.jpg')
		self.addDirectoryItem('TV Actor Search', 'tvPerson', 'search2.gif', 'DefaultTVShows.jpg')

		self.endDirectory()


	def views(self):
		try:
			control.idle()

			items = [ (control.lang(32001).encode('utf-8'), 'movies'), (control.lang(32002).encode('utf-8'), 'tvshows'), (control.lang(32054).encode('utf-8'), 'seasons'), (control.lang(32038).encode('utf-8'), 'episodes') ]

			select = control.selectDialog([i[0] for i in items], control.lang(32049).encode('utf-8'))

			if select == -1: return

			content = items[select][1]

			title = control.lang(32059).encode('utf-8')
			url = '%s?action=addView&content=%s' % (sys.argv[0], content)

			poster, banner, fanart = control.addonPoster(), control.addonBanner(), control.addonFanart()

			item = control.item(label=title)
			item.setInfo(type='Video', infoLabels = {'title': title})
			item.setArt({'icon': poster, 'thumb': poster, 'poster': poster, 'banner': banner})
			item.setProperty('Fanart_Image', fanart)

			control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)
			control.content(int(sys.argv[1]), content)
			control.directory(int(sys.argv[1]), cacheToDisc=True)

			from resources.lib.modules import views
			views.setView(content, {})
		except:
			return


	def accountCheck(self):
		if traktCredentials == False and imdbCredentials == False:
			control.idle()
			control.infoDialog(control.lang(32042).encode('utf-8'), sound=True, icon='WARNING')
			sys.exit()




	def clearCache(self):
		control.idle()
		yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
		if not yes: return
		from resources.lib.modules import cache
		cache.cache_clear()
		control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')


	def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
		try: name = control.lang(name).encode('utf-8')
		except: pass
		url = '%s?action=%s' % (sysaddon, query) if isAction == True else query
		thumb = os.path.join(artPath, thumb) if not artPath == None else icon
		cm = []
		if queue == True: cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
		if not context == None: cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
		item = control.item(label=name)
		item.addContextMenuItems(cm)
		item.setArt({'icon': thumb, 'thumb': thumb})
		if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
		control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)


	def endDirectory(self):
		control.content(syshandle, 'addons')
		control.directory(syshandle, cacheToDisc=True)


