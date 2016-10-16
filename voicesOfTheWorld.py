#!/usr/bin/python

from oauth2client.service_account import ServiceAccountCredentials
import os
import time
from random import randint
from markovbot import MarkovBot
import tweepy, sys
from googleapiclient.discovery import build
import json
from httplib2 import Http

# Consumer Key (API Key)
cons_key = 'steU21Je70gUbRVAH3iwE7lIs'
# Consumer Secret (API Secret)
cons_secret = 'ljPyRVyjAKNS7uukSNMq4TNWS24G09f3vvycYLgSmoCMNOoyAP'
# Access Token
access_token = '772744937334906880-LYLYgrnDBSvsGZeUgwjoaVJY0t6oOWf'
# Access Token Secret
access_token_secret = 'lvbkNyhz1cNPyxHm9ghGtQ711gO1IeP2nNtzHuQkE6rdE'
# TABLE ID
TABLE_ID = '14_F_BC1Tfw_8qrvX0JSwDlhL14vuUx2j9Xr4hXhW'
#Developer key
developer_key = 'AIzaSyAAd_anUP5HBWRdRpWloPAklu8gYI9FlrE'


# tweepy for periodic tweets
auth = tweepy.OAuthHandler(cons_key, cons_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

scope = ['https://www.googleapis.com/auth/fusiontables.readonly']
credentials = ServiceAccountCredentials.from_json_keyfile_name('VoicesOfTheWorldBot-2c87b0274a78.json', scope)
http_auth = credentials.authorize(Http())

#fusion table API builder
service = build('fusiontables', 'v2', http=http_auth, developerKey=developer_key, credentials=credentials)

#gc = gspread.authorize(credentials)
#wks = gc.open("voices-of-the-world").sheet1

def GetTweetStr(service):
    row = randint(2,146688)
    query = "select * from "+TABLE_ID+" where rowid="+ str(row)
    rowResponse = service.query().sqlGet(sql=query).execute()
    country = rowResponse['rows'][0][0]
    #country = wks.cell(row,1).value
    genderkey = {'1':'male','2':'female'}
    gender = genderkey[rowResponse['rows'][0][6]]
    #gender = genderkey[wks.cell(row,7).value]
    age = rowResponse['rows'][0][7]

    tweetStr_1 = "I am from the " + country + ". I am a " + age + "yr. old " + gender + "."

    educationKey = {"1":"I have been educated only upto the primary level.","2":"I have completed secondary education.","3":"I went to college!"}
    incomeQuintile = {"1":"I belong to the poorest 20% of the world.","5":"I belong to the richest 20% of the world."}
    mobileBankAccountKey = {"1":"I use mobile banking."}
    debitcardUsedLast12Months = {"2":"I have not used my debit card in the last 12 months."}
    creditcardUsedLast12Months = {"2":"I have not used my credit card in the last 12 months."}
    noAccountBecasueFarAway = {"1":"I don't have a bank account because it is too far away."}
    noAccountBecauseExpensive = {"1":"I don't have a bank account because it is too expensive"}
    noAccountBecauseDocumentation = {"1":"I don't have a bank account becuase I lack documentation."}
    noAccountBecauseTrust = {"1":"I don't have a bank account becuase I don't trust the institutions."}
    noAccountBecauseReligious = {"1":"I don't have a bank account because of religious reasons."}
    noDepositIn12Months = {"2":"I have not deposited any money into my account in the past 12 months."}
    withdrawalFromAccountIn12Months = {"2":"I have not withdrawn any money from my account in the past 12 months."}
    noMobileTransaction = {"2":"I have never made a mobile transaction."}
    noOnlineTransaction = {"2":"I have never made an online transaction."}
    savingForBusiness = {"1":"I have been saving for the past year for my business."}
    savingInformally = {"1":"I have been saving for the past year in a informal savings club."}
    loan = {"1":"I have an outstanding loan."}
    privateLenderLoan = {"1":"I have borrowed from a private lender in the past year."}
    medicalLoan = {"1":"I have taken a medical loan in the past year."}
    emergencyFundSource = {"1":"My savings are my primary source of emergency funds.","2":"My family & friends are my primary source of emergency funds.","3":"Credit is my primary source of emergency funds.","4":"Credit is my primary source of emergency funds."}
    
    sentenceKey = [educationKey,incomeQuintile, mobileBankAccountKey, debitcardUsedLast12Months, creditcardUsedLast12Months, noAccountBecasueFarAway, noAccountBecauseExpensive,noAccountBecauseDocumentation,noAccountBecauseTrust, noAccountBecauseReligious, noDepositIn12Months,withdrawalFromAccountIn12Months,noMobileTransaction,noOnlineTransaction,savingForBusiness,savingInformally,loan,privateLenderLoan,medicalLoan,emergencyFundSource]

    column = randint(8,27)
    dictNo = column - 8
    tweetStr_2 = ""
    while(tweetStr_2 == ""):
        if sentenceKey[dictNo].has_key(rowResponse['rows'][0][column]):
            tweetStr_2 = sentenceKey[dictNo][rowResponse['rows'][0][column]]
        else:
            column = randint(8,27)

    tweetStr = tweetStr_1 + tweetStr_2
    return tweetStr

while True:
    tweetStr = GetTweetStr(service)
    api.update_status(tweetStr)
    time.sleep(3600)

# Markovbot for automated replies
tweetbot = MarkovBot()

dirname = os.path.dirname(os.path.abspath(__file__))
book = os.path.join(dirname, u'ebook.txt')
tweetbot.read(book)

my_first_text = tweetbot.generate_text(25, seedword=[u'economy', u'money'])
print(u'\ntweetbot says: "%s"' % (my_first_text))

# Log in to Twitter
tweetbot.twitter_login(cons_key, cons_secret, access_token, access_token_secret)

#Start tweeting periodically
tweetbot.twitter_tweeting_start(days=0, hours=0, minutes=1, keywords=None, prefix=None, suffix=None)

