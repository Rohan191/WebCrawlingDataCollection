#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 15:04:27 2017

@author: rohantondulkar
"""

class SEED_NAMES(object):
    SKYSPORTS = 'skysports'
    
class SUB_SEEDS(object):
    SKY_FOOTBALL = 'skyfootball'
    SKY_CRICKET= 'skycricket'
    SKY_TENNIS= 'skytennis'
    SKY_RUGBY= 'skyrugby'
    SKY_GOLF= 'skygolf'
    SKY_BOXING= 'skyboxing'
    SKY_RACING= 'skyracing'

SEED_URLS = { SEED_NAMES.SKYSPORTS  : 'www.skysports.com'
             }
             
SUB_SEED_URLS = {
              SUB_SEEDS.SKY_CRICKET : 'http://www.skysports.com/cricket',
              SUB_SEEDS.SKY_TENNIS : 'http://www.skysports.com/tennis',
              SUB_SEEDS.SKY_FOOTBALL : 'http://www.skysports.com/football',
              SUB_SEEDS.SKY_RUGBY : 'http://www.skysports.com/rugby-union/',
              SUB_SEEDS.SKY_GOLF: 'http://www.skysports.com/golf/',
              SUB_SEEDS.SKY_BOXING: 'http://www.skysports.com/boxing/',
              SUB_SEEDS.SKY_RACING: 'http://www.skysports.com/racing/'
             }

MAX_DOCUMENTS = 500
NUM_WORDS_DOC = 400