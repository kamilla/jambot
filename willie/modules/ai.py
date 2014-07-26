# -*- coding: utf-8 -*-
"""
ai.py - Artificial Intelligence Module
Copyright 2009-2011, Michael Yanovich, yanovich.net
Licensed under the Eiffel Forum License 2.

http://willie.dftba.net
"""
from willie.module import rule, priority, rate
import random
import time


def configure(config):
    """
    | [ai] | example | purpose |
    | ---------- | ------- | ------- |
    | frequency | 3 | How often Willie participates in the conversation (0-10) |
    """
    if config.option('Configure ai module', False):
            if not config.has_section('ai'):
                    config.add_section('ai')
            config.interactive_add('ai', 'frequency', 
                                   "How often do you want Willie to participate in the conversation? (0-10)",
                                   3)
            config.save()     
        
        
def setup(bot):
    # Set value to 3 if not configured
    if bot.config.ai and bot.config.ai.frequency:
        bot.memory['frequency'] = bot.config.ai.frequency
    else:
        bot.memory['frequency'] = 3
        
    random.seed()
        
        
def decide(bot):
    return 0 < random.random() < float(bot.memory['frequency']) / 10


@rule('(?i)$nickname\:\s+(bye|goodbye|seeya|cya|ttyl|g2g|gnight|goodnight|cu|moikka|katotaan|heihei|heippa)')
@rate(30)
def goodbye(bot, trigger):
    byemsg = random.choice(('Moimoi', 'Hyvästi', 'Tsiigataa', 'Katellaa', 'Kiva ku kävit, kivempi ku lähit', 'heihei'))
    punctuation = random.choice(('!', ' '))
    bot.reply('%s%s' % (byemsg, punctuation))


@rule('(?i).*(thank).*(you).*(willie|$nickname).*$')
@rate(30)
@priority('high')
def ty(bot, trigger):
    human = random.uniform(0, 9)
    time.sleep(human)
    mystr = trigger.group()
    mystr = str(mystr)
    if (mystr.find(" no ") == -1) and (mystr.find("no ") == -1) and (mystr.find(" no") == -1):
        bot.reply("You're welcome.")


@rule('(?i)$nickname\:\s+(thank).*(you).*')
@rate(30)
def ty2(bot, trigger):
    ty(bot, trigger)


@rule('(?i).*(thanks).*(willie|$nickname).*')
@rate(40)
def ty4(bot, trigger):
    ty(bot, trigger)


@rule('(willie|$nickname)\:\s+(yes|no)$')
@rate(15)
def yesno(bot, trigger):
    rand = random.uniform(0, 5)
    text = trigger.group()
    text = text.split(":")
    text = text[1].split()
    time.sleep(rand)
    if text[0] == 'yes':
        bot.reply("no")
    elif text[0] == 'no':
        bot.reply("yes")


@rule('(?i)($nickname|willie)\:\s+(ping)\s*')
@rate(30)
def ping_reply(bot, trigger):
    text = trigger.group().split(":")
    text = text[1].split()
    if text[0] == 'PING' or text[0] == 'ping':
        bot.reply("PONG")


@rule('(?i)i.*love.*(willie|$nickname).*')
@rate(30)
def love(bot, trigger):
    bot.reply("I love you too.")


@rule('(?i)(willie|$nickname)\:\si.*love.*')
@rate(30)
def love2(bot, trigger):
    bot.reply("I love you too.")


@rule('(?i)(willie|$nickname)\,\si.*love.*')
@rate(30)
def love3(bot, trigger):
    bot.reply("I love you too.")


@rule('(haha!?|lol!?|trololol!?|lollo!?|hahaha!?|hah!?|lyl!?|lols!?|lal!?|loool!?|xD!?)$')
@priority('high')
def f_lol(bot, trigger):
    if decide(bot):
        respond = ['haha', 'lol', 'rofl', 'loool', 'lololo', 'lal']
        randtime = random.uniform(0, 9)
        time.sleep(randtime)
        bot.say(random.choice(respond))


@rule('(cu!?|moikka!?|katotaan!?|heihei!?|heippa!?|moimoi!?)$')
@priority('high')
def f_bye(bot, trigger):
    respond = random.choice(('Moimoi', 'Hyvästi', 'Tsiigataa', 'Katellaa', 'Kiva ku kävit, kivempi ku lähit', 'heihei'))
    bot.say('%s' % (respond))


@rule('(?i)$nickname\:\s+(oikeesti!?)')
@priority('high')
def f_really(bot, trigger):
    randtime = random.uniform(10, 45)
    time.sleep(randtime)
    bot.say(str(trigger.nick) + ": " + "Nii, ihan oikeesti.")


@rule('^(wb|welcome\sback).*$nickname\s')
def wb(bot, trigger):
    bot.reply("Kiitti!")


if __name__ == '__main__':
    print __doc__.strip()
