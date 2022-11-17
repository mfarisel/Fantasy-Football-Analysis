#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 16:57:54 2022

@author: mattfariselli
"""

import pandas as pd
import seaborn as sb


#creating data dictionary to feed to Seaborn
def pointsFromAverage(teams,week):
    matchResults = {'points':[],'oppoPoints':[],'result':[],'name':[]}
    for team in teams:
        matchResults['points'].append(team.pointsFromAverage)
        matchResults['oppoPoints'].append(team.oppoPointsFromAverage)
        matchResults['result'].append(team.result)
        matchResults['name'].append(team.name)
    
    print(matchResults)
    
    totalScoredPoints = 0
    for team in teams:
        totalScoredPoints += team.points

    averagePoints = totalScoredPoints/len(teams)
    
    for team in teams:
        team.pointsFromAverage = team.points - averagePoints
        team.oppoPointsFromAverage = team.oppoPoints - averagePoints
    
    #Calculating Axis Bounds
    maxValue = round(max(matchResults['points']),-1)+10
    minValue = (round(max(matchResults['points']),-1)+10)*-1
    
    x = pd.DataFrame(data=matchResults)
    
    
    colors = ['black','darkgrey','brown','red','darkorange','gold',
              'fuchsia','cyan','dodgerblue','darkgreen','darkorchid','springgreen']
    
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
    
    plot.ax.set_title(label=f'Week {week} Matchup'+'\n'+f'Points From Average ({round(averagePoints,2)})',
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
    
    plot.savefig('PFA.png',dpi=300)
