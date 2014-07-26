# -*- coding: utf-8 -*-
"""
triviagod.py - JamBot Quakenet's triviabot God Module
copyright © 2013 kamilla @ quakeket <admin@kamillaproductions.com>
Licensed under the Eiffel Forum License 2.0
"""
from willie.module import rule
from willie.module import commands, example
import codecs
import random

question_found = False
question = ''
channel = ''
answer_to_questions = True
answer = ''

@rule('(Question).*')
def triviatrigger(bot, trigger):
    if trigger.nick != 'triviabot':
        return
    global question_found
    global question
    global channel
    global answer
    question_found = False
    question = trigger.group().split(':', 1)[1].lstrip()
    channel = trigger.sender    
    file = codecs.open('trivia.db', 'rU', 'utf-8')
    line = 'trolol'
    while line != '':
        line = file.readline().rstrip('\n')
        if line == question:
            answer = file.readline().rstrip('\n')
            if answer_to_questions:
                bot.say(answer)
            else:
                bot.say(random.choice(('Tiedetään! Tiedetään!', 'Mä tiiän tän!!', 'Saanko vastata? Tiiän!', 'Tiedän!', 'Se oli toi.. toi.. TIIÄN!', 'Tiedän tän. Saanko spoilata vastauksen?')))
            file.close()
            question_found = True
            return
    file.close()

@rule('(?i).*(answer)\s(was).*')
def addanswer(bot, trigger):
    if trigger.nick != 'triviabot':
        return
    global question_found
    global question
    global channel
    if not question_found and trigger.sender == channel:
        answer = trigger.group().split('answer was', 1)[1].lstrip().split('. Your', 1)[0].rstrip().split(', auth with Q', 1)[0]
        if answer.startswith(':'):
            answer = answer.split(': ', 1)[1].lstrip()
        file = codecs.open('trivia.db', 'aU', 'utf-8')
        file.write(question + '\n')
        file.write(answer + '\n')
        file.close()

@rule('(Say).*(trivia).*(library).*(to).*(play).*(again).*')
def autostart(bot, trigger):
    if trigger.nick == 'triviabot' and trigger.sender == '#jambot_training':
        bot.say('blaa blaa line, to prevent JamBot from frustrating and shouting ...')
        bot.say('!trivia')

@commands('trivia')
@example('.trivia [command] (command = shutup, auto, answer, stats)')
def trivia(bot, trigger):
    """Control JamBot trivia module behaviour. commands: shutup - Don't answer the questions automatically, auto - Answer the questions automatically, answer - Answer the current question, stats - Shows how many questions JamBot knows"""
    global answer_to_questions
    if not trigger.group(2):
        bot.say("You need to specify what do you want me to do. try '.help trivia'")
        return
    if trigger.group(2).lower() == 'shutup':
        answer_to_questions = False
        bot.say("OK, I won't say anything ;_;")
    elif trigger.group(2).lower() == 'auto':
        answer_to_questions = True
        bot.say("OK, I will answer automaticly to all the trivia questions")
    elif trigger.group(2).lower() == 'answer':
        if question_found:
            bot.say(answer)
        else:
            bot.say("I don't know the answer, sorry.")
    elif trigger.group(2).lower() == 'stats':
        bot.say('I know answers to ' + triviaquestionsknown() + ' trivia questions.')
    else:
        bot.say("I don't understand what the fuck you are trying to say..")

def triviaquestionsknown():
    i = 0
    file = codecs.open('trivia.db', 'rU', 'utf-8')
    for line in file:
        i += 1
    file.close
    i /= 2
    return str(i)
