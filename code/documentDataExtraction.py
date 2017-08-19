#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 16:04:27 2017

@author: rohantondulkar
"""
import os

KEYWORDS = 'keywords'
CONTENT  = 'content'
TITLE    = 'title'

class Document(object):
        
    def __hash__(self):
        return hash(self.title)
    
    def __eq__( self, other ):
        return self.getTitle() == other.getTitle()
    
    def setTitle( self, title ):
        self.title = title
        
    def getTitle( self ):
        return self.title
        
    def setURL( self, url ):
        self.url = url
        
    def getURL( self ):
        return self.url
        
    def setDate( self, date ):
        self.date = date
        
    def getDate( self ):
        return self.date
    
    def setContent( self, content ):
        self.content = content
        
    def getContent( self ):
        return self.content
    
    def setKeywords( self, keywords ):
        self.keywords = keywords
        
    def getKeywords( self ):
        return self.keywords
    
    def setDocId( self, docId ):
        self.docId = docId
        
    def getDocId( self ):
        return self.docId
        
    def setHtml( self, html ):
        self.html = html
    
    def getHtml( self ):
        return self.html

def getTitleFromPage( bsoup ):
    '''Get the title of the page'''
    return bsoup.find( TITLE ).getText()

def getKeywordsFromPage( bsoup ):
    '''Get meta keywords from the page'''
    for meta in bsoup.select('head meta'):
        attrs = meta.attrs
        name  = attrs.get( 'name' )
        if name == KEYWORDS :
            return attrs.get( CONTENT )

def getContentFromPage( bsoup ):
    '''Get the actual article content from the page'''
    text = ''
    for par in bsoup.find_all('p'):
        text = text + par.getText()
    return text.strip()
    

def getDateFromPage( bsoup ):
    '''Get the article date from page'''
    dateTag = bsoup.find('p', class_ = 'article__header-date-time')
    if dateTag:
        date = dateTag.getText()
        return date[14:]
    
def writeDocsToFiles( DOCUMENTS ):
    '''Write the documents to a directory locally'''
    print('-----------------------------------------------------------------------------------------------')
    print('Writing document to files')
    createDirectory( 'TextFiles' )
    for doc in DOCUMENTS:
        print('Writing document with ID:{0} and title:{1}'.format(doc.getDocId(), doc.getTitle().encode('utf-8')))
        f = open( '{0}.txt'.format(doc.getDocId()), 'w')
        f.write('URL:{0}\n'.format(doc.getURL()))
        f.write('TITLE:{0}\n'.format(doc.getTitle().encode('utf-8')))
        f.write('META-KEYWORDS:{0}\n'.format(doc.getKeywords().encode('utf-8')))
        f.write('DATE:{0}\n'.format(doc.getDate()))
        f.write('DOC ID:{0}\n'.format(doc.getDocId()))
        #print(doc.getContent()[1008:1011])
        f.write('CONTENT:{0}'.format(doc.getContent().encode('utf-8')))
        f.close()
        
def createDirectory( directory ):
    '''Create a directory as per requirement'''
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir( directory )