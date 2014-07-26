# coding=utf8
"""
weather.py - Willie Yahoo! Weather Module
Copyright 2008, Sean B. Palmer, inamidst.com
Copyright 2012, Edward Powell, embolalia.net
Licensed under the Eiffel Forum License 2.

http://willie.dftba.net
"""
from __future__ import unicode_literals

from willie import web
from willie.module import commands, example

import feedparser
from lxml import etree


def setup(bot):
    # Having a db means pref's exists. Later, we can just use `if bot.db`.
    if bot.db and not bot.db.preferences.has_columns('woeid'):
        bot.db.preferences.add_columns(['woeid'])


def woeid_search(query):
    """
    Find the first Where On Earth ID for the given query. Result is the etree
    node for the result, so that location data can still be retrieved. Returns
    None if there is no result, or the woeid field is empty.
    """
    query = 'q=select * from geo.placefinder where text="%s"' % query
    body = web.get('http://query.yahooapis.com/v1/public/yql?' + query,
                   dont_decode=True)
    parsed = etree.fromstring(body)
    first_result = parsed.find('results/Result')
    if first_result is None or len(first_result) == 0:
        return None
    return first_result


def get_cover(parsed):
    try:
        condition = parsed.entries[0]['yweather_condition']
    except KeyError:
        return 'unknown'
    text = condition['text']
    # code = int(condition['code'])
    # TODO parse code to get those little icon thingies.
    return text


def get_temp(parsed):
    try:
        condition = parsed.entries[0]['yweather_condition']
        temp = int(condition['temp'])
    except (KeyError, ValueError):
        return 'unknown'
    f = round((temp * 1.8) + 32, 2)
    return (u'%d\u00B0C' % (temp))


def get_humidity(parsed):
    try:
        humidity = parsed['feed']['yweather_atmosphere']['humidity']
    except (KeyError, ValueError):
        return 'unknown'
    return ('%s%%' % (humidity))


def get_visibility(parsed):
    try:
        visibility = parsed['feed']['yweather_atmosphere']['visibility']
    except (KeyError, ValueError):
        return 'unknown'
    return ('%skm' % (visibility))


def get_pressure(parsed):
    try:
        pressure = parsed['feed']['yweather_atmosphere']['pressure']
        millibar = float(pressure)
        inches = int(millibar / 33.7685)
    except (KeyError, ValueError):
        return 'unknown'
    return ('%dhPa' % (int(millibar)))


def get_sunrise(parsed):
    try:
        sunrise = parsed['feed']['yweather_astronomy']['sunrise']
    except (KeyError, ValueError):
        return 'unknown'
    return sunrise


def get_sunset(parsed):
    try:
        sunset = parsed['feed']['yweather_astronomy']['sunset']
    except (KeyError, ValueError):
        return 'unknown'
    return sunset


def get_wind(parsed):
    try:
        wind_data = parsed['feed']['yweather_wind']
        kph = float(wind_data['speed'])
        m_s = float(round(kph / 3.6, 1))
        speed = int(round(kph / 1.852, 0))
        degrees = int(wind_data['direction'])
    except (KeyError, ValueError):
        return 'unknown'

    if speed < 1:
        description = 'Tyyntä'
    elif speed < 4:
        description = 'Pieni tuulenvire'
    elif speed < 7:
        description = 'Heikko tuuli'
    elif speed < 11:
        description = 'Kohtalainen tuuli'
    elif speed < 16:
        description = 'Kohtalainen tuuli'
    elif speed < 22:
        description = 'Kova tuuli'
    elif speed < 28:
        description = 'Kovempi tuuli'
    elif speed < 34:
        description = 'Melko navakka tuuli'
    elif speed < 41:
        description = 'Navakka tuuli'
    elif speed < 48:
        description = 'Melkein myrsky'
    elif speed < 56:
        description = 'Myrsky'
    elif speed < 64:
        description = 'Hurja myrsky'
    else:
        description = 'Hurrikaani'

    if (degrees <= 22.5) or (degrees > 337.5):
        degrees = u'\u2191'
    elif (degrees > 22.5) and (degrees <= 67.5):
        degrees = u'\u2197'
    elif (degrees > 67.5) and (degrees <= 112.5):
        degrees = u'\u2192'
    elif (degrees > 112.5) and (degrees <= 157.5):
        degrees = u'\u2198'
    elif (degrees > 157.5) and (degrees <= 202.5):
        degrees = u'\u2193'
    elif (degrees > 202.5) and (degrees <= 247.5):
        degrees = u'\u2199'
    elif (degrees > 247.5) and (degrees <= 292.5):
        degrees = u'\u2190'
    elif (degrees > 292.5) and (degrees <= 337.5):
        degrees = u'\u2196'

    return description + ' \x02' + str(m_s) + 'm/s\x02 (' + degrees + ')'


@commands('weather', 'wea')
@example('.weather London')
def weather(bot, trigger):
    """.weather location - Show the weather at the given location."""

    location = trigger.group(2)
    woeid = ''
    if not location:
        if bot.db and trigger.nick in bot.db.preferences:
            woeid = bot.db.preferences.get(trigger.nick, 'woeid')
        if not woeid:
            return bot.msg(trigger.sender, "I don't know where you live. " +
                           'Give me a location, like .weather London, or tell me where you live by saying .setlocation London, for example.')
    else:
        location = location.strip()
        if bot.db and location in bot.db.preferences:
            woeid = bot.db.preferences.get(location, 'woeid')
        else:
            first_result = woeid_search(location)
            if first_result is not None:
                woeid = first_result.find('woeid').text

    if not woeid:
        return bot.reply("I don't know where that is.")

    query = web.urlencode({'w': woeid, 'u': 'c'})
    url = 'http://weather.yahooapis.com/forecastrss?' + query
    parsed = feedparser.parse(url)
    location = parsed['feed']['title']

    cover = get_cover(parsed)
    temp = get_temp(parsed)
    pressure = get_pressure(parsed)
    wind = get_wind(parsed)
    sunrise = get_sunrise(parsed)
    sunset = get_sunset(parsed)
    humidity = get_humidity(parsed)
    visibility = get_visibility(parsed)

    bot.say(u'[WEATHER] %s - %s, \x02%s\x02, %s, \x02%s\x02, ilmankosteus: \x02%s\x02, näkyvyys: \x02%s\x02, aurinko nousee \x02%s\x02 ja laskee \x02%s\x02' % (location[17:], cover, temp, wind, pressure, humidity, visibility, sunrise, sunset))


@commands('setlocation', 'setwoeid')
@example('.setlocation Columbus, OH')
def update_woeid(bot, trigger):
    """Set your default weather location."""
    if bot.db:
        first_result = woeid_search(trigger.group(2))
        if first_result is None:
            return bot.reply("I don't know where that is.")

        woeid = first_result.find('woeid').text

        bot.db.preferences.update(trigger.nick, {'woeid': woeid})

        neighborhood = first_result.find('neighborhood').text or ''
        if neighborhood:
            neighborhood += ','
        city = first_result.find('city').text or ''
        state = first_result.find('state').text or ''
        country = first_result.find('country').text or ''
        uzip = first_result.find('uzip').text or ''
        bot.reply('I now have you at WOEID %s (%s %s, %s, %s %s.)' %
                  (woeid, neighborhood, city, state, country, uzip))
    else:
        bot.reply("I can't remember that; I don't have a database.")
