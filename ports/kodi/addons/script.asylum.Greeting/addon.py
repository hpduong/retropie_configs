import xbmc
import xbmcaddon
import xbmcgui
 
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')

settings = xbmcaddon.Addon(id='script.asylum.Greeting')
df = settings.getSetting("user")
if settings:
    line1 = "Welcome To Your Padded Cell!"
    line2 = "Nice to meet you %s" % df
    line3 = "Welcome To The Asylum!"

    xbmcgui.Dialog().ok(addonname, line1, line2, line3) 
