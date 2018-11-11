import xbmc
import xbmcaddon
import xbmcgui
 
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')

settings = xbmcaddon.Addon(id='script.tooontown.Greeting')
df = settings.getSetting("user")
if settings:
    line1 = "Welcome To ToonTown!"
    line2 = "Nice to meet you %s" % df
    line3 = "Watch Out For Falling Safes!"

    xbmcgui.Dialog().ok(addonname, line1, line2, line3) 
