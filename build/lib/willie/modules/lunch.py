# -*- coding: utf-8 -*-
"""
lunch.py - Willie JAMK Lunch-list Parser Module
copyright © 2013 kamilla @ quakeket <admin@kamillaproductions.com>
Licenced under Apache Licence, Version 2.0
"""
from datetime import datetime
from lxml.html import parse
from willie.module import commands, example

def get_lunch(*weekday):
	if len(weekday)>0:
		today = weekday[0]
	else:
		today = datetime.now().weekday()
	url = 'http://www.jamk.fi/fi/Palvelut/Tilavuokraus-ja-ravintolapalvelut/Ravintolapalvelut/Ravintola-Dynamo-lounaslista/'
	day = [[] for i in range(5)]
	html = parse(url).getroot()
	inner = html.xpath('//*[@id="Content_Content_ctl00_mainbodypanel"]/div/div')
	phase = -1
	for b in inner:
		for a in b.cssselect('p'):
			if a.text_content().strip().startswith('Maanantai'):
				phase = 0
			if a.text_content().strip().startswith('Tiistai'):
				phase = 1
			if a.text_content().strip().startswith('Keskiviikko'):
				phase = 2
			if a.text_content().strip().startswith('Torstai'):
				phase = 3
			if a.text_content().strip().startswith('Perjantai'):
				phase = 4
			if a.text_content().strip().startswith('Monday'):
				phase = -1
			if phase>=0:
				day[phase].append(a.text_content().strip())
	return '[LOUNAS] ' + ', '.join(day[today][:])

@commands('f','food')
@example('.f [weekday] (weekday: ma, ti, ke, to, pe)')
def food(bot, trigger):
	if not trigger.group(2):
		if datetime.now().weekday()>4:
			bot.reply('Koulu on kiinni köppä')
		else:
			bot.say(get_lunch())
	elif trigger.group(2)=='ma':
		bot.say(get_lunch(0))
	elif trigger.group(2)=='ti':
		bot.say(get_lunch(1))
	elif trigger.group(2)=='ke':
		bot.say(get_lunch(2))
	elif trigger.group(2)=='to':
		bot.say(get_lunch(3))
	elif trigger.group(2)=='pe':
		bot.say(get_lunch(4))
	else:
		bot.reply('Virheellinen viikonpäivä')

