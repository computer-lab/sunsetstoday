import json
from urllib.request import urlopen
import datetime
from dateutil import tz
import pytz
import random
import time
import tweepy

def creds():
    with open('creds.json') as data_file:
        data = json.load(data_file)
        consumer_key = data['creds'][0]['consumer_key']
        consumer_secret = data['creds'][0]['consumer_secret']
        access_token = data['creds'][0]['access_token']
        access_token_secret = data['creds'][0]['access_token_secret']
        #return consumer_key, consumer_secret
        return consumer_key, consumer_secret, access_token, access_token_secret


def twitter_api(consumer_key, consumer_secret, access_token, access_token_secret):
    consumer_key = consumer_key
    consumer_secret = consumer_secret
    access_token = access_token
    access_token_secret = access_token_secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def bullshit():
    url = 'http://api.sunrise-sunset.org/json?lat=40.6970074&lng=-73.9284384&date=today&formatted=0'

    response = urlopen(url).read()
    data = json.loads(response.decode('utf-8'))
    sunset = data["results"]["sunset"]

    eastern = datetime.datetime.strptime(sunset[:-6], '%Y-%m-%dT%H:%M:%S').replace(tzinfo = pytz.UTC).astimezone(pytz.timezone('America/New_York'))
    eastern_sunset_time = datetime.datetime.strptime(sunset[:-6], '%Y-%m-%dT%H:%M:%S').replace(tzinfo = pytz.UTC).astimezone(pytz.timezone('America/New_York')).time()

    current_time = datetime.datetime.utcnow().replace(tzinfo = pytz.UTC)
    current_eastern = datetime.datetime.utcnow().replace(tzinfo = pytz.UTC).astimezone(pytz.timezone('America/New_York')).time()
    utc_sunset = datetime.datetime.strptime(sunset[:-6], '%Y-%m-%dT%H:%M:%S').replace(tzinfo = pytz.UTC)
    sun_has_set_delta = datetime.datetime.combine(datetime.date.today(), eastern_sunset_time) - datetime.datetime.combine(datetime.date.today(), current_eastern)
    sun_has_set_delta = str(sun_has_set_delta)
    print(current_eastern)
    print(eastern_sunset_time)
    if current_eastern > eastern_sunset_time:
        sun_has_set = True
        sun_has_set_delta, fuckoff = str(sun_has_set_delta).split('.')
        fuckoff, sun_has_set_delta = sun_has_set_delta.split(', ')
        d_hours, d_minutes, d_seconds = sun_has_set_delta.split(':')
        ss_hours =  24 - int(d_hours)
        ss_minutes =  60 - int(d_minutes)
        ss_hours = str(ss_hours)
        ss_minutes = str(ss_minutes)
    else:
        sun_has_set = False
        sun_has_set_delta = str(sun_has_set_delta)
        sun_has_set_delta, fuckoff = str(sun_has_set_delta).split('.')
        ss_hours, ss_minutes, ss_seconds = sun_has_set_delta.split(':')

    delta = eastern - current_time
    delta, fuckoff = str(delta).split('.')
    hours, minutes, seconds = delta.split(':')
    eastern_time = str(eastern)[11:-6]
    eastern_time = datetime.datetime.strptime(eastern_time, "%H:%M:%S")
    actual_time = eastern_time.strftime("%-I:%M")

    if hours == '1':
        hours = hours+' hour'
    elif hours  == '0':
        hours = 'no'
    else:
        hours = hours+' hours'

    if minutes == '1':
        minutes = minutes+' minute'
    else:
        minutes = minutes+' minutes'

    if ss_hours == '1':
        ss_hours = ss_hours+' hour'
    elif ss_hours  == '0':
        ss_hours = 'no'
    else:
        ss_hours = ss_hours+' hours'

    if ss_minutes == '1':
        ss_minutes = ss_minutes+' minute'
    else:
        ss_minutes = ss_minutes+' minutes'

    print(sun_has_set)
    return actual_time, hours, minutes, sun_has_set, sun_has_set_delta, ss_minutes, ss_hours



consumer_key, consumer_secret, access_token, access_token_secret = creds()

while True:
    on_time = datetime.time(6,45)
    off_time = datetime.time(23,59)

    eastern_now = datetime.datetime.utcnow().replace(tzinfo = pytz.UTC).astimezone(pytz.timezone('America/New_York')).time()
    if eastern_now > on_time and eastern_now < off_time:
        actual_time, hours, minutes, sun_has_set, sun_has_set_delta, ss_minutes, ss_hours = bullshit()
        api = twitter_api(consumer_key, consumer_secret, access_token, access_token_secret)
        if sun_has_set is False:
            h = ['the sun sets '+hours+' and '+minutes+', at '+actual_time,
                    "at "+actual_time+", the sun sets ... that's like in "+hours,
                    "in "+hours+" and "+minutes+", the sun is gonna set",
                    "it is gonna be dark in about "+hours, 'oh my fucking god',
                    "at "+actual_time+", which is like in "+hours+", the sun is gonna set",
                    "the sun goes down at "+actual_time+" today, which is like in "+hours,
                    "it is going to start to get dark in "+hours,
                    "at "+actual_time+" it is going to get dark",
                    "in "+hours+" it is going to start to get dark outside",
                    "sun goes down at "+actual_time+" today",
                    "sun is going to go down at "+actual_time+", like in "+hours]

            m = ['the sun sets in '+minutes+', at '+actual_time,
                    "at "+actual_time+", the sun sets ... that's like in "+minutes,
                    "in "+minutes+", the sun is gonna set",
                    "it is gonna be dark in about "+minutes,
                    "at "+actual_time+", which is like in "+minutes+", the sun is gonna set",
                    "the sun goes down at "+actual_time+" today, which is like in "+minutes,
                    "it is going to start to get dark in "+minutes,
                    "in "+minutes+" it is going to start to get dark outside",
                    "sun is going to go down at "+actual_time+", like in "+minutes]

            if hours == 'no':
                t = (random.choice(m))
            else:
                t = (random.choice(h))
                print(t)
                try:
                    api.update_status(status=t)
                except tweepy.error.TweepError as e:
                    print('duplicate status')
                time.sleep(random.randint(6200,6900))
        else:
            h = ['the sun set at like '+ss_hours+' ago',
                    'the sun went down today '+ss_hours+' ago',
                    'it got dark outside about '+ss_hours+' ago',
                    'sun went down '+ss_hours+' ago', 'fuck', '...fuck']
            m = ['the sun set  '+ss_minutes+' ago',
                    'the sun went down today '+ss_minutes+' ago',
                    'it got dark outside about '+ss_minutes+' ago',
                    'sun went down '+ss_minutes+' ago', 'fuck...']
            if ss_hours == 'no':
                t = (random.choice(m))
            else:
                t = (random.choice(h))
                print(t)
                try:
                    api.update_status(status=t)
                except tweepy.error.TweepError as e:
                    print('duplicate status')
                time.sleep(random.randint(7200,7600))

    else:
        print('sleep')
        time.sleep(600)

