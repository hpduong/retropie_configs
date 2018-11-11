import byb_modules as BYB
import koding
import sys
import xbmcplugin
from resources import settings
from resources.lib.modules import paths

def tool_index():
	BYB.addDir_file('[COLOR red]Settings[/COLOR]','',100,paths.icon,paths.fanart,'','','','')
	BYB.addDir_file('[COLOR red]Clear Cached password[/COLOR]','',104,paths.icon,paths.fanart,'','','','')
	koding.dolog(settings.DEVMODE,line_info=True)
	if settings.DEVMODE == 'true':
		BYB.addDir_file('[COLOR red]Dev Mode tester[/COLOR]','',102,paths.icon,paths.fanart,'','','','')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


def del_cache_password():
	BYB.delete_table(filename=paths.CACHE_DB,table='login')
	koding.Notify(title='Loggin Cache', message='Loggin cache successful cleared', icon=paths.icon)
