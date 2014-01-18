# -*- coding: utf-8 -*-
"""
oracle.py - JamBot Oraakkeli Module
copyright © 2014 Kamilla Productions Uninc.
- kamilla @ quakeket <admin@kamillaproductions.com>
Licenced under Apache Licence, Version 2.0
---------------------------------------------------
using Willie - The Python IRC Bot -project of Nerdfighteria Network
with Oraakkeli - Kaikkitietävä Oraakkeli at http://www.oraakkeli.biz/
"""

import urllib
import urllib2
from lxml.html import parse
from willie.module import commands, example

url = 'http://www.oraakkeli.biz/#v'

@commands('o','oraakkeli','oracle')
@example('.o Paljonko kello on?')
def oracle(bot, trigger):
	"""Oraakkeli, jolta voit kysyä ihan mitä vaan! esim. [.o Mikä on elämän tarkoitus?]"""
	command = trigger.group(2)
	if command is None:
		bot.reply('Unohdit kysymyksen köppä. :f')
		return
	values = {'kysymys' : command.encode('utf-8'), 'ok' : '1' }
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	html = parse(response)
	inner = html.xpath('//*[@id="vastaus"]/i[2]')
	vastaus = inner[0].text_content()
	bot.reply(vastaus)
	response.close()
