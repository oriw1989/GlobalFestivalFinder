#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 16:21:48 2018

@author: orimichaelweiner
"""

import datefinder
import nltk

def simpleDateSearch(tweet, monthName="September"):

    tokens = nltk.word_tokenize(tweet)


    #find index that matches month word
    monthIndex = -1
    for index, word in enumerate(tokens):
        if (word == monthName):
            monthIndex=index
            break

    if monthIndex==-1:
        return -1, -1



    #find indices up to two words away from month
    if (monthIndex>2):
        lowerIndex = monthIndex-2
    else:
        lowerIndex = 0

    if monthIndex < len(tokens)-3:
        upperIndex = monthIndex+3
    else:
        upperIndex = len(tokens)-1

    dateTokens = tokens[lowerIndex:upperIndex]


    #now take the resulting ~5 words
    text = ""
    for token in dateTokens:
        text = text+" "+token


    dates = list(datefinder.find_dates(text))


    if len(dates)==0:
        return -1, -1


    return dates[0].month, dates[0].day





#print words around festival
def capitalizationFestivalSearch(tweet, festivalLabel="Festival"):

    tokens = nltk.word_tokenize(tweet)


    #find index that matches festival word
    fIndex = -1
    for index, word in enumerate(tokens):
        if (word == festivalLabel):
            fIndex=index
            break

    if fIndex==-1:
        return None


    festival = ""
    while fIndex > -1:
        if tokens[fIndex][0].isupper() or tokens[fIndex]=="&" or tokens[fIndex]=="and":
            festival = tokens[fIndex] + " " + festival
        else:
            break

        fIndex -= 1



    return festival[:-1]



from twitter import *
from collections import Counter
import time

def getEventNamesAndRedundencies(cityName, monthName="September", festivalLabel="Festival"):

    while True:
        try:
            t = Twitter(
                    auth=OAuth("1040306526093602816-yvOiRqZKolnuU2LApc5K9QiKoMmG2N", "OGuhyIhi3MamW4Ey14dJACqsp2p9ma4loeBErvQudapDT",
                               "vJJyEDyXo2nf6gEvU1ZjzDpEm", "fJ74NX5DPWiPnVf7Y8eqic1B8tCTN2tEzJfaaaCUBzWvxQ16YX"))

            allTweets = t.search.tweets(q=cityName + " " + festivalLabel + " " + monthName +
                                        " -filter:retweets", count=100, tweet_mode="extended")
            break

        except Exception as err:
        #except HTTPError:
            print("Reached twitter limit, waiting 15 minutes")
            time.sleep(15*60)

        #except:
        #    print("Error!")
        #    return None

    allText = []

    for tweet in allTweets['statuses']:
        allText.append(tweet['full_text'])

    #search for date and name of event
    nameAndDate = []
    for tweet in allText:
        nameAndDate.append((findEventNameInText(tweet, keyWord=festivalLabel),
                            simpleDateSearch(tweet, monthName)[1]))

    #filter useless tweets
    nameAndDate = list(filter(lambda xy: xy[1]>0 and xy[0] is not None, nameAndDate))


    return Counter(nameAndDate).most_common()


import pandas as pd

def find100CityEvents(monthName = "September", festivalLabel = "Festival"):

    cities = pd.read_excel('worldcities.xlsx')
    cities100 = cities.query('population > 3000000')

    for cityName in cities100['city'].values:
        eventNames = []
        days = []
        events = getEventNamesAndRedundencies(cityName, monthName, festivalLabel)
        if len(events) == 0:
            continue
        if events[0][1] > 1:
            print(cityName + ", " + events[0][0][0] + ", " + monthName + " " + str(events[0][0][1]))
            eventNames.append(events[0][0][0])
            days.append(events[0][0][1])

    return eventNames, days



import requests
import nltk
import string
from nltk.corpus import stopwords
from collections import Counter

def grabBagOfWords_exactsearch(eventName, cityName):

    #preliminary crunching
    eventWords = eventName.split()
    cityWords = cityName.split()

    searchString = ""
    for word in eventWords: #+cityWords
        searchString += word + "%20"

    searchWords = eventWords + cityWords


    #request data from newsriver
    response = requests.get("https://api.newsriver.io/v2/search?query=text%3A%22" + searchString[:-3] + "%22%20AND%20language%3AEN&sortBy=_score&sortOrder=DESC&limit=100",
                            headers={"Authorization":"sBBqsGXiYgF0Db5OV5tAw1PuBAhDIfdXZd2TIaluQ0eJMGTesbcsgTrnyz8q_gSqn2pHZrSf1gT2PUujH1YaQA"})
    jsonFile = response.json()


    #collect data
    titles = []
    texts = []
    for index, article in enumerate(jsonFile):
        titles.append(article['title'])
        texts.append(article['text'])


    #find most common words
    cityWords = [word.lower() for word in cityWords]
    table = str.maketrans(dict.fromkeys(string.punctuation+'’'))
    stops = stopwords.words('english') + ["january", "february", "march", "april", "may", "june", "july", "august",
                                          "september", "october", "november", "december", "festival", "2018"] + cityWords

    allTokens = []
    for text in texts:
        tokens = nltk.word_tokenize(text.lower().translate(table))
        tokens = [w for w in tokens if not w in stops]
        allTokens += tokens

    count = Counter(allTokens)

    return count.most_common(), titles, texts



def find1MCityEvents(monthName = "September", festivalLabel = "Festival"):

    cities = pd.read_excel('Data/worldcities.xlsx')
    cities1M = cities.query('population > 1000000')

    cityNames = []
    eventNames = []
    days = []
    for cityName in cities1M['city'].values:
        events = getEventNamesAndRedundencies(cityName, monthName, festivalLabel)
        if len(events) == 0:
            continue
        if events[0][1] > 1:
            print(cityName + ", " + events[0][0][0] + ", " + monthName + " " + str(events[0][0][1]))
            eventNames.append(events[0][0][0])
            days.append(events[0][0][1])
            cityNames.append(cityName)

    return cityNames, eventNames, days



def find100KCityEvents(monthName = "September", festivalLabel = "Festival"):

    cities = pd.read_excel('Data/worldcities.xlsx')
    cities1M = cities.query('population > 100000')

    cityNames = []
    eventNames = []
    days = []
    for cityName in cities1M['city'].values:
        events = getEventNamesAndRedundencies(cityName, monthName, festivalLabel)
        if len(events) == 0:
            continue
        if events[0][1] > 1:
            print(cityName + ", " + events[0][0][0] + ", " + monthName + " " + str(events[0][0][1]))
            eventNames.append(events[0][0][0])
            days.append(events[0][0][1])
            cityNames.append(cityName)

    return cityNames, eventNames, days



import pandas as pd

def generateEventDB(eventName, cityName):
    words, titles, texts = grabBagOfWords_exactsearch(eventName, cityName)
    listOfDicts = []

    for text, title in zip(texts, titles):
        d = {"Event Name": eventName, "City": cityName, "Article Title": title, "Article Text": text}
        listOfDicts.append(d)

    return pd.DataFrame(listOfDicts)

#create DF with all events
def generateNewsDataFrame(eventNames, cityNames):
    listOfDFs = []
    for event, city in zip(eventNames, cityNames):
        listOfDFs.append(generateEventDB(event, city))

    return pd.concat(listOfDFs)


#Input DF with all events, output concatanation of all text for events with more than min_articles
def generateTextDataFrame(newsDataFrame, min_articles = 5):

    listOfEvents = newsDataFrame['Event Name'].unique()
    listOfDicts = []
    for event in listOfEvents:
        eventDF = newsDataFrame[newsDataFrame['Event Name'] == event]
        if (eventDF.shape[0] >= min_articles):
            eventText = ""
            eventCity = eventDF.loc[0]['City']
            for text in eventDF['Article Text']:
                eventText = eventText + text
                eventDict = {"Event Name": event, "City": eventCity, "Text": eventText}
            listOfDicts.append(eventDict)

    return pd.DataFrame(listOfDicts)



#calculates dot product of user searched event with existing event matrix
import pickle
import numpy as np


def calculateEuclideanDistanceForUserSearch(eventName, cityName):

    tf_vectorizer = pickle.load(open('Data/tf_vectorizer_final.pkl', 'rb'))
    lda = pickle.load(open('Data/lda_final.pkl', 'rb'))
    clusters = pickle.load(open('Data/clusters_final.pkl', 'rb'))

    _, _, texts = grabBagOfWords_exactsearch(eventName, cityName)

    if (len(texts) < 5):
        print("Your query isn't returning enough results")
        return None

    eventText = ""
    for text in texts:
        eventText = eventText + text


    eventTF = tf_vectorizer.transform([eventText])
    eventScore = lda.transform(eventTF)


    #now calculate euclidean distance with some nifty numpy code
    eventScores = [eventScore[0]]*clusters.shape[0]
    eventEuclideanDistance = np.linalg.norm(eventScores - clusters, axis=1)
    bestFitIndices = np.argsort(eventEuclideanDistance)

    return eventEuclideanDistance, bestFitIndices

def calculateCosineSimilarityForUserSearch(eventName, cityName):

    tf_vectorizer = pickle.load(open('Data/tf_vectorizer_final.pkl', 'rb'))
    lda = pickle.load(open('Data/lda_final.pkl', 'rb'))
    clusters = pickle.load(open('Data/clusters_final.pkl', 'rb'))

    _, _, texts = grabBagOfWords_exactsearch(eventName, cityName)

    if (len(texts) < 2):
        print("Your query isn't returning enough results")
        return None

    eventText = ""
    for text in texts:
        eventText = eventText + text


    eventTF = tf_vectorizer.transform([eventText])
    eventScore = lda.transform(eventTF)


    #first normalize the cluster vectors
    norms = np.linalg.norm(clusters, axis=1)
    for index, a in enumerate(clusters):
        clusters[index] = a/norms[index]

    eventDotProd = np.matmul(clusters, eventScore.transpose())

    bestFitIndices = np.argsort(eventDotProd.transpose())[0]

    return eventDotProd, np.flipud(bestFitIndices)


def getTop10Festivals(festivalName, cityName):
    events = pd.read_pickle("Data/eventScores_final.pkl")
    result = calculateCosineSimilarityForUserSearch(festivalName, cityName)

    if result is None:
        return None

    eventScore, bestFits = result
    return events.loc[bestFits[0:10]]


def getAllTopFestivals(festivalName, cityName):
    events = pd.read_pickle("Data/eventScores_final.pkl")
    result = calculateCosineSimilarityForUserSearch(festivalName, cityName)

    if result is None:
        return None

    eventScore, bestFits = result
    return events.loc[bestFits]


import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()
from collections import Counter

def findEventNameInText(text, keyWord = "Festival"):
    text = text[:min(len(text), 100000)]
    doc = nlp(text)

    events = []
    for ent in doc.ents:
        if ent.label_=='EVENT':
            if len(ent.text.split()) > 2:
                if ent.text.find(keyWord) > -1:
                    events.append(ent.text.replace("The ", "").replace("the ", ""))

    if(len(events) == 0):
        return None

    eventName = Counter(events).most_common()[0]
    return(eventName[0])
