#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 19:13:03 2022

@author: mattfariselli

ref: https://stmorse.github.io/journal/espn-fantasy-v3.html
"""

from pointsFromAverage import pointsFromAverage
from config import keys
import requests
import pandas as pd
import seaborn as sb

currentWeek = 7

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

matchResults = d2['teams']

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


matchups = d['schedule']
games = [x for x in matchups if x['matchupPeriodId'] == currentWeek]

for game in games:
    winner = game['winner'].lower()
    
    for team in teams:
        
        if team.teamid == game['away']['teamId']:
            team.points = game['away']['totalPoints']
            team.oppoPoints = game['home']['totalPoints']
            if winner == 'away':
                team.result = 'won'
            else:
                team.result = 'lost'
            
        elif team.teamid == game['home']['teamId']:
            team.points = game['home']['totalPoints']
            team.oppoPoints = game['away']['totalPoints']
            if winner == 'home':
                team.result = 'won'
            else:
                team.result = 'lost'
    

totalScoredPoints = 0
for team in teams:
    totalScoredPoints += team.points

averagePoints = totalScoredPoints/len(teams)

for team in teams:
    team.pointsFromAverage = team.points - averagePoints
    team.oppoPointsFromAverage = team.oppoPoints - averagePoints
    

pointsFromAverage(teams,currentWeek)




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































'''
#creating data dictionary to feed to Seaborn
def pointsFromAverage():
    matchResults = {'points':[],'oppoPoints':[],'result':[],'name':[]}
    for team in teams:
        matchResults['points'].append(team.pointsFromAverage)
        matchResults['oppoPoints'].append(team.oppoPointsFromAverage)
        matchResults['result'].append(team.result)
        matchResults['name'].append(team.name)
    
    #Calculating Axis Bounds
    maxValue = round(max(matchResults['points']),-1)+10
    minValue = (round(max(matchResults['points']),-1)+10)*-1
    
    x = pd.DataFrame(data=matchResults)
    
    
    colors = ['black','darkgrey','brown','red','darkorange','gold',
              'darkgreen','cyan','dodgerblue','blueviolet','darkorchid','fuchsia']
    
    plot = sb.relplot(data=x, 
                      x ='points',
                      y='oppoPoints',
                      hue='name', 
                      style = 'result', 
                      s =150,
                      palette=colors,
                      height=6,
                      aspect=1)
    
    plot.ax.axline(xy1=(0, 0), 
                   slope=1, 
                   color="b", 
                   dashes=(5, 2))
    
    
    
    plot.ax.spines['bottom'].set_position('zero')
    plot.ax.spines['left'].set_position('zero')
    
    plot.ax.set(xlim=(minValue, maxValue),
           ylim=(minValue, maxValue))
    
    
    plot.ax.grid(False)
    
    plot.ax.set_title(label=f'Week {wk} Matchup'+'\n'+f'Points From Average ({round(averagePoints,2)})',
                      pad=20,
                      fontsize = 20)
    
    
    plot.ax.set_xlabel(xlabel='points \nfor',
                      # loc='left',
                       wrap = True,
                       fontsize=12,
                       x= .0,
                       labelpad=-50,
                       ha='left')
    
    plot.ax.set_ylabel(ylabel='points \n against',
                       #loc='top', 
                       rotation='horizontal',
                       wrap=True,
                       fontsize=12,
                       y=.94,
                       labelpad=20)
    
    #Labeling chart areas
    plot.ax.text(x=maxValue/1.4,
                 y=maxValue/2.5,
                 s='Earned'+'\n'+'Win',
                 ha='center')
    
    plot.ax.text(x=-maxValue/2.9,
                 y=-maxValue/1.5,
                 s='Lucky'+'\n'+'Win',
                 ha='center')
    
    plot.ax.text(x=-maxValue/1.4,
                 y=-maxValue/2.5,
                 s='Deserved'+'\n'+'Loss',
                 ha='center')
    
    plot.ax.text(x=maxValue/2.9,
                 y=maxValue/1.5,
                 s='Unlucky'+'\n'+'Loss',
                 ha='center')
    
    plot.ax.fill([0,maxValue,maxValue],[0,maxValue,0],'palegreen',
                 zorder=0)
    
    plot.ax.fill([0,0,minValue],[0,minValue,minValue],'palegreen',
                 zorder=0)
    
    plot.ax.fill([0,0,maxValue],[0,maxValue,maxValue],'lightcoral',
                 zorder=0)
    
    plot.ax.fill([0,minValue,minValue],[0,0,minValue],'lightcoral',
                 zorder=0)
    
    #plot.savefig('PFA.png',dpi=300)
'''