# -*- coding: utf-8 -*-




import urlparse,resolveurl,sys,urllib,json,xbmc,os,xbmcaddon,xbmcgui
from resources.lib.modules  import sources

dialog = xbmcgui.Dialog()						 
params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

action = params.get('action')

name = params.get('name')

title = params.get('title')

year = params.get('year')

imdb = params.get('imdb')

tvdb = params.get('tvdb')

tmdb = params.get('tmdb')

season = params.get('season')

episode = params.get('episode')

tvshowtitle = params.get('tvshowtitle')

premiered = params.get('premiered')

url = params.get('url')

image = params.get('image')

meta = params.get('meta')

select = params.get('select')

query = params.get('query')

source = params.get('source')

content = params.get('content')


if action == None:
    from resources.lib.indexers import navigator
    navigator.navigator().root()

elif action == 'tvthemeNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().themes()

elif action == 'movthemeNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movthemes()

	
elif action == 'toptvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().toptvshows()

elif action == 'Birthsigns':
    from resources.lib.indexers import navigator
    navigator.navigator().Birthsigns()

if action == 'HRmovieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().HRrated()

elif action == 'tvusNetworks':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().networks()

if action == 'networks2Navigator':
    from resources.lib.indexers import navigator
    navigator.navigator().networks2()

if action == 'networks2tvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().networks2tv()

if action == 'bottommoviesNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().bottommovies(url)


elif action == 'Aquarius':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().Aquarius(url)


elif action == 'Aquarius':
    from resources.lib.indexers import movies
    movies.movies().Aquarius(url)


elif action == 'Pisces':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().Pisces(url)


elif action == 'Pisces':
    from resources.lib.indexers import movies
    movies.movies().Pisces(url)


elif action == 'Aries':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().Aries(url)


elif action == 'Aries':
    from resources.lib.indexers import movies
    movies.movies().Aries(url)


elif action == 'Taurus':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().Taurus(url)


elif action == 'Taurus':
    from resources.lib.indexers import movies
    movies.movies().Taurus(url)


elif action == 'Gemini':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().Gemini(url)


elif action == 'Gemini':
    from resources.lib.indexers import movies
    movies.movies().Gemini(url)


elif action == 'Cancer':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().Cancer(url)


elif action == 'Cancer':
    from resources.lib.indexers import movies
    movies.movies().Cancer(url)


elif action == 'Leo':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().Leo(url)


elif action == 'Leo':
    from resources.lib.indexers import movies
    movies.movies().Leo(url)


elif action == 'Virgo':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().Virgo(url)


elif action == 'Virgo':
    from resources.lib.indexers import movies
    movies.movies().Virgo(url)


elif action == 'Libra':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().Libra(url)


elif action == 'Libra':
    from resources.lib.indexers import movies
    movies.movies().Libra(url)


elif action == 'Sagittarius':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().Sagittarius(url)


elif action == 'Sagittarius':
    from resources.lib.indexers import movies
    movies.movies().Sagittarius(url)


elif action == 'Capricorn':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().Capricorn(url)


elif action == 'Capricorn':
    from resources.lib.indexers import movies
    movies.movies().Capricorn(url)


elif action == 'scorpio':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().scorpio(url)


elif action == 'scorpio':
    from resources.lib.indexers import movies
    movies.movies().scorpio(url)


elif action == 'movieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies()

elif action == 'movieliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies(lite=True)

elif action == 'mymovieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies()

elif action == 'mymovieliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies(lite=True)

elif action == 'tvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows()

elif action == 'tvliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows(lite=True)

elif action == 'mytvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mytvshows()

elif action == 'mytvliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mytvshows(lite=True)

elif action == 'movieMosts':
    from resources.lib.indexers import navigator
    navigator.navigator().movieMosts()

elif action == 'downloadNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().downloads()

elif action == 'libraryNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().library()

elif action == 'toolNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tools()

elif action == 'searchNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().search()

elif action == 'viewsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().views()

elif action == 'clearCache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCache()

elif action == 'infoCheck':
    from resources.lib.indexers import navigator
    navigator.navigator().infoCheck('')

elif action == 'movies':
    from resources.lib.indexers import movies
    movies.movies().get(url)

elif action == 'moviePage':
    from resources.lib.indexers import movies
    movies.movies().get(url)

elif action == 'movieWidget':
    from resources.lib.indexers import movies
    movies.movies().widget()

elif action == 'movieSearch':
    from resources.lib.indexers import movies
    movies.movies().search()

elif action == 'moviePerson':
    from resources.lib.indexers import movies
    movies.movies().person()

elif action == 'movieGenres':
    from resources.lib.indexers import movies
    movies.movies().genres()

elif action == 'movieLanguages':
    from resources.lib.indexers import movies
    movies.movies().languages()

elif action == 'movieCertificates':
    from resources.lib.indexers import movies
    movies.movies().certifications()

elif action == 'movieYears':
    from resources.lib.indexers import movies
    movies.movies().years()

elif action == 'moviePersons':
    from resources.lib.indexers import movies
    movies.movies().persons(url)

elif action == 'movieUserlists':
    from resources.lib.indexers import movies
    movies.movies().userlists()

elif action == 'tvshows':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)

elif action == 'tvshowPage':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)

elif action == 'tvSearch':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search()

elif action == 'tvPerson':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().person()

elif action == 'tvGenres':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().genres()

elif action == 'tvNetworks':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().networks()

elif action == 'tvLanguages':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().languages()

elif action == 'tvCertificates':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().certifications()

elif action == 'tvPersons':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().persons(url)

elif action == 'tvUserlists':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().userlists()

elif action == 'seasons':
    from resources.lib.indexers import episodes
    episodes.seasons().get(tvshowtitle, year, imdb, tvdb)

elif action == 'episodes':
    from resources.lib.indexers import episodes
    episodes.episodes().get(tvshowtitle, year, imdb, tvdb, season, episode)

elif action == 'calendar':
    from resources.lib.indexers import episodes
    episodes.episodes().calendar(url)

elif action == 'tvWidget':
    from resources.lib.indexers import episodes
    episodes.episodes().widget()

elif action == 'calendars':
    from resources.lib.indexers import episodes
    episodes.episodes().calendars()

elif action == 'episodeUserlists':
    from resources.lib.indexers import episodes
    episodes.episodes().userlists()

elif action == 'refresh':
    from resources.lib.modules import control
    control.refresh()

elif action == 'queueItem':
    from resources.lib.modules import control
    control.queueItem()

elif action == 'openSettings':
    from resources.lib.modules import control
    control.openSettings(query)

elif action == 'artwork':
    from resources.lib.modules import control
    control.artwork()

elif action == 'addView':
    from resources.lib.modules import views
    views.addView(content)

elif action == 'moviePlaycount':
    from resources.lib.modules import playcount
    playcount.movies(imdb, query)

elif action == 'episodePlaycount':
    from resources.lib.modules import playcount
    playcount.episodes(imdb, tvdb, season, episode, query)

elif action == 'tvPlaycount':
    from resources.lib.modules import playcount
    playcount.tvshows(name, imdb, tvdb, season, query)

elif action == 'trailer':
    from resources.lib.modules import trailer
    trailer.trailer().play(name, url)

elif action == 'traktManager':
    from resources.lib.modules import trakt
    trakt.manager(name, imdb, tvdb, content)

elif action == 'authTrakt':
    from resources.lib.modules import trakt
    trakt.authTrakt()

elif action == 'smuSettings':
    try: import resolveurl
    except: pass
    resolveurl.display_settings()

elif action == 'download':
    import json
    from resources.lib.modules import sources
    from resources.lib.modules import downloader
    try: downloader.download(name, image, sources.sources().sourcesResolve(json.loads(source)[0], True))
    except: pass

elif action == 'play':
    from resources.lib.modules import control
    select = control.setting('hosts.mode')
    if select == '3' and 'plugin' in control.infoLabel('Container.PluginName'):
		from resources.lib.modules import sources
		sources.sources().play_dialog(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
    elif select == '4' and 'plugin' in control.infoLabel('Container.PluginName'):
		from resources.lib.modules import sources
		sources.sources().play_dialog_list(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
    else:
		from resources.lib.modules import sources										  
		sources.sources().play(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)

		
elif action == 'play_alter':
		from resources.lib.modules import sources
		sources.sources().play_alter(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta)
elif action == 'addItem':
    from resources.lib.modules import sources
    sources.sources().addItem(title)

elif action == 'playItem':
    from resources.lib.modules import sources
    sources.sources().playItem(title, source)

elif action == 'alterSources':
    from resources.lib.modules import sources
    sources.sources().alterSources(url, meta)

elif action == 'clearSources':
    from resources.lib.modules import sources
    sources.sources().clearSources()

elif action == 'random':
    rtype = params.get('rtype')
    if rtype == 'movie':
        from resources.lib.indexers import movies
        rlist = movies.movies().get(url, create_directory=False)
        r = sys.argv[0]+"?action=play"
    elif rtype == 'episode':
        from resources.lib.indexers import episodes
        rlist = episodes.episodes().get(tvshowtitle, year, imdb, tvdb, season, create_directory=False)
        r = sys.argv[0]+"?action=play"
    elif rtype == 'season':
        from resources.lib.indexers import episodes
        rlist = episodes.seasons().get(tvshowtitle, year, imdb, tvdb, create_directory=False)
        r = sys.argv[0]+"?action=random&rtype=episode"
    elif rtype == 'show':
        from resources.lib.indexers import tvshows
        rlist = tvshows.tvshows().get(url, create_directory=False)
        r = sys.argv[0]+"?action=random&rtype=season"
    from resources.lib.modules import control
    from random import randint
    import json
    try:
        rand = randint(1,len(rlist))-1
        for p in ['title','year','imdb','tvdb','season','episode','tvshowtitle','premiered','select']:
            if rtype == "show" and p == "tvshowtitle":
                try: r += '&'+p+'='+urllib.quote_plus(rlist[rand]['title'])
                except: pass
            else:
                try: r += '&'+p+'='+urllib.quote_plus(rlist[rand][p])
                except: pass
        try: r += '&meta='+urllib.quote_plus(json.dumps(rlist[rand]))
        except: r += '&meta='+urllib.quote_plus("{}")
        if rtype == "movie":
            try: control.infoDialog(rlist[rand]['title'], control.lang(32536).encode('utf-8'), time=30000)
            except: pass
        elif rtype == "episode":
            try: control.infoDialog(rlist[rand]['tvshowtitle']+" - Season "+rlist[rand]['season']+" - "+rlist[rand]['title'], control.lang(32536).encode('utf-8'), time=30000)
            except: pass
        control.execute('RunPlugin(%s)' % r)
    except:
        control.infoDialog(control.lang(32537).encode('utf-8'), time=8000)

elif action == 'movieToLibrary':
    from resources.lib.modules import libtools
    libtools.libmovies().add(name, title, year, imdb, tmdb)

elif action == 'moviesToLibrary':
    from resources.lib.modules import libtools
    libtools.libmovies().range(url)

elif action == 'tvshowToLibrary':
    from resources.lib.modules import libtools
    libtools.libtvshows().add(tvshowtitle, year, imdb, tvdb)

elif action == 'tvshowsToLibrary':
    from resources.lib.modules import libtools
    libtools.libtvshows().range(url)

elif action == 'updateLibrary':
    from resources.lib.modules import libtools
    libtools.libepisodes().update(query)

elif action == 'service':
    from resources.lib.modules import libtools
    libtools.libepisodes().service()

elif action == 'universalscrapersettings'    : xbmcaddon.Addon('script.module.universalscrapers').openSettings()
