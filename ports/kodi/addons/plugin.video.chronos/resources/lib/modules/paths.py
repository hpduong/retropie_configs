import koding
import os 
from koding import Addon_Info


#Addon paths
''' author, changelog, description, disclaimer, fanart, icon, id, name,
    path, profile, stars, summary, type, version'''

addon             = Addon_Info(id='name')
addon_path        = Addon_Info(id='path')
icon              = Addon_Info(id='icon')
fanart            = Addon_Info(id='fanart')
profile_path      = Addon_Info(id='profile')#path as special
real_profile_path = koding.Physical_Path(profile_path) # path as real c://kodi 
koding.dolog('addon= %s addon_path= %s icon= %s fanart= %s profile_path= %s real_profile_path= %s'%(addon,addon_path,icon,fanart,profile_path,real_profile_path),line_info=True)


#Folder paths







#File Paths
CACHE_DB = os.path.join(real_profile_path,'cache.db')
