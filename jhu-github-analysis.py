#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 06 11:25:56 2020

@author: kchittur
"""

# a hack to examine and plot git hub hopkins data on sars cov2
# creates a bunch of different plots - when I can, I will add some
# documentation

# collect libraries you will need - for reading csv files, plotting etc

import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
matplotlib.rcParams['text.latex.preamble'] = [r'\boldmath']
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import sys
import numpy as np
from csv import reader
from csv import *
import csv
import math

# directory where files are located, from the basedir
# in my case this was $HOME/COVID-19/
# place this code there
# clone the git hub repository 
# git clone https://github.com/CSSEGISandData/COVID-19
# and it will create a clone of their repo 
# git pull will update your copy
# run this code 
# look for a bunch of png's

# name the files to use them later

timeseries = 'csse_covid_19_data/csse_covid_19_time_series/'
confirmedGlobal = timeseries+'time_series_covid19_confirmed_global.csv'
deathsGlobal = timeseries+'time_series_covid19_deaths_global.csv'
recoveredGlobal = timeseries+'time_series_covid19_recovered_global.csv'
confirmedUS = timeseries+'time_series_covid19_confirmed_US.csv'
deathsUS = timeseries+'time_series_covid19_deaths_US.csv'
recoveredUS = timeseries+'time_series_covid19_recovered_US.csv'

# get the date from the files - read the first line really

def getdates(filename):
    csvfile = open(filename,'r')
    mycsvreader = csv.reader(csvfile,delimiter=',')
    thedates = []
    therows = []
    for row in mycsvreader:
        therows.append(row)
    for i in range(4,len(therows[0])):
        thedates.append(therows[0][i])
    return thedates

# get dates - but this time for US state based data - slightly different 
# format

def getstatedates(filename):
    csvfile = open(filename,'r')
    mycsvreader = csv.reader(csvfile,delimiter=',')
    thedates = []
    therows = []
    for row in mycsvreader:
        therows.append(row)
    for i in range(12,len(therows[0])):
        thedates.append(therows[0][i])
    return thedates

# get data about a specific country - if there is more than one row,
# it will collect data from all such rows

def getcountrydata(filename,thecountry):
    csvfile = open(filename,'r')
    mycsvreader = csv.reader(csvfile,delimiter=',')
    therows = []
    thenumbers= []
    for row in mycsvreader:
        therows.append(row)
    rown = []
    nrows = 0
    for i in range(len(therows)):
        thiscountry = therows[i][1]
        if (thiscountry == thecountry):
            rown.append(i)
            nrows = nrows + 1
    nl = len(therows[0])
    thesum = []
    for i in range(4,nl):
        sum = 0

        for j in range(len(rown)):
            thisr = int(rown[j])
            sum = sum + int(therows[thisr][i])
        thesum.append(sum)          
    return thesum

# get data from each state - this works for the state based data 
# ignore the dummy variables I have used!

def getstatedata(filename,thecountry):
    csvfile = open(filename,'r')
    mycsvreader = csv.reader(csvfile,delimiter=',')
    therows = []
    thenumbers= []
    for row in mycsvreader:
        therows.append(row)
    rown = []
    nrows = 0
    for i in range(len(therows)):
        thiscountry = therows[i][6]
        if (thiscountry == thecountry):
            rown.append(i)
            nrows = nrows + 1
    nl = len(therows[0])
    thesum = []
    for i in range(12,nl):
        sum = 0

        for j in range(len(rown)):
            thisr = int(rown[j])
            sum = sum + int(therows[thisr][i])
        thesum.append(sum)          
    return thesum

# this is to create plots from multiple files and multiple countries
# you can specify the output file names
# ndays refers to the days back from the last date to use in the program
# if you want to look at last 20 daus ndays = 20 and so on

def createmultipleplots(mfilenames,mfiletitles,theratio,ndays,countrynames,outputfiles):
    import matplotlib.ticker as ticker
    import matplotlib.pyplot as plt
    for i in range(len(mfilenames)):
        print ("Working with ", mfilenames[i])
        filename = mfilenames[i]
        thistitle = mfiletitles[i]
        for j in range(len(countrynames)):
            print ("Working on ", countrynames[j])
            country = countrynames[j]
            ydata = getcountrydata(filename,country)
            xdata = getdates(filename)
            if (i == theratio[0] and j == theratio[2]):
                firstset = getcountrydata(filename,country)
            if (i == theratio[1] and j == theratio[2]):
                secondset = getcountrydata(filename,country)
            ax = plt.axes()
            ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
            ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
            plt.xticks(rotation=90,fontsize=10,fontweight='bold')
            plt.xlabel("Date")
            plt.ylabel("Number")
            plt.title(r"{https://github.com/CSSEGISandData/COVID-19} %s day window" %(ndays),fontsize=8)
            plt.tight_layout
            plt.grid()
            thislabel=country+thistitle
            plt.plot(xdata[-ndays+1:],ydata[-ndays+1:],label=thislabel)
            plt.legend(loc='best')
        plt.savefig(outputfiles[i])
        plt.clf()
    ratiodata = []
    for i in range(len(firstset)):
        if (firstset[i] == 0.0 or secondset[i] == 0.0):
            ratiodata.append(0.0)
        else:
            ratiodata.append(firstset[i]/secondset[i])
    ax = plt.axes()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    plt.xticks(rotation=90,fontsize=10,fontweight='bold')
    plt.xlabel("Date")
    plt.ylabel("Ratio")
    thistitle = str(countrynames[theratio[2]])+' Ratio of Deaths to Recovered '
    plt.title(str(countrynames[theratio[2]]))
    plt.title(thistitle)
    plt.tight_layout
    plt.grid()
    plt.plot(xdata[-ndays+1:], ratiodata[-ndays+1:],label='Ratio')
    plt.legend(loc='best')
    rationame = str(countrynames[theratio[2]])+'Deaths2Recovered.png'
    plt.savefig(rationame)
    print ("Created ", rationame)


ndays = 50

# analyze global data 
# you can select which data to ratio against
# 1, 2 means ratio deathsGlobal to recoveredGlobal and 1 means Italy
# 1, 2, 0 means same - but this time for US

mfilenames = [confirmedGlobal,deathsGlobal,recoveredGlobal]
mfiletitles = ['confirmedGlobal','deathsGlobal','recoveredGlobal']
theratio = [1,2,1]
countrynames = ['US','Italy']
outputfiles = ['confirmedGlobal.png','deathsGlobal.png','recoveredGlobal.png']

# run function to create global data plots

createmultipleplots(mfilenames,mfiletitles,theratio,ndays,countrynames,outputfiles)

# analyze US state data  

mSfilenames = [confirmedUS,deathsUS]
mSfiletitles = ['confirmedUS','deathsUS']
statenames = ['New York', 'Alabama','Utah','California']
stateoutputfiles = ['confirmedUS.png','deathsUS.png']

def createmultipleUSStateplots(mSfilenames,mSfiletitles,ndays,statenames,outputfiles):
    import matplotlib.ticker as ticker
    import matplotlib.pyplot as plt
    for i in range(len(mSfilenames)):
        print ("Working on", mSfilenames[i])
        filename = mSfilenames[i]
        thistitle = mSfiletitles[i]
        for j in range(len(statenames)):
            print ("Working on ", statenames[j])
            country = statenames[j]
            ydata = getstatedata(filename,country)
            xdata = getstatedates(filename)
            ax = plt.axes()
            ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
            ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
            plt.xticks(rotation=90,fontsize=10,fontweight='bold')
            plt.xlabel("Date")
            plt.ylabel("Number")
            plt.title(r"{https://github.com/CSSEGISandData/COVID-19} %s day window" %(ndays),fontsize=8)
            plt.tight_layout
            plt.grid()
            thislabel=country+thistitle
            plt.plot(xdata[-ndays+1:],ydata[-ndays+1:],label=thislabel)
            plt.legend(loc='best')
        plt.savefig(outputfiles[i])
        plt.clf()

# run function to create state data 

createmultipleUSStateplots(mSfilenames,mSfiletitles,ndays,statenames,stateoutputfiles)



