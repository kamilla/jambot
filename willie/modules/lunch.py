# -*- coding: utf-8 -*-
"""
lunch.py - Willie JAMK Lunch-list Parser Module
copyright © 2013 kamilla @ quakeket <admin@kamillaproductions.com>
Licenced under Apache Licence, Version 2.0
"""
from datetime import datetime
from lxml.html import parse
from willie.module import commands, example
import codecs

def get_lunch(*weekday):

	#if weekday is not set, then use todays date
	if len(weekday)>0:
		today = weekday[0]
	else:
		today = datetime.now().weekday()

	#page url and array initialization values
	url = 'http://www.jamk.fi/fi/Palvelut/Tilavuokraus-ja-ravintolapalvelut/Ravintolapalvelut/Ravintola-Dynamo-lounaslista/'
	day = [[] for i in range(5)]	#array to hold lunches

	#lets get our url to html
	html = parse(url).getroot()

	#brutehack to swap <br> to ,
	for br in html.xpath("*//br"):
        	br.tail = ", " + br.tail if br.tail else ", "

	#we need only the part containing lunch defs of the page
	inner = html.xpath('//*[@id="Content_Content_ctl00_mainbodypanel"]/div/div')

	#looping for container div
	for b in inner:

		#looping the <p> tags if they are used. retarded JAMK-stuff does every week things differently
		for a in b.cssselect('p'):

			#setting the indexes of starting point of lunch information
			ma = a.text_content().find('Maanantai')
			ti = a.text_content().find('Tiistai')
			ke = a.text_content().find('Keskiviikko')
			to = a.text_content().find('Torstai')
			pe = a.text_content().find('Perjantai')
			weekend = a.text_content().find('Monday')

			#appending lunch info if found
			if ma>=0:
				#if in separate <p> tags
				if ti<0:
					day[0].append(a.text_content()[ma:].replace(","," -",1))
				#if in the same <p> tag
				if ti>=0:
					day[0].append(a.text_content()[ma:ti].replace(","," -",1))
				#setting value to -1 so we know the current days lunch has already been added
				ma = -1
			
			#tuesday
			if ti>=0:
				if ke<0:
					day[1].append(a.text_content()[ti:].replace(","," -",1))
				if ke>=0:
					day[1].append(a.text_content()[ti:ke].replace(","," -",1))
				ti = -1

			#wednesday
			if ke>=0:
				if to<0:
					day[2].append(a.text_content()[ke:].replace(","," -",1))
				if to>=0:
					day[2].append(a.text_content()[ke:to].replace(","," -",1))
				ke = -1

			#thursday
			if to>=0:
				if pe<0:
					day[3].append(a.text_content()[to:].replace(","," -",1))
				if pe>=0:
					day[3].append(a.text_content()[to:pe].replace(","," -",1))
				to = -1

			#friday
			if pe>=0:
				if weekend<0:
					day[4].append(a.text_content()[pe:].replace(","," -",1))
				if weekend>=0:
					day[4].append(a.text_content()[pe:weekend].replace(","," -",1))
				pe = -1

	#returning the wanted information
	return '[LOUNAS] ' + ', '.join(day[today][:])

@commands('f','food')
@example('.f [weekday] (weekday: ma, ti, ke, to, pe)')
def food(bot, trigger):
	"""Finds out whats for lunch for given day."""
	if not trigger.group(2):

		#if trying to use on weekend
		if datetime.now().weekday()>4:
			bot.reply('Koulu on kiinni köppä')
		#gets the lunch for today
		else:
			bot.say(get_lunch())

	#gets the lunch for given day
	elif trigger.group(2).lower()=='ma':
		bot.say(get_lunch(0))
	elif trigger.group(2).lower()=='ti':
		bot.say(get_lunch(1))
	elif trigger.group(2).lower()=='ke':
		bot.say(get_lunch(2))
	elif trigger.group(2).lower()=='to':
		bot.say(get_lunch(3))
	elif trigger.group(2).lower()=='pe':
		bot.say(get_lunch(4))
	else:
		bot.reply('Virheellinen viikonpäivä')

