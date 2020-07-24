# -*- coding: utf-8 -*-


from resources.lib.modules import trakt
from resources.lib.modules import cleantitle
from resources.lib.modules import cleangenre
from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import metacache
from resources.lib.modules import playcount
from resources.lib.modules import workers
from resources.lib.modules import views
from resources.lib.modules import utils
from resources.lib.indexers import navigator

import os,sys,re,json,urllib,urlparse,datetime

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?',''))) if len(sys.argv) > 1 else dict()

action = params.get('action')

control.moderator()


class tvshows:
    def __init__(self):
        self.list = []

        self.imdb_link = 'http://www.imdb.com'
        self.trakt_link = 'http://api.trakt.tv'
        self.tvmaze_link = 'http://www.tvmaze.com'
        self.tvdb_key = 'MTQ4RENEM0JENjIzMjE4RA=='
        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        self.trakt_user = control.setting('trakt.user').strip()
        self.imdb_user = control.setting('imdb.user').replace('ur', '')
        self.fanart_tv_user = control.setting('fanart.tv.user')
        self.user = control.setting('fanart.tv.user') + str('')
        self.lang = control.apiLanguage()['tvdb']

        self.search_link = 'http://api.trakt.tv/search/show?limit=20&page=1&query='
        self.tvmaze_info_link = 'http://api.tvmaze.com/shows/%s'
        self.tvdb_info_link = 'http://thetvdb.com/api/%s/series/%s/%s.xml' % (self.tvdb_key.decode('base64'), '%s', self.lang)
        self.fanart_tv_art_link = 'http://webservice.fanart.tv/v3/tv/%s'
        self.fanart_tv_level_link = 'http://webservice.fanart.tv/v3/level'
        self.tvdb_by_imdb = 'http://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=%s'
        self.tvdb_by_query = 'http://thetvdb.com/api/GetSeries.php?seriesname=%s'
        self.tvdb_image = 'http://thetvdb.com/banners/'
        self.persons_link = 'http://www.imdb.com/search/name?count=100&name='
        self.personlist_link = 'http://www.imdb.com/search/name?count=100&gender=male,female'
        self.popular_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=100,&release_date=,date[0]&sort=moviemeter,asc&count=40&start=1'
        self.airing_link = 'http://www.imdb.com/search/title?title_type=tv_episode&release_date=date[1],date[0]&sort=moviemeter,asc&count=40&start=1'
        self.active_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=10,&production_status=active&sort=moviemeter,asc&count=40&start=1'
        self.premiere_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&languages=en&num_votes=10,&release_date=date[60],date[0]&sort=moviemeter,asc&count=40&start=1'
        self.rating_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=5000,&release_date=,date[0]&sort=user_rating,desc&count=40&start=1'
        self.views_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=100,&release_date=,date[0]&sort=num_votes,desc&count=40&start=1'
        self.person_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&release_date=,date[0]&role=%s&sort=year,desc&count=40&start=1'
        self.genre_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&release_date=,date[0]&genres=%s&sort=moviemeter,asc&count=40&start=1'
        self.keyword_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&release_date=,date[0]&keywords=%s&sort=moviemeter,asc&count=40&start=1'
        self.language_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=100,&production_status=released&primary_language=%s&sort=moviemeter,asc&count=40&start=1'
        self.certification_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&release_date=,date[0]&certificates=us:%s&sort=moviemeter,asc&count=40&start=1'
        self.trending_link = 'http://api.trakt.tv/shows/trending?limit=40&page=1'
        self.popular2_link = 'http://api.trakt.tv/shows/popular?limit=40&page=1'
        self.anticipated_link = 'http://api.trakt.tv/shows/anticipated?limit=40&page=1'
        self.update_link = 'http://api.trakt.tv/shows/updates/%s?limit=40&page=1'
        self.genre2_link = 'http://api.trakt.tv/shows/genres/%s?limit=40&page=1'
        self.search2_link = 'http://api.trakt.tv/shows/search/%s?limit=40&page=1'
        self.calendar_link = 'http://api.trakt.tv/calendars/all/shows?limit=40&page=1'
        self.premieres_link = 'http://api.trakt.tv/calendars/all/shows/premieres?limit=40&page=1'
		
        self.traktlists_link = 'http://api.trakt.tv/users/me/lists'
        self.traktlikedlists_link = 'http://api.trakt.tv/users/likes/lists?limit=1000000'
        self.traktlist_link = 'http://api.trakt.tv/users/%s/lists/%s/items'
        self.traktcollection_link = 'http://api.trakt.tv/users/me/collection/shows'
        self.traktwatchlist_link = 'http://api.trakt.tv/users/me/watchlist/shows'
        self.traktfeatured_link = 'http://api.trakt.tv/recommendations/shows?limit=40'
        self.imdblists_link = 'http://www.imdb.com/user/ur%s/lists?tab=all&sort=mdfd&order=desc&filter=titles' % self.imdb_user
        self.imdblist_link = 'http://www.imdb.com/list/%s/?view=detail&sort=alpha,asc&title_type=tvSeries,miniSeries&start=1'
        self.imdblist2_link = 'http://www.imdb.com/list/%s/?view=detail&sort=date_added,desc&title_type=tvSeries,miniSeries&start=1'
        self.imdbwatchlist_link = 'http://www.imdb.com/user/ur%s/watchlist?sort=alpha,asc' % self.imdb_user
        self.imdbwatchlist2_link = 'http://www.imdb.com/user/ur%s/watchlist?sort=date_added,desc' % self.imdb_user

        self.superhero_link = 'http://www.imdb.com/search/title?keywords=superhero&title_type=tv_series&count=40&start=1&countries=us&sort=alpha,asc&ref_=gnr_kw_fa,desc'
        self.Action_link = 'http://www.imdb.com/search/title?genres=action&title_type=tv_series&count=40&start=1&countries=us&sort=alpha,asc&ref_=gnr_kw_fa,desc'
        self.Adventure_link = 'http://www.imdb.com/search/title?genres=Adventure&title_type=tv_series&count=40&start=1&countries=us&sort=alpha,asc&ref_=gnr_kw_fa,desc'
        self.Animation_link = 'http://www.imdb.com/search/title?genres=Animation&title_type=tv_series&count=40&start=1&countries=us&sort=alpha,asc&ref_=gnr_kw_fa,desc'
        self.Comedy_link = 'http://www.imdb.com/search/title?genres=Comedy&title_type=tv_series&count=40&start=1&countries=us&sort=alpha,asc&ref_=gnr_kw_fa,desc'		
        self.Crime_link = 'http://www.imdb.com/search/title?genres=Crime&title_type=tv_series&count=40&start=1&countries=us&sort=alpha,asc&ref_=gnr_kw_fa,desc'		
        self.Drama_link = 'http://www.imdb.com/search/title?genres=Drama&title_type=tv_series&count=40&start=1&countries=us&sort=alpha,asc&ref_=gnr_kw_fa,desc'		
        self.Family_link = 'http://www.imdb.com/search/title?genres=Family&title_type=tv_series&count=40&start=1&countries=us&sort=alpha,asc&ref_=gnr_kw_fa,desc'		
        self.Fantasy_link = 'http://www.imdb.com/search/title?genres=Fantasy&title_type=tv_series&count=40&start=1&countries=us&sort=alpha,asc&ref_=gnr_kw_fa,desc'		
        self.History_link = 'http://www.imdb.com/search/title?genres=History&title_type=tv_series&count=40&start=1&countries=us&sort=alpha,asc&ref_=gnr_kw_fa,desc'		
        self.Horror_link = 'http://www.imdb.com/search/title?genres=Horror&title_type=tv_series&count=40&start=1&countries=us&sort=alpha,asc&ref_=gnr_kw_fa,desc'		
        self.Mystery_link = 'http://www.imdb.com/search/title?genres=Mystery&title_type=tv_series&count=40&start=1&countries=us&sort=alpha,asc&ref_=gnr_kw_fa,desc'		
        self.ScienceFiction_link = 'http://www.imdb.com/search/title?genres=ScienceFiction&title_type=tv_series&count=40&start=1&countries=us&sort=alpha,asc&ref_=gnr_kw_fa,desc'		
        self.Romance_link = 'http://www.imdb.com/search/title?genres=Romance&title_type=tv_series&count=40&start=1&countries=us&sort=alpha,asc&ref_=gnr_kw_fa,desc'		
        self.Sport_link = 'http://www.imdb.com/search/title?genres=Sport&title_type=tv_series&count=40&start=1&countries=us&sort=alpha,asc&ref_=gnr_kw_fa,desc'		
        self.Thriller_link = 'http://www.imdb.com/search/title?genres=Thriller&title_type=tv_series&count=40&start=1&countries=us&sort=alpha,asc&ref_=gnr_kw_fa,desc'		
        self.War_link = 'http://www.imdb.com/search/title?genres=War&title_type=tv_series&count=40&start=1&countries=us&sort=alpha,asc&ref_=gnr_kw_fa,desc'		
        self.Western_link = 'http://www.imdb.com/search/title?genres=Western&title_type=tv_series&count=40&start=1&countries=us&sort=alpha,asc&ref_=gnr_kw_fa,desc'
        self.listAquarius_link = 'http://www.imdb.com/search/name?count=100&gender=male,female&star_sign=aquarius'
        self.listPisces_link = 'http://www.imdb.com/search/name?count=100&gender=male,female&star_sign=pisces'
        self.listAries_link = 'http://www.imdb.com/search/name?count=100&gender=male,female&star_sign=aries'
        self.listTaurus_link = 'http://www.imdb.com/search/name?count=100&gender=male,female&star_sign=taurus'
        self.listGemini_link = 'http://www.imdb.com/search/name?count=100&gender=male,female&star_sign=gemini'
        self.listCancer_link = 'http://www.imdb.com/search/name?count=100&gender=male,female&star_sign=cancer'
        self.listLeo_link = 'http://www.imdb.com/search/name?count=100&gender=male,female&star_sign=leo'
        self.listVirgo_link = 'http://www.imdb.com/search/name?count=100&gender=male,female&star_sign=virgo'
        self.listLibra_link = 'http://www.imdb.com/search/name?count=100&gender=male,female&star_sign=libra'
        self.listCapricorn_link = 'http://www.imdb.com/search/name?count=100&gender=male,female&star_sign=capricorn'
        self.listscorpio_link = 'http://www.imdb.com/search/name?count=100&gender=male,female&star_sign=scorpio'
        self.listSagittarius_link = 'http://www.imdb.com/search/name?count=100&gender=male,female&star_sign=Sagittarius'
        self.anime_link = 'http://www.imdb.com/search/title?count=50&keywords=anime&ref_=gnr_kw_ag,desc&start=1'

        #self._link = 'http://www.imdb.com/search/title?count=50&keywords=bruce-lee&ref_=gnr_kw_ag,desc&start=1'
        #self._link = 'http://www.imdb.com/search/title?,desc&count=40&start=1'
        #self._link = 'http://www.imdb.com/search/title?,desc&count=40&start=1'
        self.actionhero_link = 'http://www.imdb.com/search/title?count=50&keywords=action-hero&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.alternatehistory_link = 'http://www.imdb.com/search/title?count=50&keywords=alternate-history&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.ambiguousending_link = 'http://www.imdb.com/search/title?count=50&keywords=ambiguous-ending&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.americana_link = 'http://www.imdb.com/search/title?count=50&keywords=americana&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.antihero_link = 'http://www.imdb.com/search/title?count=50&keywords=anti-hero&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.avantgarde_link = 'http://www.imdb.com/search/title?count=50&keywords=avant-garde&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.bmovie_link = 'http://www.imdb.com/search/title?count=50&keywords=b-movie&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.bankheist_link = 'http://www.imdb.com/search/title?count=50&keywords=bank-heist&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.basedonbook_link = 'http://www.imdb.com/search/title?count=50&keywords=based-on-book&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.basedonplay_link = 'http://www.imdb.com/search/title?count=50&keywords=based-on-play&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.basedoncomic_link = 'http://www.imdb.com/search/title?count=50&keywords=based-on-comic&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.basedoncomicbook_link = 'http://www.imdb.com/search/title?count=50&keywords=based-on-comic-book&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.basedonnovel_link = 'http://www.imdb.com/search/title?count=50&keywords=based-on-novel&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.basedonnovella_link = 'http://www.imdb.com/search/title?count=50&keywords=based-on-novella&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.basedonshortstory_link = 'http://www.imdb.com/search/title?count=50&keywords=based-on-short-story&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.battle_link = 'http://www.imdb.com/search/title?count=50&keywords=battle&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.betrayal_link = 'http://www.imdb.com/search/title?count=50&keywords=betrayal&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.biker_link = 'http://www.imdb.com/search/title?count=50&keywords=biker&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.blackcomedy_link = 'http://www.imdb.com/search/title?count=50&keywords=black-comedy&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.blockbuster_link = 'http://www.imdb.com/search/title?count=50&keywords=blockbuster&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.breakingthefourthwall_link = 'http://www.imdb.com/search/title?count=50&keywords=breaking-the-fourth-wall&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.business_link = 'http://www.imdb.com/search/title?count=50&keywords=business&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.caper_link = 'http://www.imdb.com/search/title?count=50&keywords=caper&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.caraccident_link = 'http://www.imdb.com/search/title?count=50&keywords=car-accident&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.carchase_link = 'http://www.imdb.com/search/title?count=50&keywords=car-chase&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.carcrash_link = 'http://www.imdb.com/search/title?count=50&keywords=car-crash&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.characternameintitle_link = 'http://www.imdb.com/search/title?count=50&keywords=character-name-in-title&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.characterspointofviewcamerashot_link = 'http://www.imdb.com/search/title?count=50&keywords=character%27s-point-of-view-camera-shot&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.chickflick_link = 'http://www.imdb.com/search/title?count=50&keywords=chick-flick&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.comingofage_link = 'http://www.imdb.com/search/title?count=50&keywords=coming-of-age&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.competition_link = 'http://www.imdb.com/search/title?count=50&keywords=competition&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.conspiracy_link = 'http://www.imdb.com/search/title?count=50&keywords=conspiracy&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.corruption_link = 'http://www.imdb.com/search/title?count=50&keywords=corruption&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.criminalmainmind_link = 'http://www.imdb.com/search/title?count=50&keywords=criminal-mastermind&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.cult_link = 'http://www.imdb.com/search/title?count=50&keywords=cult&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.cultfilm_link = 'http://www.imdb.com/search/title?count=50&keywords=cult-film&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.cyberpunk_link = 'http://www.imdb.com/search/title?count=50&keywords=cyberpunk&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.darkhero_link = 'http://www.imdb.com/search/title?count=50&keywords=dark-hero&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.deusexmachina_link = 'http://www.imdb.com/search/title?count=50&keywords=deus-ex-machina&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.dialoguedriven_link = 'http://www.imdb.com/search/title?count=50&keywords=dialogue-driven&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.dialoguedrivenstory_link = 'http://www.imdb.com/search/title?count=50&keywords=dialogue-driven-story&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.directedbystar_link = 'http://www.imdb.com/search/title?count=50&keywords=directed-by-star&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.directorcameo_link = 'http://www.imdb.com/search/title?count=50&keywords=director-cameo&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.doublecross_link = 'http://www.imdb.com/search/title?count=50&keywords=double-cross&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.dreamsequence_link = 'http://www.imdb.com/search/title?count=50&keywords=dream-sequence&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.dystopia_link = 'http://www.imdb.com/search/title?count=50&keywords=dystopia&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.ensemblecast_link = 'http://www.imdb.com/search/title?count=50&keywords=ensemble-cast&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.epic_link = 'http://www.imdb.com/search/title?count=50&keywords=epic&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.espionage_link = 'http://www.imdb.com/search/title?count=50&keywords=espionage&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.experimental_link = 'http://www.imdb.com/search/title?count=50&keywords=experimental&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.experimentalfilm_link = 'http://www.imdb.com/search/title?count=50&keywords=experimental-film&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.fairytale_link = 'http://www.imdb.com/search/title?count=50&keywords=fairy-tale&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.famousline_link = 'http://www.imdb.com/search/title?count=50&keywords=famous-line&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.famousopeningtheme_link = 'http://www.imdb.com/search/title?count=50&keywords=famous-opening-theme&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.famousscore_link = 'http://www.imdb.com/search/title?count=50&keywords=famous-score&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.fantasysequence_link = 'http://www.imdb.com/search/title?count=50&keywords=fantasy-sequence&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.farce_link = 'http://www.imdb.com/search/title?count=50&keywords=farce&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.fatherdaughterrelationship_link = 'http://www.imdb.com/search/title?count=50&keywords=father-daughter-relationship&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.fathersonrelationship_link = 'http://www.imdb.com/search/title?count=50&keywords=father-son-relationship&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.femmefatale_link = 'http://www.imdb.com/search/title?count=50&keywords=femme-fatale&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.fictionalbiography_link = 'http://www.imdb.com/search/title?count=50&keywords=fictional-biography&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.flashback_link = 'http://www.imdb.com/search/title?count=50&keywords=flashback&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.futuristic_link = 'http://www.imdb.com/search/title?count=50&keywords=futuristic&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.goodversusevil_link = 'http://www.imdb.com/search/title?count=50&keywords=good-versus-evil&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.heist_link = 'http://www.imdb.com/search/title?count=50&keywords=heist&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.hero_link = 'http://www.imdb.com/search/title?count=50&keywords=hero&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.highschool_link = 'http://www.imdb.com/search/title?count=50&keywords=high-school&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.husbandwiferelationship_link = 'http://www.imdb.com/search/title?count=50&keywords=husband-wife-relationship&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.idealism_link = 'http://www.imdb.com/search/title?count=50&keywords=idealism&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.independentfilm_link = 'http://www.imdb.com/search/title?count=50&keywords=independent-film&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.investigation_link = 'http://www.imdb.com/search/title?count=50&keywords=investigation&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.kidnapping_link = 'http://www.imdb.com/search/title?count=50&keywords=kidnapping&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.knight_link = 'http://www.imdb.com/search/title?count=50&keywords=knight&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.kungfu_link = 'http://www.imdb.com/search/title?count=50&keywords=kung-fu&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.macguffin_link = 'http://www.imdb.com/search/title?count=50&keywords=macguffin&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.medievaltimes_link = 'http://www.imdb.com/search/title?count=50&keywords=medieval-times&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.mockumentary_link = 'http://www.imdb.com/search/title?count=50&keywords=mockumentary&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.monster_link = 'http://www.imdb.com/search/title?count=50&keywords=monster&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.motherdaughterrelationship_link = 'http://www.imdb.com/search/title?count=50&keywords=mother-daughter-relationship&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.mothersonrelationship_link = 'http://www.imdb.com/search/title?count=50&keywords=mother-son-relationship&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.multipleactorsplayingsamerole_link = 'http://www.imdb.com/search/title?count=50&keywords=multiple-actors-playing-same-role&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.multipleendings_link = 'http://www.imdb.com/search/title?count=50&keywords=multiple-endings&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.multipleperspectives_link = 'http://www.imdb.com/search/title?count=50&keywords=multiple-perspectives&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.multiplestoryline_link = 'http://www.imdb.com/search/title?count=50&keywords=multiple-storyline&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.multipletimeframes_link = 'http://www.imdb.com/search/title?count=50&keywords=multiple-time-frames&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.murder_link = 'http://www.imdb.com/search/title?count=50&keywords=murder&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.musicalnumber_link = 'http://www.imdb.com/search/title?count=50&keywords=musical-number&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.neonoir_link = 'http://www.imdb.com/search/title?count=50&keywords=neo-noir&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.neorealism_link = 'http://www.imdb.com/search/title?count=50&keywords=neorealism&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.ninja_link = 'http://www.imdb.com/search/title?count=50&keywords=ninja&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.nobackgroundscore_link = 'http://www.imdb.com/search/title?count=50&keywords=no-background-score&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.nomusic_link = 'http://www.imdb.com/search/title?count=50&keywords=no-music&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.noopeningcredits_link = 'http://www.imdb.com/search/title?count=50&keywords=no-opening-credits&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.notitleatbeginning_link = 'http://www.imdb.com/search/title?count=50&keywords=no-title-at-beginning&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.nonlineartimeline_link = 'http://www.imdb.com/search/title?count=50&keywords=nonlinear-timeline&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.ontherun_link = 'http://www.imdb.com/search/title?count=50&keywords=on-the-run&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.oneagainstmany_link = 'http://www.imdb.com/search/title?count=50&keywords=one-against-many&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.onemanarmy_link = 'http://www.imdb.com/search/title?count=50&keywords=one-man-army&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.openingactionscene_link = 'http://www.imdb.com/search/title?count=50&keywords=opening-action-scene&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.organizedcrime_link = 'http://www.imdb.com/search/title?count=50&keywords=organized-crime&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.parenthood_link = 'http://www.imdb.com/search/title?count=50&keywords=parenthood&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.parody_link = 'http://www.imdb.com/search/title?count=50&keywords=parody&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.plottwist_link = 'http://www.imdb.com/search/title?count=50&keywords=plot-twist&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.policecorruption_link = 'http://www.imdb.com/search/title?count=50&keywords=police-corruption&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.policedetective_link = 'http://www.imdb.com/search/title?count=50&keywords=police-detective&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.postapocalypse_link = 'http://www.imdb.com/search/title?count=50&keywords=post-apocalypse&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.postmodern_link = 'http://www.imdb.com/search/title?count=50&keywords=postmodern&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.psychopath_link = 'http://www.imdb.com/search/title?count=50&keywords=psychopath&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.raceagainsttime_link = 'http://www.imdb.com/search/title?count=50&keywords=race-against-time&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.redemption_link = 'http://www.imdb.com/search/title?count=50&keywords=redemption&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.remake_link = 'http://www.imdb.com/search/title?count=50&keywords=remake&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.rescue_link = 'http://www.imdb.com/search/title?count=50&keywords=rescue&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.roadmovie_link = 'http://www.imdb.com/search/title?count=50&keywords=road-movie&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.robbery_link = 'http://www.imdb.com/search/title?count=50&keywords=robbery&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.robot_link = 'http://www.imdb.com/search/title?count=50&keywords=robot&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.rotoscoping_link = 'http://www.imdb.com/search/title?count=50&keywords=rotoscoping&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.satire_link = 'http://www.imdb.com/search/title?count=50&keywords=satire&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.selfsacrifice_link = 'http://www.imdb.com/search/title?count=50&keywords=self-sacrifice&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.serialkiller_link = 'http://www.imdb.com/search/title?count=50&keywords=serial-killer&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.shakespeare_link = 'http://www.imdb.com/search/title?count=50&keywords=shakespeare&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.shootout_link = 'http://www.imdb.com/search/title?count=50&keywords=shootout&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.showwithinashow_link = 'http://www.imdb.com/search/title?count=50&keywords=show-within-a-show&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.slasher_link = 'http://www.imdb.com/search/title?count=50&keywords=slasher&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.southerngothic_link = 'http://www.imdb.com/search/title?count=50&keywords=southern-gothic&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.spaghettiwestern_link = 'http://www.imdb.com/search/title?count=50&keywords=spaghetti-western&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.spirituality_link = 'http://www.imdb.com/search/title?count=50&keywords=spirituality&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.spoof_link = 'http://www.imdb.com/search/title?count=50&keywords=spoof&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.steampunk_link = 'http://www.imdb.com/search/title?count=50&keywords=steampunk&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.subjectivecamera_link = 'http://www.imdb.com/search/title?count=50&keywords=subjective-camera&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.superhero_link = 'http://www.imdb.com/search/title?count=50&keywords=superhero&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.supernatural_link = 'http://www.imdb.com/search/title?count=50&keywords=supernatural&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.surpriseending_link = 'http://www.imdb.com/search/title?count=50&keywords=surprise-ending&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.swashbuckler_link = 'http://www.imdb.com/search/title?count=50&keywords=swashbuckler&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.swordandsandal_link = 'http://www.imdb.com/search/title?count=50&keywords=sword-and-sandal&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.technoir_link = 'http://www.imdb.com/search/title?count=50&keywords=tech-noir&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.timetravel_link = 'http://www.imdb.com/search/title?count=50&keywords=time-travel&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.titlespokenbycharacter_link = 'http://www.imdb.com/search/title?count=50&keywords=title-spoken-by-character&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.toldinflashback_link = 'http://www.imdb.com/search/title?count=50&keywords=told-in-flashback&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.vampire_link = 'http://www.imdb.com/search/title?count=50&keywords=vampire&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.virtualreality_link = 'http://www.imdb.com/search/title?count=50&keywords=virtual-reality&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.voiceovernarration_link = 'http://www.imdb.com/search/title?count=50&keywords=voice-over-narration&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.whistleblower_link = 'http://www.imdb.com/search/title?count=50&keywords=whistleblower&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.wilhelmscream_link = 'http://www.imdb.com/search/title?count=50&keywords=wilhelm-scream&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'
        self.wuxia_link = 'http://www.imdb.com/search/title?count=50&keywords=wuxia&ref_=gnr_kw_ag,desc&start=1&title_type=tv_series,tv_special'

        self.fox_link = 'http://www.imdb.com/search/title?companies=fox&title_type=tv_movie,tv_series,tv_special,mini_series'
        self.Sony_link = 'http://www.imdb.com/search/title?companies=Sony&title_type=tv_movie,tv_series,tv_special,mini_series'
        self.DreamWorks_link = 'http://www.imdb.com/search/title?companies=DreamWorks&title_type=tv_movie,tv_series,tv_special,mini_series'
        self.MGM_link = 'http://www.imdb.com/search/title?companies=MGM&title_type=tv_movie,tv_series,tv_special,mini_series'
        self.Paramount_link = 'http://www.imdb.com/search/title?companies=Paramount&title_type=tv_movie,tv_series,tv_special,mini_series'
        self.Universal_link = 'http://www.imdb.com/search/title?companies=Universal&title_type=tv_movie,tv_series,tv_special,mini_series'
        self.disney_link = 'http://www.imdb.com/search/title?companies=disney&title_type=tv_movie,tv_series,tv_special,mini_series'
        self.warner_link = 'http://www.imdb.com/search/title?companies=warner&title_type=tv_movie,tv_series,tv_special,mini_series'
        self.IMDb_link = 'http://www.imdb.com/search/title?online_availability=US/today/IMDb/free/paid&title_type=tv_movie,tv_series,tv_special,mini_series'
        self.Amazon_link = 'http://www.imdb.com/search/title?online_availability=US/today/Amazon/paid,US/today/Amazon/subs&title_type=tv_movie,tv_series,tv_special,mini_series'
        self.Amazonp_link = 'http://www.imdb.com/search/title?online_availability=US/today/Amazon/subs&title_type=tv_movie,tv_series,tv_special,mini_series'
        self.WithoutABox_link = 'http://www.imdb.com/search/title?online_availability=US/today/WithoutABox/free/paid&title_type=tv_movie,tv_series,tv_special,mini_series'



    def get(self, url, idx=True, create_directory=True):
        try:
            try: url = getattr(self, url + '_link')
            except: pass

            try: u = urlparse.urlparse(url).netloc.lower()
            except: pass


            if u in self.trakt_link and '/users/' in url:
                try:
                    if not '/users/me/' in url: raise Exception()
                    if trakt.getActivity() > cache.timeout(self.trakt_list, url, self.trakt_user): raise Exception()
                    self.list = cache.get(self.trakt_list, 720, url, self.trakt_user)
                except:
                    self.list = cache.get(self.trakt_list, 0, url, self.trakt_user)

                if '/users/me/' in url and '/collection/' in url:
                    self.list = sorted(self.list, key=lambda k: utils.title_key(k['title']))

                if idx == True: self.worker()

            elif u in self.trakt_link and self.search_link in url:
                self.list = cache.get(self.trakt_list, 1, url, self.trakt_user)
                if idx == True: self.worker(level=0)

            elif u in self.trakt_link:
                self.list = cache.get(self.trakt_list, 24, url, self.trakt_user)
                if idx == True: self.worker()


            elif u in self.imdb_link and ('/user/' in url or '/list/' in url):
                self.list = cache.get(self.imdb_list, 0, url)
                if idx == True: self.worker()

            elif u in self.imdb_link:
                self.list = cache.get(self.imdb_list, 24, url)
                if idx == True: self.worker()


            elif u in self.tvmaze_link:
                self.list = cache.get(self.tvmaze_list, 168, url)
                if idx == True: self.worker()


            if idx == True and create_directory == True: self.tvshowDirectory(self.list)
            return self.list
        except:
            pass


    def search(self):
        try:
            control.idle()

            t = control.lang(32010).encode('utf-8')
            k = control.keyboard('', t) ; k.doModal()
            q = k.getText() if k.isConfirmed() else None

            if (q == None or q == ''): return

            url = self.search_link + urllib.quote_plus(q)
            url = '%s?action=tvshowPage&url=%s' % (sys.argv[0], urllib.quote_plus(url))
            control.execute('Container.Update(%s)' % url)
        except:
            return


    def person(self):
        try:
            control.idle()

            t = control.lang(32010).encode('utf-8')
            k = control.keyboard('', t) ; k.doModal()
            q = k.getText() if k.isConfirmed() else None

            if (q == None or q == ''): return

            url = self.persons_link + urllib.quote_plus(q)
            url = '%s?action=tvPersons&url=%s' % (sys.argv[0], urllib.quote_plus(url))

            control.execute('Container.Update(%s)' % url)
        except:
            return

    def genres(self):
        genres = [
            ('Action', 'action', True),
            ('Adventure', 'adventure', True),
            ('Animation', 'animation', True),
            ('Anime', 'anime', False),
            ('Biography', 'biography', True),
            ('Comedy', 'comedy', True),
            ('Crime', 'crime', True),
            ('Drama', 'drama', True),
            ('Family', 'family', True),
            ('Fantasy', 'fantasy', True),
            ('Game-Show', 'game_show', True),
            ('History', 'history', True),
            ('Horror', 'horror', True),
            ('Music ', 'music', True),
            ('Musical', 'musical', True),
            ('Mystery', 'mystery', True),
            ('News', 'news', True),
            ('Reality-TV', 'reality_tv', True),
            ('Romance', 'romance', True),
            ('Science Fiction', 'sci_fi', True),
            ('Sport', 'sport', True),
            ('Talk-Show', 'talk_show', True),
            ('Thriller', 'thriller', True),
            ('War', 'war', True),
            ('Western', 'western', True)
        ]

        for i in genres: self.list.append(
            {
                'name': cleangenre.lang(i[0], self.lang),
                'url': self.genre_link % i[1] if i[2] else self.keyword_link % i[1],
                'image': 'genres.png',
                'action': 'tvshows'
            })

        self.addDirectory(self.list)
        return self.list

    def networks(self):
        networks = [
        ('ae', '/networks/29/ae'),
        ('abc', '/networks/3/abc'),
        ('adult-swim', '/networks/10/adult-swim'),
        ('ahc', '/networks/229/ahc'),
        ('amc', '/networks/20/amc'),
        ('animal-planet', '/networks/92/animal-planet'),
        ('audience-network', '/networks/31/audience-network'),
        ('axs-tv', '/networks/170/axs-tv'),
        ('bbc-america', '/networks/15/bbc-america'),
        ('bet', '/networks/56/bet'),
        ('bloomberg-tv', '/networks/172/bloomberg-tv'),
        ('boomerang', '/networks/456/boomerang'),
        ('bounce-tv', '/networks/261/bounce-tv'),
        ('bravo', '/networks/52/bravo'),
        ('byu-television', '/networks/467/byu-television'),
        ('c-span2', '/networks/1514/c-span2'),
        ('cartoon-network', '/networks/11/cartoon-network'),
        ('cbs', '/networks/2/cbs'),
        ('cbs-sports-network', '/networks/272/cbs-sports-network'),
        ('centric', '/networks/58/centric'),
        ('christian-broadcasting-network', '/networks/1513/christian-broadcasting-network'),
        ('cmt', '/networks/173/cmt'),
        ('cnbc', '/networks/93/cnbc'),
        ('cnn', '/networks/40/cnn'),
        ('comedy-central', '/networks/23/comedy-central'),
        ('cooking-channel', '/networks/174/cooking-channel'),
        ('create', '/networks/175/create'),
        ('destination-america', '/networks/107/destination-america'),
        ('discovery-channel', '/networks/66/discovery-channel'),
        ('discovery-family', '/networks/176/discovery-family'),
        ('discovery-life-channel', '/networks/177/discovery-life-channel'),
        ('disney-channel', '/networks/78/disney-channel'),
        ('disney-junior', '/networks/1039/disney-junior'),
        ('disney-xd', '/networks/25/disney-xd'),
        ('diy-network', '/networks/90/diy-network'),
        ('e', '/networks/43/e'),
        ('el-rey-network', '/networks/21/el-rey-network'),
        ('epix', '/networks/253/epix'),
        ('espn', '/networks/39/espn'),
        ('espn2', '/networks/180/espn2'),
        ('espnews', '/networks/181/espnews'),
        ('esquire-network', '/networks/184/esquire-network'),
        ('estrella-tv', '/networks/535/estrella-tv'),
        ('food-network', '/networks/81/food-network'),
        ('fox', '/networks/4/fox'),
        ('fox-business-network', '/networks/524/fox-business-network'),
        ('fox-news-channel', '/networks/185/fox-news-channel'),
        ('fox-sports-1', '/networks/95/fox-sports-1'),
        ('fox-sports-sun', '/networks/1047/fox-sports-sun'),
        ('freeform', '/networks/26/freeform'),
        ('fuse-tv', '/networks/186/fuse-tv'),
        ('fusion', '/networks/187/fusion'),
        ('fx', '/networks/13/fx'),
        ('fxx', '/networks/47/fxx'),
        ('fyi', '/networks/125/fyi'),
        ('g4', '/networks/248/g4'),
        ('game-show-network', '/networks/189/game-show-network'),
        ('golf-channel', '/networks/188/golf-channel'),
        ('great-american-country', '/networks/103/great-american-country'),
        ('h2', '/networks/74/h2'),
        ('hallmark-channel', '/networks/50/hallmark-channel'),
        ('hallmark-movies-mysteries', '/networks/252/hallmark-movies-mysteries'),
        ('hbo', '/networks/8/hbo'),
        ('hbo-family', '/networks/190/hbo-family'),
        ('headline-news', '/networks/193/headline-news'),
        ('hgtv', '/networks/192/hgtv'),
        ('history', '/networks/53/history'),
        ('ifc', '/networks/65/ifc'),
        ('insp', '/networks/660/insp'),
        ('investigation-discovery', '/networks/89/investigation-discovery'),
        ('lifetime-movie-network', '/networks/232/lifetime-movie-network'),
        ('mavtv', '/networks/739/mavtv'),
        ('msnbc', '/networks/201/msnbc'),
        ('mtv', '/networks/22/mtv'),
        ('mtv2', '/networks/145/mtv2'),
        ('national-geographic-channel', '/networks/42/national-geographic-channel'),
        ('national-geographic-wild', '/networks/83/national-geographic-wild'),
        ('nbc', '/networks/1/nbc'),
        ('nbcsn', '/networks/104/nbcsn'),
        ('nfl-network', '/networks/205/nfl-network'),
        ('nick-jr', '/networks/206/nick-jr'),
        ('nickelodeon', '/networks/27/nickelodeon'),
        ('nicktoons', '/networks/73/nicktoons'),
        ('oprah-winfrey-network', '/networks/236/oprah-winfrey-network'),
        ('outdoor-channel', '/networks/207/outdoor-channel'),
        ('oxygen', '/networks/79/oxygen'),
        ('pbs', '/networks/85/pbs'),
        ('pivot', '/networks/211/pivot'),
        ('playboy-tv', '/networks/1035/playboy-tv'),
        ('pop', '/networks/88/pop'),
        ('revolt', '/networks/520/revolt'),
        ('science', '/networks/77/science'),
        ('showtime', '/networks/9/showtime'),
        ('smithsonian-channel', '/networks/86/smithsonian-channel'),
        ('spike', '/networks/34/spike'),
        ('sportsman-channel', '/networks/217/sportsman-channel'),
        ('starz', '/networks/17/starz'),
        ('sundance-tv', '/networks/33/sundance-tv'),
        ('syfy', '/networks/16/syfy'),
        ('syndication', '/networks/72/syndication'),
        ('tbn', '/networks/758/tbn'),
        ('tbs', '/networks/32/tbs'),
        ('telemundo', '/networks/219/telemundo'),
        ('the-cw', '/networks/5/the-cw'),
        ('the-weather-channel', '/networks/228/the-weather-channel'),
        ('tlc', '/networks/80/tlc'),
        ('tnt', '/networks/14/tnt'),
        ('travel-channel', '/networks/82/travel-channel'),
        ('trutv', '/networks/84/trutv'),
        ('tv-guide-channel', '/networks/455/tv-guide-channel'),
        ('tv-land', '/networks/57/tv-land'),
        ('tv-one', '/networks/224/tv-one'),
        ('unimas', '/networks/225/unimas'),
        ('universal-kids', '/networks/342/universal-kids'),
        ('univision', '/networks/226/univision'),
        ('up-tv', '/networks/227/up-tv'),
        ('usa-network', '/networks/30/usa-network'),
        ('velocity', '/networks/142/velocity'),
        ('vh1', '/networks/55/vh1'),
        ('vh1-classic', '/networks/557/vh1-classic'),
        ('viceland', '/networks/1006/viceland'),
        ('we-tv', '/networks/122/we-tv'),
        ('wgbh-tv', '/networks/1089/wgbh-tv'),
        ('world', '/networks/430/world'),
        ('netflix', '/webchannels/1/netflix'),
        ('amazon-prime', '/webchannels/3/amazon-prime'),
        ('hulu', '/webchannels/2/hulu'),
        ('crackle', '/webchannels/4/crackle'),
        ]

        for i in networks: self.list.append({'name': i[0], 'url': self.tvmaze_link + i[1], 'image': 'networks.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list

    def languages(self):
        languages = [
        ('Arabic', 'ar'),
        ('Bulgarian', 'bg'),
        ('Chinese', 'zh'),
        ('Croatian', 'hr'),
        ('Dutch', 'nl'),
        ('English', 'en'),
        ('Finnish', 'fi'),
        ('French', 'fr'),
        ('German', 'de'),
        ('Greek', 'el'),
        ('Hebrew', 'he'),
        ('Hindi ', 'hi'),
        ('Hungarian', 'hu'),
        ('Icelandic', 'is'),
        ('Italian', 'it'),
        ('Japanese', 'ja'),
        ('Korean', 'ko'),
        ('Norwegian', 'no'),
        ('Persian', 'fa'),
        ('Polish', 'pl'),
        ('Portuguese', 'pt'),
        ('Punjabi', 'pa'),
        ('Romanian', 'ro'),
        ('Russian', 'ru'),
        ('Spanish', 'es'),
        ('Swedish', 'sv'),
        ('Turkish', 'tr'),
        ('Ukrainian', 'uk')
        ]

        for i in languages: self.list.append({'name': str(i[0]), 'url': self.language_link % i[1], 'image': 'languages.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def certifications(self):
        certificates = ['TV-G', 'TV-PG', 'TV-14', 'TV-MA']

        for i in certificates: self.list.append({'name': str(i), 'url': self.certification_link % str(i).replace('-', '_').lower(), 'image': 'certificates.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list

    def Aquarius(self, url):
        if url == None:
            self.list = cache.get(self.imdb_person_list, 24, self.listAquarius_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)

        for i in range(0, len(self.list)): self.list[i].update({'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list
		
		
		
    def Pisces(self, url):
        if url == None:
            self.list = cache.get(self.imdb_person_list, 24, self.listPisces_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)

        for i in range(0, len(self.list)): self.list[i].update({'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list
		
    def Aries(self, url):
        if url == None:
            self.list = cache.get(self.imdb_person_list, 24, self.listAries_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)

        for i in range(0, len(self.list)): self.list[i].update({'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list
		
    def Taurus(self, url):

        if url == None:
            self.list = cache.get(self.imdb_person_list, 24, self.listTaurus_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)

        for i in range(0, len(self.list)): self.list[i].update({'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list
		
    def Gemini(self, url):

        if url == None:
            self.list = cache.get(self.imdb_person_list, 24, self.listGemini_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)

        for i in range(0, len(self.list)): self.list[i].update({'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list
		
    def Cancer(self, url):	 

        if url == None:
            self.list = cache.get(self.imdb_person_list, 24, self.listCancer_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)

        for i in range(0, len(self.list)): self.list[i].update({'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list
		
    def Leo(self, url):	 

        if url == None:
            self.list = cache.get(self.imdb_person_list, 24, self.listLeo_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)

        for i in range(0, len(self.list)): self.list[i].update({'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list

    def Virgo(self, url):

        if url == None:
            self.list = cache.get(self.imdb_person_list, 24, self.listVirgo_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)

        for i in range(0, len(self.list)): self.list[i].update({'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list
		
    def Libra(self, url):

        if url == None:
            self.list = cache.get(self.imdb_person_list, 24, self.listLibra_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)

        for i in range(0, len(self.list)): self.list[i].update({'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list

    def Sagittarius(self, url):
        if url == None:
            self.list = cache.get(self.imdb_person_list, 24, self.listSagittarius_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)

        for i in range(0, len(self.list)): self.list[i].update({'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list
		
    def Capricorn(self, url):
        if url == None:
            self.list = cache.get(self.imdb_person_list, 24, self.Capricornlist_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)

        for i in range(0, len(self.list)): self.list[i].update({'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list

    def scorpio(self, url):
        if url == None:
            self.list = cache.get(self.imdb_person_list, 24, self.listscorpio_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)



    def persons(self, url):
        if url == None:
            self.list = cache.get(self.imdb_person_list, 24, self.personlist_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)

        for i in range(0, len(self.list)): self.list[i].update({'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def userlists(self):
        try:
            userlists = []
            if trakt.getTraktCredentialsInfo() == False: raise Exception()
            activity = trakt.getActivity()
        except:
            pass

        try:
            if trakt.getTraktCredentialsInfo() == False: raise Exception()
            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlists_link, self.trakt_user): raise Exception()
                userlists += cache.get(self.trakt_user_list, 720, self.traktlists_link, self.trakt_user)
            except:
                userlists += cache.get(self.trakt_user_list, 0, self.traktlists_link, self.trakt_user)
        except:
            pass
        try:
            self.list = []
            if self.imdb_user == '': raise Exception()
            userlists += cache.get(self.imdb_user_list, 0, self.imdblists_link)
        except:
            pass
        try:
            self.list = []
            if trakt.getTraktCredentialsInfo() == False: raise Exception()
            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlikedlists_link, self.trakt_user): raise Exception()
                userlists += cache.get(self.trakt_user_list, 720, self.traktlikedlists_link, self.trakt_user)
            except:
                userlists += cache.get(self.trakt_user_list, 0, self.traktlikedlists_link, self.trakt_user)
        except:
            pass

        self.list = userlists
        for i in range(0, len(self.list)): self.list[i].update({'image': 'userlists.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def trakt_list(self, url, user):
        try:
            dupes = []

            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            q.update({'extended': 'full'})
            q = (urllib.urlencode(q)).replace('%2C', ',')
            u = url.replace('?' + urlparse.urlparse(url).query, '') + '?' + q

            result = trakt.getTraktAsJson(u)

            items = []
            for i in result:
                try: items.append(i['show'])
                except: pass
            if len(items) == 0:
                items = result
        except:
            return

        try:
            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            if not int(q['limit']) == len(items): raise Exception()
            q.update({'page': str(int(q['page']) + 1)})
            q = (urllib.urlencode(q)).replace('%2C', ',')
            next = url.replace('?' + urlparse.urlparse(url).query, '') + '?' + q
            next = next.encode('utf-8')
        except:
            next = ''

        for item in items:
            try:
                title = item['title']
                title = re.sub('\s(|[(])(UK|US|AU|\d{4})(|[)])$', '', title)
                title = client.replaceHTMLCodes(title)

                year = item['year']
                year = re.sub('[^0-9]', '', str(year))

                if int(year) > int((self.datetime).strftime('%Y')): raise Exception()

                imdb = item['ids']['imdb']
                if imdb == None or imdb == '': imdb = '0'
                else: imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))

                tvdb = item['ids']['tvdb']
                tvdb = re.sub('[^0-9]', '', str(tvdb))

                if tvdb == None or tvdb == '' or tvdb in dupes: raise Exception()
                dupes.append(tvdb)

                try: premiered = item['first_aired']
                except: premiered = '0'
                try: premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except: premiered = '0'

                try: studio = item['network']
                except: studio = '0'
                if studio == None: studio = '0'

                try: genre = item['genres']
                except: genre = '0'
                genre = [i.title() for i in genre]
                if genre == []: genre = '0'
                genre = ' / '.join(genre)

                try: duration = str(item['runtime'])
                except: duration = '0'
                if duration == None: duration = '0'

                try: rating = str(item['rating'])
                except: rating = '0'
                if rating == None or rating == '0.0': rating = '0'

                try: votes = str(item['votes'])
                except: votes = '0'
                try: votes = str(format(int(votes),',d'))
                except: pass
                if votes == None: votes = '0'

                try: mpaa = item['certification']
                except: mpaa = '0'
                if mpaa == None: mpaa = '0'

                try: plot = item['overview']
                except: plot = '0'
                if plot == None: plot = '0'
                plot = client.replaceHTMLCodes(plot)

                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'plot': plot, 'imdb': imdb, 'tvdb': tvdb, 'poster': '0', 'next': next})
            except:
                pass

        return self.list


    def trakt_user_list(self, url, user):
        try:
            items = trakt.getTraktAsJson(url)
        except:
            pass

        for item in items:
            try:
                try: name = item['list']['name']
                except: name = item['name']
                name = client.replaceHTMLCodes(name)

                try: url = (trakt.slug(item['list']['user']['username']), item['list']['ids']['slug'])
                except: url = ('me', item['ids']['slug'])
                url = self.traktlist_link % url
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass

        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
        return self.list


    def imdb_list(self, url):
        try:
            dupes = []

            for i in re.findall('date\[(\d+)\]', url):
                url = url.replace('date[%s]' % i, (self.datetime - datetime.timedelta(days = int(i))).strftime('%Y-%m-%d'))

            def imdb_watchlist_id(url):
                return client.parseDOM(client.request(url), 'meta', ret='content', attrs = {'property': 'pageId'})[0]

            if url == self.imdbwatchlist_link:
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdblist_link % url

            elif url == self.imdbwatchlist2_link:
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdblist2_link % url

            result = client.request(url)

            result = result.replace('\n', ' ')

            items = client.parseDOM(result, 'div', attrs = {'class': 'lister-item .+?'})
            items += client.parseDOM(result, 'div', attrs = {'class': 'list_item.+?'})
        except:
            return

        try:
            next = client.parseDOM(result, 'a', ret='href', attrs = {'class': 'lister-page-next next-page'})

            if len(next) == 0:
                next = client.parseDOM(result, 'div', attrs = {'class': 'pagination'})[0]
                next = zip(client.parseDOM(next, 'a', ret='href'), client.parseDOM(next, 'a'))
                next = [i[0] for i in next if 'Next' in i[1]]

            next = url.replace(urlparse.urlparse(url).query, urlparse.urlparse(next[0]).query)
            next = client.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for item in items:
            try:
                title = client.parseDOM(item, 'a')[1]
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = client.parseDOM(item, 'span', attrs = {'class': 'lister-item-year.+?'})
                year += client.parseDOM(item, 'span', attrs = {'class': 'year_type'})
                year = re.findall('(\d{4})', year[0])[0]
                year = year.encode('utf-8')

                if int(year) > int((self.datetime).strftime('%Y')): raise Exception()

                imdb = client.parseDOM(item, 'a', ret='href')[0]
                imdb = re.findall('(tt\d*)', imdb)[0]
                imdb = imdb.encode('utf-8')

                if imdb in dupes: raise Exception()
                dupes.append(imdb)

                try: poster = client.parseDOM(item, 'img', ret='loadlate')[0]
                except: poster = '0'
                if '/nopicture/' in poster: poster = '0'
                poster = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', poster)
                poster = client.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                rating = '0'
                try: rating = client.parseDOM(item, 'span', attrs = {'class': 'rating-rating'})[0]
                except: pass
                try: rating = client.parseDOM(rating, 'span', attrs = {'class': 'value'})[0]
                except: rating = '0'
                try: rating = client.parseDOM(item, 'div', ret='data-value', attrs = {'class': '.*?imdb-rating'})[0]
                except: pass
                if rating == '' or rating == '-': rating = '0'
                rating = client.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                plot = '0'
                try: plot = client.parseDOM(item, 'p', attrs = {'class': 'text-muted'})[0]
                except: pass
                try: plot = client.parseDOM(item, 'div', attrs = {'class': 'item_description'})[0]
                except: pass
                plot = plot.rsplit('<span>', 1)[0].strip()
                plot = re.sub('<.+?>|</.+?>', '', plot)
                if plot == '': plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'rating': rating, 'plot': plot, 'imdb': imdb, 'tvdb': '0', 'poster': poster, 'next': next})
            except:
                pass

        return self.list


    def imdb_person_list(self, url):
        try:
            result = client.request(url)
            items = client.parseDOM(result, 'div', attrs = {'class': '.+? mode-detail'})
        except:
            return

        for item in items:
            try:
                name = client.parseDOM(item, 'img', ret='alt')[0]
                name = client.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = re.findall('(nm\d*)', url, re.I)[0]
                url = self.person_link % url
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = client.parseDOM(item, 'img', ret='src')[0]
                #if not ('._SX' in image or '._SY' in image): raise Exception()
                #image = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', image)
                image = client.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list


    def imdb_user_list(self, url):
        try:
            result = client.request(url)
            items = client.parseDOM(result, 'li', attrs = {'class': 'ipl-zebra-list__item user-list'})
        except:
            pass

        for item in items:
            try:
                name = client.parseDOM(item, 'a')[0]
                name = client.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = url = url.split('/list/', 1)[-1].strip('/')
                url = self.imdblist_link % url
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass

        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
        return self.list


    def tvmaze_list(self, url):
        try:
            result = client.request(url)
            result = client.parseDOM(result, 'section', attrs = {'id': 'this-seasons-shows'})

            items = client.parseDOM(result, 'div', attrs = {'class': 'content auto cell'})
            items = [client.parseDOM(i, 'a', ret='href') for i in items]
            items = [i[0] for i in items if len(i) > 0]
            items = [re.findall('/(\d+)/', i) for i in items]
            items = [i[0] for i in items if len(i) > 0]
            items = items[:50]
        except:
            return

        def items_list(i):
            try:
                url = self.tvmaze_info_link % i

                item = client.request(url)
                item = json.loads(item)

                title = item['name']
                title = re.sub('\s(|[(])(UK|US|AU|\d{4})(|[)])$', '', title)
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = item['premiered']
                year = re.findall('(\d{4})', year)[0]
                year = year.encode('utf-8')

                if int(year) > int((self.datetime).strftime('%Y')): raise Exception()

                imdb = item['externals']['imdb']
                if imdb == None or imdb == '': imdb = '0'
                else: imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                tvdb = item['externals']['thetvdb']
                tvdb = re.sub('[^0-9]', '', str(tvdb))
                tvdb = tvdb.encode('utf-8')

                if tvdb == None or tvdb == '': raise Exception()
 
                try: poster = item['image']['original']
                except: poster = '0'
                if poster == None or poster == '': poster = '0'
                poster = poster.encode('utf-8')

                premiered = item['premiered']
                try: premiered = re.findall('(\d{4}-\d{2}-\d{2})', premiered)[0]
                except: premiered = '0'
                premiered = premiered.encode('utf-8')

                try: studio = item['network']['name']
                except: studio = '0'
                if studio == None: studio = '0'
                studio = studio.encode('utf-8')

                try: genre = item['genres']
                except: genre = '0'
                genre = [i.title() for i in genre]
                if genre == []: genre = '0'
                genre = ' / '.join(genre)
                genre = genre.encode('utf-8')

                try: duration = item['runtime']
                except: duration = '0'
                if duration == None: duration = '0'
                duration = str(duration)
                duration = duration.encode('utf-8')

                try: rating = item['rating']['average']
                except: rating = '0'
                if rating == None or rating == '0.0': rating = '0'
                rating = str(rating)
                rating = rating.encode('utf-8')

                try: plot = item['summary']
                except: plot = '0'
                if plot == None: plot = '0'
                plot = re.sub('<.+?>|</.+?>|\n', '', plot)
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                try: content = item['type'].lower()
                except: content = '0'
                if content == None or content == '': content = '0'
                content = content.encode('utf-8')

                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'plot': plot, 'imdb': imdb, 'tvdb': tvdb, 'poster': poster, 'content': content})
            except:
                pass

        try:
            threads = []
            for i in items: threads.append(workers.Thread(items_list, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

            filter = [i for i in self.list if i['content'] == 'scripted']
            filter += [i for i in self.list if not i['content'] == 'scripted']
            self.list = filter

            return self.list
        except:
            return


    def worker(self, level=1):
        self.meta = []
        total = len(self.list)

        self.fanart_tv_headers = {'api-key': 'YTc2MGMyMTEzYTM1OTk5NzFiN2FjMWU0OWUzMTAyMGQ='.decode('base64')}
        if not self.fanart_tv_user == '':
            self.fanart_tv_headers.update({'client-key': self.fanart_tv_user})

        for i in range(0, total): self.list[i].update({'metacache': False})

        self.list = metacache.fetch(self.list, self.lang, self.user)

        for r in range(0, total, 40):
            threads = []
            for i in range(r, r+40):
                if i <= total: threads.append(workers.Thread(self.super_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

            if self.meta: metacache.insert(self.meta)

        self.list = [i for i in self.list if not i['tvdb'] == '0']

        if self.fanart_tv_user == '':
            for i in self.list: i.update({'clearlogo': '0', 'clearart': '0'})


    def super_info(self, i):
        try:
            if self.list[i]['metacache'] == True: raise Exception()

            imdb = self.list[i]['imdb'] if 'imdb' in self.list[i] else '0'
            tvdb = self.list[i]['tvdb'] if 'tvdb' in self.list[i] else '0'

            if imdb == '0':
                try:
                    imdb = trakt.SearchTVShow(urllib.quote_plus(self.list[i]['title']), self.list[i]['year'], full=False)[0]
                    imdb = imdb.get('show', '0')
                    imdb = imdb.get('ids', {}).get('imdb', '0')
                    imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))

                    if not imdb: imdb = '0'
                except:
                    imdb = '0'

            if tvdb == '0' and not imdb == '0':
                url = self.tvdb_by_imdb % imdb

                result = client.request(url, timeout='10')

                try: tvdb = client.parseDOM(result, 'seriesid')[0]
                except: tvdb = '0'

                try: name = client.parseDOM(result, 'SeriesName')[0]
                except: name = '0'
                dupe = re.findall('[***]Duplicate (\d*)[***]', name)
                if dupe: tvdb = str(dupe[0])

                if tvdb == '': tvdb = '0'


            if tvdb == '0':
                url = self.tvdb_by_query % (urllib.quote_plus(self.list[i]['title']))

                years = [str(self.list[i]['year']), str(int(self.list[i]['year'])+1), str(int(self.list[i]['year'])-1)]

                tvdb = client.request(url, timeout='10')
                tvdb = re.sub(r'[^\x00-\x7F]+', '', tvdb)
                tvdb = client.replaceHTMLCodes(tvdb)
                tvdb = client.parseDOM(tvdb, 'Series')
                tvdb = [(x, client.parseDOM(x, 'SeriesName'), client.parseDOM(x, 'FirstAired')) for x in tvdb]
                tvdb = [(x, x[1][0], x[2][0]) for x in tvdb if len(x[1]) > 0 and len(x[2]) > 0]
                tvdb = [x for x in tvdb if cleantitle.get(self.list[i]['title']) == cleantitle.get(x[1])]
                tvdb = [x[0][0] for x in tvdb if any(y in x[2] for y in years)][0]
                tvdb = client.parseDOM(tvdb, 'seriesid')[0]

                if tvdb == '': tvdb = '0'


            url = self.tvdb_info_link % tvdb
            item = client.request(url, timeout='10')
            if item == None: raise Exception()

            if imdb == '0':
                try: imdb = client.parseDOM(item, 'IMDB_ID')[0]
                except: pass
                if imdb == '': imdb = '0'
                imdb = imdb.encode('utf-8')


            try: title = client.parseDOM(item, 'SeriesName')[0]
            except: title = ''
            if title == '': title = '0'
            title = client.replaceHTMLCodes(title)
            title = title.encode('utf-8')

            try: year = client.parseDOM(item, 'FirstAired')[0]
            except: year = ''
            try: year = re.compile('(\d{4})').findall(year)[0]
            except: year = ''
            if year == '': year = '0'
            year = year.encode('utf-8')

            try: premiered = client.parseDOM(item, 'FirstAired')[0]
            except: premiered = '0'
            if premiered == '': premiered = '0'
            premiered = client.replaceHTMLCodes(premiered)
            premiered = premiered.encode('utf-8')

            try: studio = client.parseDOM(item, 'Network')[0]
            except: studio = ''
            if studio == '': studio = '0'
            studio = client.replaceHTMLCodes(studio)
            studio = studio.encode('utf-8')

            try: genre = client.parseDOM(item, 'Genre')[0]
            except: genre = ''
            genre = [x for x in genre.split('|') if not x == '']
            genre = ' / '.join(genre)
            if genre == '': genre = '0'
            genre = client.replaceHTMLCodes(genre)
            genre = genre.encode('utf-8')

            try: duration = client.parseDOM(item, 'Runtime')[0]
            except: duration = ''
            if duration == '': duration = '0'
            duration = client.replaceHTMLCodes(duration)
            duration = duration.encode('utf-8')

            try: rating = client.parseDOM(item, 'Rating')[0]
            except: rating = ''
            if 'rating' in self.list[i] and not self.list[i]['rating'] == '0':
                rating = self.list[i]['rating']
            if rating == '': rating = '0'
            rating = client.replaceHTMLCodes(rating)
            rating = rating.encode('utf-8')

            try: votes = client.parseDOM(item, 'RatingCount')[0]
            except: votes = ''
            if 'votes' in self.list[i] and not self.list[i]['votes'] == '0':
                votes = self.list[i]['votes']
            if votes == '': votes = '0'
            votes = client.replaceHTMLCodes(votes)
            votes = votes.encode('utf-8')

            try: mpaa = client.parseDOM(item, 'ContentRating')[0]
            except: mpaa = ''
            if mpaa == '': mpaa = '0'
            mpaa = client.replaceHTMLCodes(mpaa)
            mpaa = mpaa.encode('utf-8')

            try: cast = client.parseDOM(item, 'Actors')[0]
            except: cast = ''
            cast = [x for x in cast.split('|') if not x == '']
            try: cast = [(x.encode('utf-8'), '') for x in cast]
            except: cast = []
            if cast == []: cast = '0'

            try: plot = client.parseDOM(item, 'Overview')[0]
            except: plot = ''
            if plot == '': plot = '0'
            plot = client.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')

            try: poster = client.parseDOM(item, 'poster')[0]
            except: poster = ''
            if not poster == '': poster = self.tvdb_image + poster
            else: poster = '0'
            if 'poster' in self.list[i] and poster == '0': poster = self.list[i]['poster']
            poster = client.replaceHTMLCodes(poster)
            poster = poster.encode('utf-8')

            try: banner = client.parseDOM(item, 'banner')[0]
            except: banner = ''
            if not banner == '': banner = self.tvdb_image + banner
            else: banner = '0'
            banner = client.replaceHTMLCodes(banner)
            banner = banner.encode('utf-8')

            try: fanart = client.parseDOM(item, 'fanart')[0]
            except: fanart = ''
            if not fanart == '': fanart = self.tvdb_image + fanart
            else: fanart = '0'
            fanart = client.replaceHTMLCodes(fanart)
            fanart = fanart.encode('utf-8')

            try:
                artmeta = True
                #if self.fanart_tv_user == '': raise Exception()
                art = client.request(self.fanart_tv_art_link % tvdb, headers=self.fanart_tv_headers, timeout='10', error=True)
                try: art = json.loads(art)
                except: artmeta = False
            except:
                pass

            try:
                poster2 = art['tvposter']
                poster2 = [x for x in poster2 if x.get('lang') == self.lang][::-1] + [x for x in poster2 if x.get('lang') == 'en'][::-1] + [x for x in poster2 if x.get('lang') in ['00', '']][::-1]
                poster2 = poster2[0]['url'].encode('utf-8')
            except:
                poster2 = '0'

            try:
                fanart2 = art['showbackground']
                fanart2 = [x for x in fanart2 if x.get('lang') == self.lang][::-1] + [x for x in fanart2 if x.get('lang') == 'en'][::-1] + [x for x in fanart2 if x.get('lang') in ['00', '']][::-1]
                fanart2 = fanart2[0]['url'].encode('utf-8')
            except:
                fanart2 = '0'

            try:
                banner2 = art['tvbanner']
                banner2 = [x for x in banner2 if x.get('lang') == self.lang][::-1] + [x for x in banner2 if x.get('lang') == 'en'][::-1] + [x for x in banner2 if x.get('lang') in ['00', '']][::-1]
                banner2 = banner2[0]['url'].encode('utf-8')
            except:
                banner2 = '0'

            try:
                if 'hdtvlogo' in art: clearlogo = art['hdtvlogo']
                else: clearlogo = art['clearlogo']
                clearlogo = [x for x in clearlogo if x.get('lang') == self.lang][::-1] + [x for x in clearlogo if x.get('lang') == 'en'][::-1] + [x for x in clearlogo if x.get('lang') in ['00', '']][::-1]
                clearlogo = clearlogo[0]['url'].encode('utf-8')
            except:
                clearlogo = '0'

            try:
                if 'hdclearart' in art: clearart = art['hdclearart']
                else: clearart = art['clearart']
                clearart = [x for x in clearart if x.get('lang') == self.lang][::-1] + [x for x in clearart if x.get('lang') == 'en'][::-1] + [x for x in clearart if x.get('lang') in ['00', '']][::-1]
                clearart = clearart[0]['url'].encode('utf-8')
            except:
                clearart = '0'

            item = {'title': title, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'poster': poster, 'poster2': poster2, 'banner': banner, 'banner2': banner2, 'fanart': fanart, 'fanart2': fanart2, 'clearlogo': clearlogo, 'clearart': clearart, 'premiered': premiered, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'cast': cast, 'plot': plot}
            item = dict((k,v) for k, v in item.iteritems() if not v == '0')
            self.list[i].update(item)

            if artmeta == False: raise Exception()

            meta = {'imdb': imdb, 'tvdb': tvdb, 'lang': self.lang, 'user': self.user, 'item': item}
            self.meta.append(meta)
        except:
            pass


    def tvshowDirectory(self, items):
        if items == None or len(items) == 0: control.idle() ; sys.exit()

        sysaddon = sys.argv[0]

        syshandle = int(sys.argv[1])

        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()

        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')

        traktCredentials = trakt.getTraktCredentialsInfo()

        try: isOld = False ; control.item().getArt('type')
        except: isOld = True

        indicators = playcount.getTVShowIndicators(refresh=True) if action == 'tvshows' else playcount.getTVShowIndicators()

        flatten = True if control.setting('flatten.tvshows') == 'true' else False

        watchedMenu = control.lang(32068).encode('utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(32066).encode('utf-8')

        unwatchedMenu = control.lang(32069).encode('utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(32067).encode('utf-8')

        queueMenu = control.lang(32065).encode('utf-8')

        traktManagerMenu = control.lang(32070).encode('utf-8')

        nextMenu = control.lang(32053).encode('utf-8')

        playRandom = control.lang(32535).encode('utf-8')

        addToLibrary = control.lang(32551).encode('utf-8')

        for i in items:
            try:
                label = i['title']
                systitle = sysname = urllib.quote_plus(i['originaltitle'])
                sysimage = urllib.quote_plus(i['poster'])
                imdb, tvdb, year = i['imdb'], i['tvdb'], i['year']

                meta = dict((k,v) for k, v in i.iteritems() if not v == '0')
                meta.update({'code': imdb, 'imdbnumber': imdb, 'imdb_id': imdb})
                meta.update({'tvdb_id': tvdb})
                meta.update({'mediatype': 'tvshow'})
                meta.update({'trailer': '%s?action=trailer&name=%s' % (sysaddon, urllib.quote_plus(label))})
                if not 'duration' in i: meta.update({'duration': '60'})
                elif i['duration'] == '0': meta.update({'duration': '60'})
                try: meta.update({'duration': str(int(meta['duration']) * 60)})
                except: pass
                try: meta.update({'genre': cleangenre.lang(meta['genre'], self.lang)})
                except: pass

                try:
                    overlay = int(playcount.getTVShowOverlay(indicators, tvdb))
                    if overlay == 7: meta.update({'playcount': 1, 'overlay': 7})
                    else: meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass


                if flatten == True:
                    url = '%s?action=episodes&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s' % (sysaddon, systitle, year, imdb, tvdb)
                else:
                    url = '%s?action=seasons&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s' % (sysaddon, systitle, year, imdb, tvdb)


                cm = []

                cm.append((playRandom, 'RunPlugin(%s?action=random&rtype=season&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s)' % (sysaddon, urllib.quote_plus(systitle), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(tvdb))))

                cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))

                cm.append((watchedMenu, 'RunPlugin(%s?action=tvPlaycount&name=%s&imdb=%s&tvdb=%s&query=7)' % (sysaddon, systitle, imdb, tvdb)))

                cm.append((unwatchedMenu, 'RunPlugin(%s?action=tvPlaycount&name=%s&imdb=%s&tvdb=%s&query=6)' % (sysaddon, systitle, imdb, tvdb)))

                if traktCredentials == True:
                    cm.append((traktManagerMenu, 'RunPlugin(%s?action=traktManager&name=%s&tvdb=%s&content=tvshow)' % (sysaddon, sysname, tvdb)))

                if isOld == True:
                    cm.append((control.lang2(19033).encode('utf-8'), 'Action(Info)'))

                cm.append((addToLibrary, 'RunPlugin(%s?action=tvshowToLibrary&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s)' % (sysaddon, systitle, year, imdb, tvdb)))

                item = control.item(label=label)

                art = {}

                if 'poster' in i and not i['poster'] == '0':
                    art.update({'icon': i['poster'], 'thumb': i['poster'], 'poster': i['poster']})
                #elif 'poster2' in i and not i['poster2'] == '0':
                    #art.update({'icon': i['poster2'], 'thumb': i['poster2'], 'poster': i['poster2']})
                else:
                    art.update({'icon': addonPoster, 'thumb': addonPoster, 'poster': addonPoster})

                if 'banner' in i and not i['banner'] == '0':
                    art.update({'banner': i['banner']})
                #elif 'banner2' in i and not i['banner2'] == '0':
                    #art.update({'banner': i['banner2']})
                elif 'fanart' in i and not i['fanart'] == '0':
                    art.update({'banner': i['fanart']})
                else:
                    art.update({'banner': addonBanner})

                if 'clearlogo' in i and not i['clearlogo'] == '0':
                    art.update({'clearlogo': i['clearlogo']})

                if 'clearart' in i and not i['clearart'] == '0':
                    art.update({'clearart': i['clearart']})

                if settingFanart == 'true' and 'fanart' in i and not i['fanart'] == '0':
                    item.setProperty('Fanart_Image', i['fanart'])
                #elif settingFanart == 'true' and 'fanart2' in i and not i['fanart2'] == '0':
                    #item.setProperty('Fanart_Image', i['fanart2'])
                elif not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)

                item.setArt(art)
                item.addContextMenuItems(cm)
                item.setInfo(type='Video', infoLabels = meta)

                video_streaminfo = {'codec': 'h264'}
                item.addStreamInfo('video', video_streaminfo)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                pass

        try:
            url = items[0]['next']
            if url == '': raise Exception()

            icon = control.addonNext()
            url = '%s?action=tvshowPage&url=%s' % (sysaddon, urllib.quote_plus(url))

            item = control.item(label=nextMenu)

            item.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': icon})
            if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)

            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
        except:
            pass

        control.content(syshandle, 'tvshows')
        control.directory(syshandle, cacheToDisc=True)
        views.setView('tvshows', {'skin.estuary': 55, 'skin.confluence': 500})


    def addDirectory(self, items, queue=False):
        if items == None or len(items) == 0: control.idle() ; sys.exit()

        sysaddon = sys.argv[0]

        syshandle = int(sys.argv[1])

        addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()

        queueMenu = control.lang(32065).encode('utf-8')

        playRandom = control.lang(32535).encode('utf-8')

        addToLibrary = control.lang(32551).encode('utf-8')

        for i in items:
            try:
                name = i['name']

                if i['image'].startswith('http'): thumb = i['image']
                elif not artPath == None: thumb = os.path.join(artPath, i['image'])
                else: thumb = addonThumb

                url = '%s?action=%s' % (sysaddon, i['action'])
                try: url += '&url=%s' % urllib.quote_plus(i['url'])
                except: pass

                cm = []

                cm.append((playRandom, 'RunPlugin(%s?action=random&rtype=show&url=%s)' % (sysaddon, urllib.quote_plus(i['url']))))

                if queue == True:
                    cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))

                try: cm.append((addToLibrary, 'RunPlugin(%s?action=tvshowsToLibrary&url=%s)' % (sysaddon, urllib.quote_plus(i['context']))))
                except: pass

                item = control.item(label=name)

                item.setArt({'icon': thumb, 'thumb': thumb})
                if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)

                item.addContextMenuItems(cm)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                pass

        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)


