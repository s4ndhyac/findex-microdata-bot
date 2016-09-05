import gspread
from oauth2client.service_account import ServiceAccountCredentials

import os
import time

from markovbot import MarkovBot

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('VoicesOfTheWorldBot-2c87b0274a78.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open("voices-of-the-world").sheet1

from random import randint
row = randint(2,25)

country = wks.cell(row,1).value
genderkey = {'1':'male','2':'female'}
gender = wks.cell(row,7).value
age = wks.cell(row,8).value

print "I am from the " + country + ". I am a " + age + "yr. old " + genderkey[gender] 

tweetbot = MarkovBot()

dirname = os.path.dirname(os.path.abspath(__file__))
book = os.path.join(dirname, u'ebook.txt')
tweetbot.read(book)

my_first_text = tweetbot.generate_text(25, seedword=[u'economy', u'money'])
print(u'\ntweetbot says: "%s"' % (my_first_text))

# Consumer Key (API Key)
cons_key = 'steU21Je70gUbRVAH3iwE7lIs'
# Consumer Secret (API Secret)
cons_secret = 'ljPyRVyjAKNS7uukSNMq4TNWS24G09f3vvycYLgSmoCMNOoyAP'
# Access Token
access_token = '772744937334906880-LYLYgrnDBSvsGZeUgwjoaVJY0t6oOWf'
# Access Token Secret
access_token_secret = 'lvbkNyhz1cNPyxHm9ghGtQ711gO1IeP2nNtzHuQkE6rdE'

# Log in to Twitter
tweetbot.twitter_login(cons_key, cons_secret, access_token, access_token_secret)

#Start tweeting periodically
tweetbot.twitter_tweeting_start(days=0, hours=0, minutes=1, keywords=None, prefix=None, suffix=None)
