# -*- coding: utf-8 -*-
"""
gtranslate.py - Wille JAMK Google Translator Module
copyright © 2013 Kamilla Productions Uninc.
- kamilla @ quakeket <admin@kamillaproductions.com>
Licenced under Apache Licence, Version 2.0
---------------------------------------------------
All credits of translating service goes to © 2013 Google Inc.
"""
from willie.module import commands, example
import urllib2
import json

language = ['af', 'sq', 'ar', 'az', 'eu', 'bn', 'be', 'bg', 'ca', 'zh-CN', 'zh-TW', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et', 'tl', 'fi', 'fr', 'gl', 'ka', 'de', 'el', 'gu', 'ht', 'iw', 'hi', 'hu', 'is', 'id', 'ga', 'it', 'ja', 'kn', 'ko', 'la', 'lv', 'lt', 'mk', 'ms', 'mt', 'no', 'fa', 'pl', 'pt', 'ro', 'ru', 'sr', 'sk', 'sl', 'es', 'sw', 'sv', 'ta', 'te', 'th', 'tr', 'uk', 'ur', 'vi', 'cy', 'yi']
lang_en = ['afrikaans', 'albanian', 'arabic', 'azerbaijani', 'basque', 'bengali', 'belarusian', 'bulgarian', 'catalan', 'chinese simplified', 'chinese traditional', 'croatian', 'czech', 'danish', 'dutch', 'english', 'esperanto', 'estonian', 'filipino', 'finnish', 'french', 'galician', 'georgian', 'german', 'greek', 'gujarati', 'haitian creole', 'hebrew', 'hindi', 'hungarian', 'icelandic', 'indonesian', 'irish', 'italian', 'japanese', 'kannada', 'korean', 'latin', 'latvian', 'lithuanian', 'macedonian', 'malay', 'maltese', 'norwegian', 'persian', 'polish', 'portuguese', 'romanian', 'russian', 'serbian', 'slovak', 'slovenian', 'spanish', 'swahili', 'swedish', 'tamil', 'telugu', 'thai', 'turkish', 'ukrainian', 'urdu', 'vietnamese', 'welsh', 'yiddish']
lang_fi = ['afrikaani', 'albania', 'arabia', 'azerbaidzan', 'baski', 'bengali', 'valko-venäjä', 'bulgaria', 'katalonia', 'yksinkertaistettu kiina', 'perinteinen kiina', 'kroatia', 'tsekki, tshekki', 'tanska', 'hollanti', 'englanti', 'esperanto', 'viro', 'filippiini', 'suomi', 'ranska', 'galicia', 'georgia', 'saksa', 'kreikka', 'gujarati', 'haitin kreoli', 'heprea', 'hindi', 'unkari', 'islanti', 'indonesia', 'irlanti', 'italia', 'japani', 'kannada', 'korea', 'latina', 'latvia', 'liettua', 'makedonia', 'malaiji', 'malta', 'norja', 'persia', 'puola', 'portugali', 'romania', 'venäjä', 'serbia', 'slovakia', 'slovenia', 'espanja', 'swahili', 'ruotsi', 'tamil', 'telugu', 'thaimaa', 'turkki', 'ukraina', 'urdu', 'vietnam', 'wales', 'jiddis']

def find(lst, predicate):
    return next((i for i,j in enumerate(lst) if predicate(j)), -1)

def find_lang(predicate):
    pattern = predicate.lower()
    index = find(lang_en,lambda lang: pattern in lang)
    if index<0:
        index = find(lang_fi,lambda lang: pattern in lang)
    if index<0:
        index = find(language,lambda lang: pattern in lang)
    return index

def translate(text, il='auto', ol='en'):

	opener = urllib2.build_opener()
	opener.addheaders = [(
		'User-Agent', 'Mozilla/5.0' +
		'(X11; U; Linux i686)' +
		'Gecko/20071127 Firefox/2.0.0.11'
	)]

	il, ol = urllib2.quote(il), urllib2.quote(ol)
	try:
		if text is not text.encode('utf-8'):
			text = text.encode('utf-8')
	except:
		pass
	text = urllib2.quote(text)
	result = opener.open('http://translate.google.com/translate_a/t?' +
		('client=t&sl=%s&tl=%s' % (il, ol)) +
		('&q=%s' % text)).read()
	
	while ',,' in result:
		result = result.replace(',,', ',null,')
	
	data = json.loads(result)
	
	try:
		language = data[2]
	except:
		language = '?'
	
	return ''.join(x[0] for x in data[0]), language

@example('.gt en fi Sentence to be translated')
@commands('gtranslate', 'gt')
def gtranslate(bot, trigger):
	"""Translates a phrase to preferred language, see .lang list for available prefixes"""
	command = trigger.group(2).encode('utf-8')
	args = ['auto', 'en']
	for i in range(2):
	    if not ' ' in command:
	        break
	    prefix, cmd = command.split(' ', 1)
	    if prefix in language:
	        if i==0:
	            args[1] = prefix
	        else:
	            args[0] = args[1]
	            args[1] = prefix
	        command = cmd
	phrase = command
	il, ol = args
	if il!=ol:
		try:
			translated, il = translate(phrase, il, ol)
			il_en = lang_en[language.index(il)]
			ol_en = lang_en[language.index(ol)]
			bot.reply('"%s" (%s to %s)' % (translated, il_en, ol_en))
		except:
			bot.reply('You fail hard, go away.')
	else:
		bot.reply('Unable to translate between same language (%s to %s), try again, retard.' % (il_en, ol_en))

@example('.lang Bengali')
@commands('lang', 'l')
def listlang(bot, trigger):
	"""Lists prefix on defined language, use list to print all"""
	pattern = trigger.group(2)
	if pattern is None:
		bot.reply('Please enter string to search..')
		return
	if pattern == 'list':
		msg = 'Languages: '
		for index, lang in enumerate(lang_en):
			msg = msg + '%s - %s, ' % (lang, language[index])
		bot.reply(msg[:-2])
		return
	index = find_lang(pattern.encode('utf-8'))
	if index<0:
		bot.reply('No match found, try .lang list')
		return
	bot.reply('Found: %s, %s, prefix: %s' % (lang_en[index],lang_fi[index],language[index]))

