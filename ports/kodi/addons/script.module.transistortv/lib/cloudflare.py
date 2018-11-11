
#
#      Copyright (C) 2015 tknorris (Derived from Mikey1234's & Lambda's)
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
#  This code is a derivative of the YouTube plugin for XBMC and associated works
#  released under the terms of the GNU General Public License as published by
#  the Free Software Foundation; version 3


import re
import urllib
import log_utils
import kodi
import xbmc
import xbmcgui
import xbmcvfs
from collections import namedtuple

MAX_TRIES = 3
logger = log_utils.Logger.get_logger(__name__)
logger.disable()

def createCookie(url,cj=None,agent='Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0'):
    urlData=''
    try:
        import urlparse,cookielib,urllib2

        class NoRedirection(urllib2.HTTPErrorProcessor):    
            def http_response(self, request, response):
                return response

        def parseJSString(s):
            try:
                offset=1 if s[0]=='+' else 0
                val = int(eval(s.replace('!+[]','1').replace('!![]','1').replace('[]','0').replace('(','str(')[offset:]))
                return val
            except:
                pass

        #agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'
        if cj==None:
            cj = cookielib.CookieJar()

        opener = urllib2.build_opener(NoRedirection, urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-Agent', agent)]
        response = opener.open(url)
        result=urlData = response.read()
        response.close()
#        print result
#        print response.headers
        jschl = re.compile('name="jschl_vc" value="(.+?)"/>').findall(result)[0]

        init = re.compile('setTimeout\(function\(\){\s*.*?.*:(.*?)};').findall(result)[0]
        builder = re.compile(r"challenge-form\'\);\s*(.*)a.v").findall(result)[0]
        decryptVal = parseJSString(init)
        lines = builder.split(';')

        for line in lines:
            if len(line)>0 and '=' in line:
                sections=line.split('=')

                line_val = parseJSString(sections[1])
                decryptVal = int(eval(str(decryptVal)+sections[0][-1]+str(line_val)))

#        print urlparse.urlparse(url).netloc
        answer = decryptVal + len(urlparse.urlparse(url).netloc)

        u='/'.join(url.split('/')[:-1])
        query = '%s/cdn-cgi/l/chk_jschl?jschl_vc=%s&jschl_answer=%s' % (u, jschl, answer)

        if 'type="hidden" name="pass"' in result:
            passval=re.compile('name="pass" value="(.*?)"').findall(result)[0]
            query = '%s/cdn-cgi/l/chk_jschl?pass=%s&jschl_vc=%s&jschl_answer=%s' % (u,urllib.quote_plus(passval), jschl, answer)
            xbmc.sleep(4*1000) ##sleep so that the call work
            
 #       print query
#        import urllib2
#        opener = urllib2.build_opener(NoRedirection,urllib2.HTTPCookieProcessor(cj))
#        opener.addheaders = [('User-Agent', agent)]
        #print opener.headers
        response = opener.open(query)
 #       print response.headers
        #cookie = str(response.headers.get('Set-Cookie'))
        #response = opener.open(url)
        #print cj
#        print response.read()
        response.close()

        return urlData
    except:
        traceback.print_exc(file=sys.stdout)
        return urlData

