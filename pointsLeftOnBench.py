#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 12:42:54 2022

@author: mattfariselli
"""

from config import keys
import requests
import pandas as pd
import seaborn as sb


swid = keys['fantasyFootballSWID']
espn_s2 = keys['fantasyFootballESPN_S2']
seasonId = '2022'
leagueId = keys['leagueID']


url = 'https://fantasy.espn.com/apis/v3/games/ffl/seasons/2022/segments/0/leagues/' + leagueId 

#this request is for the points from average chart
r = requests.get(url,
                 cookies={"swid": swid,
                          "espn_s2": espn_s2},
                 params={"view": "mMatchup"})
#Other params: mMatchup, mTeam, mBoxscore, mRoster, mSettings, kona_player_info, player_wl, mSchedule

d = r.json()

#This request is for the points left on the bench plot
r2 = requests.get(url,
                 cookies={"swid": swid,
                          "espn_s2": espn_s2},
                 params={"view": "mRoster"})

d2 = r2.json()

class player:
    def __init__(self, name, teamid):
        self.name = name
        self.teamid = teamid
        self.result = 'null'
        self.points = 0
        self.pointsFromAverage = 0
        self.oppoPoints = 0
        self.oppoPointsFromAverage = 0
        self.teamDict = {}
        self.playerData = []


matchResults= d2['teams']

#initializing each of the player classes
mattf = player('mattf', 7)
mattw = player('mattw', 10)
jesse = player('jesse', 5)
nessel = player('nessel', 1)
dave = player('dave', 9)
chris = player('chris', 8)
andrew = player('andrew', 2)
calvin = player('calvin', 3)
luke = player('luke', 4)
mahoney = player('mahoney', 6)
kate = player('kate',11)
tim = player('tim', 12)


#Creating a list of teams to loop through
teams = [mattf, mattw, jesse, nessel, dave, chris, andrew, calvin, luke, mahoney, kate, tim]

for team in teams:
    #assigning team data to each class
    team.teamDict = matchResults[team.teamid-1]['roster']['entries']

    #sorting through team data to pull valuable player information
    for player in team.teamDict:
        tempDict = {}
        tempDict['name'] = player['playerPoolEntry']['player']['fullName']
        tempDict['pointsScored'] = player['playerPoolEntry']['appliedStatTotal']
        tempDict['position'] = player['playerPoolEntry']['player']['defaultPositionId']
        
        team.playerData.append(tempDict)
    
    
