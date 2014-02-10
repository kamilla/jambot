# -*- coding: utf-8 -*-
"""
image.py - JamBot Google Image Search Module
copyright © 2014 Kamilla Productions Uninc.
- kamilla @ quakeket <admin@kamillaproductions.com>
Licenced under Apache Licence, Version 2.0
---------------------------------------------------
using Willie - The Python IRC Bot -project of Nerdfighteria Network
with Bing - Using Bing Search API
"""

import urllib
import urllib2
import json
from lxml.html import parse
from willie.module import commands, example

key= 'kmRHxWzkgFde43xLqlqDg1jZ37fmxsTMWt5UU1v8Dk0='
user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'

@commands('i','image')
@example('.i sad kitten')
def oracle(bot, trigger):
        """Bing kuvahaku, laittaa ensimmäisenä tuloksissa olevan linkin"""
        command = trigger.group(2)
        if command is None:
                bot.reply('Unohdit laittaa hakuparametrin köppä :c Kokeile [.i sad kitten]')
                return
        query = command.encode('utf-8')
        bot.say(bing_search(query, 'Image'))

def bing_search(query, search_type):
    try:
        query = urllib.quote(query)
    	credentials = (':%s' % key).encode('base64')[:-1]
    	auth = 'Basic %s' % credentials
    	url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/'+search_type+'?Query=%27'+query+'%27&$top=1&$format=json&Adult=%27Off%27'
    	request = urllib2.Request(url)
    	request.add_header('Authorization', auth)
    	request.add_header('User-Agent', user_agent)
    	request_opener = urllib2.build_opener()
    	response = request_opener.open(request)
    	response_data = response.read()
    	json_result = json.loads(response_data)
    	result_list = json_result['d']['results'][0]['MediaUrl']
    	return result_list
    except:
	return "Evotat huolella, opettele kirjottaa lol"
