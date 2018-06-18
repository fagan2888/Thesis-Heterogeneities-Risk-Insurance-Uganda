# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 11:15:04 2018

@author: Albert
"""


import pandas as pd
import numpy as np
import os


os.chdir('D:/Documents/Documents/IDEA/Research/Data/UGANDA/data11')
pd.options.display.float_format = '{:,.2f}'.format

dollars = 2586.89

#%%Income 

lab9 = pd.read_stata("GSEC8.dta")
lab9 = lab9[["HHID","PID", "h8q31a","h8q31b","h8q31c","h8q44","h8q44_1","h8q45a","h8q45b","h8q45c"]]     
lab9.columns = [["hh","pid","cash1","inkind1", "time1", "months2","weeks2", "cash2","inkind2", "time2"]]

#very few people report hours so fuck them
pd.value_counts(lab9.time1).reset_index()
pd.value_counts(lab9.time2).reset_index()

lab9["pay1"] = lab9.loc[:,["cash1","inkind1"]].sum(axis=1)
lab9["pay2"] = lab9.loc[:,["cash2","inkind2"]].sum(axis=1)
del lab9["cash1"], lab9["inkind1"], lab9["cash2"], lab9["inkind2"]


#Creating week wages
# From Besamuscka, Tijdens (2012),  https://wageindicator.org/main/Wageindicatorfoundation/publications/2012/wages-in-uganda-wage-indicator-survey-2012
# we take mean average hours and days worked per week: 60 and 6
lab9.loc[lab9.time1 == "Day", 'pay1'] = lab9.loc[lab9.time1 == "Day", 'pay1']*6
lab9.loc[lab9.time1 == "Month", 'pay1'] = lab9.loc[lab9.time1 == "Month", 'pay1']/4
lab9.loc[lab9.time1 == "Hour", 'pay1'] = lab9.loc[lab9.time1 == "Hour", 'pay1']*60

lab9.loc[lab9.time1 == "Day", 'pay2'] = lab9.loc[lab9.time1 == "Day", 'pay2']*6
lab9.loc[lab9.time1 == "Month", 'pay2'] = lab9.loc[lab9.time1 == "Month", 'pay2']/4
lab9.loc[lab9.time1 == "Hour", 'pay2'] = lab9.loc[lab9.time1 == "Hour", 'pay2']*60

#We don't have info about months and weeks worked. We use the sample mean of 2013-2014. Note that this can hidden important inequality on work time.
lab9["wage1"] = 9.75*3.72*lab9.pay1
lab9["wage2"] = lab9.months2*lab9.weeks2*lab9.pay2



lab99 = lab9.groupby(by="hh")[["wage1","wage2"]].sum()
lab99["wage_total"] = lab99.loc[:,["wage1","wage2"]].sum(axis=1)
lab99= lab99.replace(0, np.nan)


lab99["hh"] = np.array(lab99.index.values)
summaryw = lab99.describe()
print(summaryw.to_latex())

del lab9

#%% business

bus12 = pd.read_stata('GSEC12.dta')
bus12 = bus12[["HHID","h12q12", "h12q13","h12q15","h12q16","h12q17"]]
bus12.rename(columns={'HHID':'hh'}, inplace=True)
bus12.rename(columns={'h12q13':'revenue'}, inplace=True)
bus12["cost"] = -bus12.loc[:,["h12q15","h12q16","h12q17"]].sum(axis=1)
bus12["bs_profit"] = bus12.loc[:,["revenue","cost"]].sum(axis=1)
bus12["bs_profit"] = bus12["bs_profit"].replace(0,np.nan)
bus12 = bus12[["hh","bs_profit"]]
bus12 = bus12.groupby(by="hh").sum()

bus12["hh"] = np.array(bus12.index.values)

summarybus = bus12.describe()

print(summarybus.to_latex())

#%% Other income

other = pd.read_stata('GSEC11.dta')
other = other[["HHID","h11q5","h11q6"]]
other.rename(columns={'HHID':'hh'}, inplace=True)
other["other_inc"] = other.loc[:,["h11q5","h11q6"]].sum(axis=1)
other = other[["hh","other_inc"]]
other = other.groupby(by="hh").sum()
other = other
other["hh"] = np.array(other.index.values)
summaryo = other.describe()



# extra-expenditures ---------------------------------------
# NO QUESTIONARY IN EXTRA EXPENDITURES





#%% Merge datasets
income_gsec = pd.merge(lab99, bus12, on="hh", how="outer")
income_gsec = pd.merge(income_gsec, other, on="hh", how="outer")
del income_gsec["wage1"], income_gsec["wage2"], bus12,  dollars, other, lab99, summarybus, summaryo, summaryw

sumlab = income_gsec[["wage_total","bs_profit", "other_inc"]].describe()
print(sumlab.to_latex())

income_gsec.to_csv('income_hhsec_2011.csv')


