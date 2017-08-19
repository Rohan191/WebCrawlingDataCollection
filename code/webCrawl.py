#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 15:39:39 2017

@author: rohantondulkar
"""

import constants as config
import requests
from bs4 import BeautifulSoup
import documentDataExtraction as doc

DOCUMENTS = set()
VALID_URLS= set()

def startCrawlingSeeds():
    '''This is the method to run this crawler.
        This function crawls the seed urls'''
    for seed, url in config.SEED_URLS.items():
        print('Starting crawling for seed :{0}'.format(seed))
        url = 'http://{0}'.format(url)
        webCrawl( url, seed )
    doc.writeDocsToFiles( DOCUMENTS )
        
def webCrawl( url, seed ):
    '''To get the page of this url and call other important functions to create document and get other urls in this page'''
    page      = requests.get(url)
    getDocumentFromPage( page, seed )
    #Get the urls from seed home page
    getUrlListForPage( page.text, seed )
    
    #Continue to the loop for all urls added to VALID_URLS
    while True:
        if len(DOCUMENTS)> config.MAX_DOCUMENTS:
            break
        try:
            url  = VALID_URLS.pop()
            page = requests.get(url)
            #print('Number of Documents:{0}'.format(len(DOCUMENTS)))
            #print('Crawling url: {0}'.format(url))
            if getDocumentFromPage( page, seed ):
                #Only get the urls if a document can now be generated from this page
                getUrlListForPage( page.text, seed )
        except Exception as e:
            print('Exception raised being ignored: {0}'.format(e))
            break
    
def getUrlListForPage( page_text, seed ):
    '''For a given page, get the valid urls from that page'''
    bsoup = BeautifulSoup( page_text, 'html.parser' )
    for ahref in bsoup.find_all('a'):
        url = getUrlFromHref(ahref)
        if url and isValidUrl( url, seed ):
            VALID_URLS.add( url )

def getUrlFromHref( ahref ):
    '''get the url text from the anchor <a> tag'''
    url = ahref.get('href')
    return url.strip() if url else None
    

def isStartsWithDomain( url, seed ):
    '''To check if domain name is amongst the first 15 letters of url'''
    domain = config.SEED_URLS.get( seed )   
    index = url.find( domain )
    return index>=0 and index<=15

def isContainNews( url, seed ):
    '''To check if its a news article'''
    return 'news' in url

def isContainNewsOrLiveScores( url, seed):
    '''To check if url is of news or live scores'''
    return 'news' in url or 'live-scores' in url
    
#URL RUlE list per seed to be defined here
URL_RULE_LIST = { config.SEED_NAMES.SKYSPORTS : [ isStartsWithDomain,
                                                   isContainNews
                                                  ],
        }

def isValidUrl( url, seed ):
    '''Apply rule list on url to check if its valid'''
    if not isSubSeed( url, seed ):
        ruleList = URL_RULE_LIST.get( seed )
        for rule in ruleList:
            if not rule( url, seed ):
                return False
    return True

def isSubSeed( url, seed ):
    '''To check if the url is amongst the subseeds'''
    return url in config.SUB_SEED_URLS.values()

def getDocumentFromPage( page, seed ):
    '''Create document from the page if it satisfies the constraints'''
    bsoup = BeautifulSoup( page.text, 'html.parser' )
    document = doc.Document()
    document.setContent( doc.getContentFromPage(bsoup) )
    document.setTitle( doc.getTitleFromPage(bsoup))
    document.setKeywords( doc.getKeywordsFromPage(bsoup))
    document.setDate( doc.getDateFromPage(bsoup))
    document.setURL( page.url )
    document.setHtml( page.content )
    if document not in DOCUMENTS:   #Avoid duplicate documents based on title
        num_words = len(document.getContent().split())
        if num_words >=config.NUM_WORDS_DOC:
            document.setDocId( len(DOCUMENTS) + 1)
            DOCUMENTS.add( document )
            print('Number of words in this doc: {0}'.format(num_words))
            print('-----------------------------------------------------------------------------------------------')
            print('Adding document with docId: {0} and title:{1}'.format(document.getDocId(), document.getTitle()))
            print('-----------------------------------------------------------------------------------------------')
            return True
        else:
            print('Ignoring document due to lesser words in content:{0}'.format(num_words))
            if len(DOCUMENTS) == 0 or isSubSeed( page.url, seed ):
                return True
            else:
                return False
    else:
        print('Not adding duplicate document: {0}'.format(document.getTitle()))
        return False
    