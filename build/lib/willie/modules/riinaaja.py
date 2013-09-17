# -*- coding: utf-8 -*-
from willie.module import commands

@commands('.*[Hh][Uu][Oo][Mm][Ee][Nn][Tt][Aa]\s*.*[Jj][Aa][Mm][Bb][Oo][Tt].*|.*[Jj][Aa][Mm][Bb][Oo][Tt]\s*.*[Hh][Uu][Oo][Mm][Ee][Nn][Tt][Aa].*')
def gmorning(bot, trigger):
	if trigger.nick=='Riinaaja' or trigger.nick=='kamilla':
		bot.say('Huomenta '+ trigger.nick +', sinä ihana otus <3')
