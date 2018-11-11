
import sys
import xbmcplugin

def get_setting(setting):
	Setting = xbmcplugin.getSetting(int(sys.argv[1]), setting)
	return Setting

DEBUG      = get_setting( 'debug')
DEVMODE    = get_setting('dev_mode')
LOGIN_PREF = get_setting( 'loggin_prefernce')
PASSWORD   = get_setting( 'password')
USERNAME   = get_setting( 'username')

