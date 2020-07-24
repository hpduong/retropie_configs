import xbmc,os

addon_id   = 'script.module.vistatvlive'

icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))

def cat():
    #iplayer()
    addDir('[COLOR white][B]BBC iPlayer[/COLOR][/B]','iplayer',1,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('[COLOR white][B]ITV Player[/COLOR][/B]','itv',1,'http://blog.careco.co.uk/wp-content/uploads/2015/08/x__i0KC0.png',fanart,'')
    #addDir('[COLOR white][B]Tv Catchup[/COLOR][/B]','tvcatchup',1,'http://www.tvcatchup.com/tvcatchup-sm.jpg',fanart,'')
    addDir('[COLOR white][B]Tv Player[/COLOR][/B]','tvplayer',1,'http://www.broadbandtvnews.com/wp-content/uploads/2017/04/TVPlayer.png',fanart,'')

def get(url):
    if url == 'tvplayer':
        tvplayer()
    elif url == 'tvcatchup':
        tvcatchup()
    elif url == 'iplayer':
        iplayer()
    elif url == 'itv':
        itv()
        
    
def tvcatchup():
    import re,string
    open = OPEN_URL('http://tvcatchup.com')
    all  = regex_get_all(open,'<div class="channelsHolder','</div>')
    for a in all:
        name = re.compile('img src.+?alt="(.+?)"').findall(a)[0]
        name = (name).replace('Watch','')
        icon = re.compile('src="(.+?)"').findall(a)[0]
        url  = re.compile('href="(.+?)"').findall(a)[0]
        epg  = re.compile('<br/>(.+?)</a>').findall(a)[0]
        epg  = (epg).replace('amp;','')
        addDir('[B][COLOR white]%s[/COLOR][/B] - %s'%(name,epg),'http://tvcatchup.com'+url,9999,icon,fanart,'')
        
        
        
def tvplayer():
    xbmc.executebuiltin('RunAddon(plugin.video.tvplayer)')
        
        
        

        
def iplayer():
    addDir('BBC One','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/abr_hdtv/ak/bbc_one_hd.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('BBC One Cambridge','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/bbc_one_cambridge.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('BBC One Channel Island','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/bbc_one_channel_islands.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('BBC One East','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/bbc_one_east.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('BBC One East Midlands','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/bbc_one_east_midlands.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('BBC One East Yorkshire','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/bbc_one_east_yorkshire.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('BBC One London','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/bbc_one_london.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('BBC One North East','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/bbc_one_north_east.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('BBC One North West','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/bbc_one_north_west.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('BBC One Northen Ireland','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/abr_hdtv/ak/bbc_one_northern_ireland_hd.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('BBC One Oxford','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/bbc_one_oxford.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('BBC One Scotland','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/abr_hdtv/ak/bbc_one_scotland_hd.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('BBC One South','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/bbc_one_south.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('BBC One South East','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/bbc_one_south_east.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('BBC One South West','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/bbc_one_south_west.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('BBC One Wales','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/abr_hdtv/ak/bbc_one_wales_hd.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('BBC One West','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/bbc_one_west.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('BBC One West Midlands','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/bbc_one_west_midlands.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('BBC One Yorkshire','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/bbc_one_yorks.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')

    addDir('BBC Two','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/abr_hdtv/ak/bbc_two_hd.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('BBC Two Scotland','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/bbc_two_scotland.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('BBC Two Northen Ireland','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/bbc_two_northern_ireland_digital.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('BBC Two Wales','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/bbc_two_wales_digital.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('BBC Two England','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/abr_hdtv/ak/bbc_two_england.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    
    addDir('BBC Four','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/abr_hdtv/ak/bbc_four_hd.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('BBC News','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/abr_hdtv/ak/bbc_news24.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('BBC Parlimant','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/bbc_parliament.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    
    addDir('CBBC','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/abr_hdtv/ak/cbbc_hd.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('CBeebies','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/abr_hdtv/ak/cbeebies_hd.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    
    addDir('Alba','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/bbc_alba.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    addDir('S4C','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/s4cpbs.m3u8',9999,'https://pbs.twimg.com/profile_images/851480480700669952/5ttz9hg1.jpg',fanart,'')
    
    
def itv():
        xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.itv/?iconimage=C%3a%5cUsers%5cbigla%5cAppData%5cRoaming%5cKodi%5caddons%5cplugin.video.itv%5cicon.png&mode=206&name=Live&url=Live")')
    
#def itv():
#        addDir('ITV 1','PlayMedia("plugin://plugin.video.itv/?url=ITV&amp;mode=8&amp;name=ITV+-+%5BCOLOR+orange%5DThis+Morning%5B%2FCOLOR%5D&amp;iconimage=C%3A%5CUsers%5Cbigla%5CAppData%5CRoaming%5CKodi%5Caddons%5Cplugin.video.itv%5Cart%2F2.png")',9999,'http://blog.careco.co.uk/wp-content/uploads/2015/08/x__i0KC0.png',fanart,'')
#        addDir('ITV 2','PlayMedia("plugin://plugin.video.playlistLoader/?logos=&cache=0&name=ITV2&url=https%3A%2F%2Fitv2livedotcom-i.akamaihd.net%2Fhls%2Flive%2F565528%2Fitvlive%2FITV2MN%2Fmain.m3u8%3Fhdnea%3Dst%3D1525357203%7Eexp%3D1525378803%7Eacl%3D%2F%2A%7Edata%3Dnohubplus%7Ehmac%3D93f76afb65443591a7a731e607235e5ac01258818f617e468804fb9c5e04c054&iconimage=&mode=32")',9999,'http://blog.careco.co.uk/wp-content/uploads/2015/08/x__i0KC0.png',fanart,'')
#        addDir('ITV 3','PlayMedia("plugin://plugin.video.playlistLoader/?logos=&cache=0&name=ITV3&url=https%3A%2F%2Fitv3livedotcom-i.akamaihd.net%2Fhls%2Flive%2F565527%2Fitvlive%2FITV3MN%2Fmain.m3u8%3Fhdnea%3Dst%3D1525357317%7Eexp%3D1525378917%7Eacl%3D%2F%2A%7Edata%3Dnohubplus%7Ehmac%3Daf0a822fae2388dcd576c0867210fb360848a02757e4a75530d0d9d3b7e0581d&iconimage=&mode=32")',9999,'http://blog.careco.co.uk/wp-content/uploads/2015/08/x__i0KC0.png',fanart,'')
#        addDir('ITV 4','PlayMedia("plugin://plugin.video.playlistLoader/?logos=&cache=0&name=ITV4&url=https%3A%2F%2Fitv4livedotcom-i.akamaihd.net%2Fhls%2Flive%2F565529%2Fitvlive%2FITV4MN%2Fmain.m3u8%3Fhdnea%3Dst%3D1525357387%7Eexp%3D1525378987%7Eacl%3D%2F%2A%7Edata%3Dnohubplus%7Ehmac%3D07c3eeca1b205769834eeabf713915e59ea915588e339aff1734c5aabde35401&iconimage=&mode=32")',9999,'http://blog.careco.co.uk/wp-content/uploads/2015/08/x__i0KC0.png',fanart,'')
#        addDir('ITV Be','PlayMedia("plugin://plugin.video.playlistLoader/?logos=&cache=0&name=ITV+Be&url=https%3A%2F%2Fitvbelivedotcom-i.akamaihd.net%2Fhls%2Flive%2F565509%2Fitvlive%2FITVBEMN%2Fmain.m3u8%3Fhdnea%3Dst%3D1525357408%7Eexp%3D1525379008%7Eacl%3D%2F%2A%7Edata%3Dnohubplus%7Ehmac%3D30f42debe8b9190d8681d5f5e4b0133ddb5982fc0b7242f260fbf346ce4d6417&iconimage=&mode=32")',9999,'http://blog.careco.co.uk/wp-content/uploads/2015/08/x__i0KC0.png',fanart,'')
#        addDir('CITV','PlayMedia("plugin://plugin.video.playlistLoader/?logos=&cache=0&name=CITV&url=https%3A%2F%2Fcitvlivedotcom-i.akamaihd.net%2Fhls%2Flive%2F565526%2Fitvlive%2FCITVMN%2Fmain.m3u8%3Fhdnea%3Dst%3D1525357429%7Eexp%3D1525379029%7Eacl%3D%2F%2A%7Edata%3Dnohubplus%7Ehmac%3D03086a9a7dcf4e24c48a5853d6ef7fe83740077f43709f7fd0c1eeaeb3c2481b&iconimage=&mode=32")',9999,'http://blog.careco.co.uk/wp-content/uploads/2015/08/x__i0KC0.png',fanart,'')
#        addDir('ITV Sports','PlayMedia("plugin://plugin.video.playlistLoader/?logos=&cache=0&name=ITV+Sports&url=https%3A%2F%2Fitvliveevents-i.akamaihd.net%2Fhls%2Flive%2F203496%2Fitvliveevents%2FITVEVTMN%2Fmain.m3u8&iconimage=&mode=32")',9999,'',fanart,'')
        
                
        
######################################################################################################
        
        
        
def regex_from_to(text, from_string, to_string, excluding=True):
    import re,string
    if excluding:
        try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
        except: r = ''
    else:
        try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
        except: r = ''
    return r


def regex_get_all(text, start_with, end_with):
    import re,string
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r



def OPEN_URL(url):
    import requests
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    link = requests.session().get(url, headers=headers, verify=False).text
    link = link.encode('ascii', 'ignore')
    return link
    
    
    

        
        
def addDir(name,url,mode,iconimage,fanart,description):
    import xbmcgui,xbmcplugin,urllib,sys
    u=sys.argv[0]+"?url="+url+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
    liz.setProperty('fanart_image', fanart)
    if mode==10 or mode==9999:
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    else:
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok
    xbmcplugin.endOfDirectory