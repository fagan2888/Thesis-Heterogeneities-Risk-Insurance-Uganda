# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 16:51:17 2018

@author: Albert
"""
 
#### Agriculture 2011-2012
import pandas as pd
import numpy as np
import os
os.chdir('D:/Documents/Documents/IDEA/Research/python Albert')
from data_functions_albert import remove_outliers


os.chdir('D:/Documents/Documents/IDEA/Research/Data/UGANDA/data11')
pd.options.display.float_format = '{:,.2f}'.format
dollars = 2586.89



#%% AGRICULTURAL SEASON 1:

#rent obtained------------------------------
ag2a = pd.read_stata('AGSEC2A.dta')
ag2a = ag2a[["HHID", "a2aq14"]]
ag2a = ag2a.groupby(by="HHID")[["a2aq14"]].sum()
ag2a.columns = ["rent_owner"]
ag2a["hh"] = np.array(ag2a.index.values)



# rent payment--------------------------
ag2b = pd.read_stata('AGSEC2B.dta')
ag2b = ag2b[["HHID", "a2bq9", "a2bq13"]]
values = ["a2bq9", "a2bq13"]
ag2b = ag2b.groupby(by="HHID")[["a2bq9", "a2bq13"]].sum()

ag2b["rent_noowner"] = ag2b["a2bq13"].fillna(0) - ag2b["a2bq9"].fillna(0)
ag2b["rent_noowner"] = ag2b["rent_noowner"].replace(0, np.nan)
ag2b = ag2b[["rent_noowner"]]
ag2b["hh"] = np.array(ag2b.index.values)
#rent obtained - payed for those who rend
#REVENUE




# Fertilizers & labor costs-------------------------------------
ag3a = pd.read_stata('AGSEC3A.dta')
ag3a = ag3a[["HHID", "a3aq8", "a3aq18", "a3aq27","a3aq36"]]

ag3a = ag3a.groupby(by="HHID")[["a3aq8", "a3aq18", "a3aq27","a3aq36"]].sum()

ag3a["fert_lab_c"] = ag3a["a3aq8"].fillna(0)+ ag3a["a3aq18"].fillna(0) + ag3a["a3aq27"].fillna(0) + ag3a["a3aq36"].fillna(0)
ag3a["fert_lab_c"] = ag3a["fert_lab_c"].replace(0, np.nan)
ag3a = ag3a[["fert_lab_c"]]
ag3a["hh"] = np.array(ag3a.index.values)
#COST




# Seeds costs------------------------------------------------------
ag4a = pd.read_stata('AGSEC4A.dta')
ag4a = ag4a[["HHID", "a4aq15"]]
ag4a = ag4a.groupby(by="HHID")[["a4aq15"]].sum()
ag4a.columns = ["seeds_c"]
ag4a["hh"] = np.array(ag4a.index.values)
#COST




# Output -------------------------------------------------------
ag5a = pd.read_stata('agsec5a.dta')
ag5a = ag5a[["HHID","cropID","a5aq6a","a5aq6c","a5aq6d","a5aq7a","a5aq7c","A5AQ7D","a5aq8","a5aq10","a5aq12","a5aq13","a5aq14a","a5aq114b","a5aq15","a5aq21"]]
ag5a.columns = ["HHID", "cropID", "total","unit", "tokg", "sell", "unit2","tokg2", "value_sells", "trans_cost", "gift", "cons", "food_prod", "animal", "seeds", "stored"]


# Convert all quantitites to kilos:

#1.1 get median conversations (self-reported values)
conversion_kg = ag5a.groupby(by="unit")[["tokg"]].median()
conversion_kg.reset_index(inplace=True)
conversion_kg.loc[conversion_kg.unit=="Kilogram (KG)", "tokg"] = 1
conversion_kg.columns = ["unit","kgconverter"]


ag5a = ag5a.merge(conversion_kg, on="unit", how="left")


# Convert to kg
ag5a[["total", "sell", "gift", "cons", "food_prod", "animal", "seeds", "stored"]] = ag5a[["total", "sell", "gift", "cons", "food_prod", "animal", "seeds", "stored"]].multiply(ag5a["kgconverter"], axis="index")


#1.2 Check reported quantities
ag5a["total"] = ag5a["total"].fillna(0)
ag5a["total2"] =  ag5a.loc[:,["sell","gift","cons","food_prod","animal", "seeds", "stored"]].sum(axis=1)
ag5a["diff_totals"] = ag5a.total -ag5a.total2


count_equal = len(ag5a.loc[ag5a.total==ag5a.total2])
count_bigger = len(ag5a.loc[ag5a.total>ag5a.total2])
count_smaller = len(ag5a.loc[ag5a.total<ag5a.total2])


#Prices
ag5a["prices"] = ag5a.value_sells.div(ag5a.sell, axis=0) 
prices = ag5a.groupby(by=["cropID"])[["prices"]].median()

#Check price values in Dollars: they make sense!!!!
prices_usd = ag5a.groupby(by=["cropID"])[["prices"]].median()/dollars


prices.reset_index(inplace=True)
prices.columns=["cropID","med_prices"]


## Use consumption prices
cprices= pd.read_csv("pricesfood11.csv")

pricesname = prices.cropID
cprices["cropID"] = "nothing"

cprices.loc[cprices["code"].isin([101,102,103,104]),"cropID"] = "Banana food"
cprices.loc[cprices["code"].isin([105,106]),"cropID"] = "Sweet potatoes"
cprices.loc[cprices["code"].isin([107,108]),"cropID"] = "Cassava"

cprices.loc[cprices["code"]==109,"cropID"] = "Sweet potatoes"
cprices.loc[cprices["code"]==110,"cropID"] = "Rice"
cprices.loc[cprices["code"].isin([111,112,113]),"cropID"] = "Maize"

cprices.loc[cprices["code"]==115, "cropID"] = "Finger millet"
cprices.loc[cprices["code"]==116,"cropID"] = "Sorghum"
cprices.loc[cprices["code"]==146,"cropID"] = "Simsim"
cprices.loc[cprices["code"]==137,"cropID"] = "Cabbages"
cprices.loc[cprices["code"]==138,"cropID"] = "Dodo"
cprices.loc[cprices["code"]==136,"cropID"] = "Tomatoes"
cprices.loc[cprices["code"]==135,"cropID"] = "Onions"
cprices.loc[cprices["code"]==165,"cropID"] = "Pumpkins"
cprices.loc[cprices["code"]==168,"cropID"] = "Eggplants"
cprices.loc[cprices["code"]==170,"cropID"] = "Pineapples"
cprices.loc[cprices["code"]==132,"cropID"] = "Mango"
cprices.loc[cprices["code"]==130,"cropID"] = "Passion fruit"
cprices.loc[cprices["code"]==166,"cropID"] = "Avacoda"
cprices.loc[cprices["code"]==148,"cropID"] = "Coffee"
cprices.loc[cprices["code"]==149,"cropID"] = "Tea"

cprices.loc[cprices["code"].isin([140,141]),"cropID"] = "Beans"
cprices.loc[cprices["code"].isin([142,143,144,184]),"cropID"] = "Groundnuts"

cprices.loc[cprices["code"].isin([145,162]),"cropID"] = "Peas"

cprices.drop(["code"], axis=1, inplace=True)

# Set of prices
prices = prices.merge(cprices, on="cropID", how="left")
prices[["m_p","gate_p"]] = prices[["m_p","gate_p"]].fillna(0)
prices.to_csv("cropprices11.csv")

#For the items that do not have consumption prices input the selling ones.
prices.loc[prices["m_p"]==0, ["m_p"]] = prices.loc[prices["m_p"]==0, "med_prices"]
prices.loc[prices["gate_p"]==0, ["gate_p"]] = prices.loc[prices["gate_p"]==0, "med_prices"]
prices.columns = ["cropID","p_sell", "p_c", "p_c_gate"]


ag5a = ag5a.merge(prices, on="cropID", how="left")

quant = ["total","total2","sell","gift","cons","food_prod","animal","seeds","stored"]
priceslist = ["p_sell"] 
#to check production value for the 3 type of prices uncomment:
# priceslist = ["p_sell", "p_m", "p_gate"] 
values_ag5a = ag5a[["HHID", "trans_cost"]]
#Generate values for each quantities and each type of price. Now I only use for sellings prices since the consumption ones where to big.
for q in quant:
    for p in priceslist:
        values_ag5a[q+"_value_"+p] = ag5a[q]*ag5a[p]


ag5a = values_ag5a.groupby(by="HHID").sum()
ag5a= ag5a.replace(0, np.nan)
ag5a["hh"] = np.array(ag5a.index.values)
sumag5a = ag5a.describe()/dollars


"""
# Use reported own produced consumption for crops
crops_c = pd.read_csv("crops_c11.csv")
ag5a = pd.merge(ag5a, crops_c, on="hh")
sumowncrops = ag5a[["cons_value","own_value"]].describe()/dollars
ag5a["cons_value2"] = ag5a["own_value"]/2
ag5a.drop(["own_value"], axis=1)
ag5a["total_value2"] =  ag5a.loc[:,["sells_value_2","gift_value","cons_value2","food_prod_value","animal_value", "seeds_value", "stored_value"]].sum(axis=1)
"""



# Merge datasets -------------------------------------------
agrica = pd.merge(ag2a, ag2b, on='hh', how='outer')
agrica = pd.merge(agrica, ag3a, on='hh', how='outer')
agrica = pd.merge(agrica, ag4a, on='hh', how='outer')
agrica = pd.merge(agrica, ag5a, on='hh', how='outer')



#### Trim the data at the 0.1% both sides
agrica.set_index("hh", inplace=True)

agrica = remove_outliers(agrica, lq=0, hq=0.999)

#Pass it to dollars to see if values make sense or not
summarya1 = agrica.describe()/dollars
agrica.reset_index(inplace=True)
  

del ag2a, ag2b, ag3a, ag4a, ag5a, prices
#agrica = pd.merge(agrica, basic, on='hh', how='outer')


agrica["cost_agra"] = -agrica.loc[:,["fet_lab_c","seeds_c","trans_cost"]].sum(axis=1)
agrica["profit_agra"] = agrica.loc[:,["total2_value_p_sell","rent_owner","rent_noowner","cost_agra"]].sum(axis=1)
agrica= agrica.replace(0, np.nan)
agA = agrica[["hh", "profit_agra"]]


suma = agA.describe()/dollars

#%% AGRICULTURAL SEASON 2:

# Fertilizers & labor costs--------------------------------------
ag3b = pd.read_stata('AGSEC3B.dta')
ag3b = ag3b[["HHID", "a3bq8", "a3bq18", "a3bq27","a3bq36"]]

ag3b = ag3b.groupby(by='HHID').sum()
ag3b["fert_lab_cb"] = ag3b.loc[:,["a3bq8","a3bq18","a3bq27","a3bq36"]].sum(axis=1)
ag3b = ag3b[["fert_lab_cb"]]
ag3b = ag3b.replace(0,np.nan)
ag3b["hh"] = np.array(ag3b.index.values)
#COST



# Seeds costs----------------------------------------------------
ag4b = pd.read_stata('AGSEC4B.dta')
ag4b = ag4b[["HHID", "a4bq15"]]
ag4b = ag4b.groupby(by='HHID').sum()
ag4b.columns= [["seeds_cb"]]
ag4b["hh"] = np.array(ag4b.index.values)
#COST


# Output-----------------------------------------------------
ag5b = pd.read_stata('agsec5b.dta')

ag5b = ag5b[["HHID","cropID","a5bq6a","a5bq6c","a5bq6d","a5bq7a","a5bq7c","A5BQ7D","a5bq8","a5bq10","a5bq12","a5bq13","a5bq14a","a5bq14b","a5bq15","a5bq21"]]
ag5b.columns = ["HHID", "cropID", "total","unit", "tokg", "sell", "unit2","tokg2", "value_sells", "trans_cost", "gift", "cons", "food_prod", "animal", "seeds", "stored"]


# Convert all quantitites to kilos:

#1.1 get median conversations (self-reported values)
conversion_kg = ag5b.groupby(by="unit")[["tokg"]].median()
conversion_kg.reset_index(inplace=True)
conversion_kg.loc[conversion_kg.unit=="Kilogram (KG)", "tokg"] = 1
conversion_kg.columns = ["unit","kgconverter"]


ag5b = ag5b.merge(conversion_kg, on="unit", how="left")


# Convert to kg
ag5b[["total", "sell", "gift", "cons", "food_prod", "animal", "seeds", "stored"]] = ag5b[["total", "sell", "gift", "cons", "food_prod", "animal", "seeds", "stored"]].multiply(ag5b["kgconverter"], axis="index")


#1.2 Check reported quantities
ag5b["total"] = ag5b["total"].fillna(0)
ag5b["total2"] =  ag5b.loc[:,["sell","gift","cons","food_prod","animal", "seeds", "stored"]].sum(axis=1)
ag5b["diff_totals"] = ag5b.total -ag5b.total2


count_equal = len(ag5b.loc[ag5b.total==ag5b.total2])
count_bigger = len(ag5b.loc[ag5b.total>ag5b.total2])
count_smaller = len(ag5b.loc[ag5b.total<ag5b.total2])


#Prices
ag5b["prices"] = ag5b.value_sells.div(ag5b.sell, axis=0) 
prices = ag5b.groupby(by=["cropID"])[["prices"]].median()

#Check price values in Dollars: they make sense!!!!
prices_usd = ag5b.groupby(by=["cropID"])[["prices"]].median()/dollars


prices.reset_index(inplace=True)
prices.columns=["cropID","med_prices"]


## Use consumption prices
cprices= pd.read_csv("pricesfood11.csv")

pricesname = prices.cropID
cprices["cropID"] = "nothing"

cprices.loc[cprices["code"].isin([101,102,103,104]),"cropID"] = "Banana food"
cprices.loc[cprices["code"].isin([105,106]),"cropID"] = "Sweet potatoes"
cprices.loc[cprices["code"].isin([107,108]),"cropID"] = "Cassava"

cprices.loc[cprices["code"]==109,"cropID"] = "Sweet potatoes"
cprices.loc[cprices["code"]==110,"cropID"] = "Rice"
cprices.loc[cprices["code"].isin([111,112,113]),"cropID"] = "Maize"

cprices.loc[cprices["code"]==115, "cropID"] = "Finger millet"
cprices.loc[cprices["code"]==116,"cropID"] = "Sorghum"
cprices.loc[cprices["code"]==146,"cropID"] = "Simsim"
cprices.loc[cprices["code"]==137,"cropID"] = "Cabbages"
cprices.loc[cprices["code"]==138,"cropID"] = "Dodo"
cprices.loc[cprices["code"]==136,"cropID"] = "Tomatoes"
cprices.loc[cprices["code"]==135,"cropID"] = "Onions"
cprices.loc[cprices["code"]==165,"cropID"] = "Pumpkins"
cprices.loc[cprices["code"]==168,"cropID"] = "Eggplants"
cprices.loc[cprices["code"]==170,"cropID"] = "Pineapples"
cprices.loc[cprices["code"]==132,"cropID"] = "Mango"
cprices.loc[cprices["code"]==130,"cropID"] = "Passion fruit"
cprices.loc[cprices["code"]==166,"cropID"] = "Avacoda"
cprices.loc[cprices["code"]==148,"cropID"] = "Coffee"
cprices.loc[cprices["code"]==149,"cropID"] = "Tea"

cprices.loc[cprices["code"].isin([140,141]),"cropID"] = "Beans"
cprices.loc[cprices["code"].isin([142,143,144,184]),"cropID"] = "Groundnuts"

cprices.loc[cprices["code"].isin([145,162]),"cropID"] = "Peas"

cprices.drop(["code"], axis=1, inplace=True)

# Set of prices
prices = prices.merge(cprices, on="cropID", how="left")
prices[["m_p","gate_p"]] = prices[["m_p","gate_p"]].fillna(0)

#For the items that do not have consumption prices input the selling ones.
prices.loc[prices["m_p"]==0, ["m_p"]] = prices.loc[prices["m_p"]==0, "med_prices"]
prices.loc[prices["gate_p"]==0, ["gate_p"]] = prices.loc[prices["gate_p"]==0, "med_prices"]
prices.columns = ["cropID","p_sell", "p_c", "p_c_gate"]


ag5b = ag5b.merge(prices, on="cropID", how="left")
quant = ["total","total2","sell","gift","cons","food_prod","animal","seeds","stored"]
priceslist = ["p_sell"] 
#to check production value for the 3 type of prices uncomment:
# priceslist = ["p_sell", "p_m", "p_gate"] 
values_ag5b = ag5b[["HHID", "trans_cost"]]
#Generate values for each quantities and each type of price. Now I only use for sellings prices since the consumption ones where to big.
for q in quant:
    for p in priceslist:
        values_ag5b[q+"_value_"+p] = ag5b[q]*ag5b[p]


ag5b = values_ag5b.groupby(by="HHID").sum()
ag5b= ag5b.replace(0, np.nan)
ag5b["hh"] = np.array(ag5b.index.values)
sumag5b = ag5b.describe()


"""
# Use reported own produced consumption for crops
crops_c = pd.read_csv("crops_c11.csv")
ag5b = pd.merge(ag5b, crops_c, on="hh")
sumowncrops = ag5b[["cons_value","own_value"]].describe()/dollars
ag5b["cons_value2"] = ag5b["own_value"]/2
ag5b.drop(["own_value"], axis=1)
ag5b["total_value2"] =  ag5b.loc[:,["sells_value_2","gift_value","cons_value2","food_prod_value","animal_value", "seeds_value", "stored_value"]].sum(axis=1)
"""



# Merge datasets -------------------------------------------

agricb = pd.merge(ag3b, ag4b, on='hh', how='outer')
agricb = pd.merge(agricb, ag5b, on='hh', how='outer')



#### Trim the data at the 0.1% both sides
agricb.set_index("hh", inplace=True)

agricb = remove_outliers(agricb, lq=0, hq=0.999)

#Pass it to dollars to see if values make sense or not
summaryb1 = agricb.describe()/dollars
agricb.reset_index(inplace=True)
  

del  ag3b, ag4b, ag5b, prices
#agricb = pd.merge(agricb, basic, on='hh', how='outer')


agricb["cost_agrb"] = -agricb.loc[:,["fet_lab_c","seeds_c","trans_cost"]].sum(axis=1)
agricb["profit_agrb"] = agricb.loc[:,["total2_value_p_sell","rent_owner","rent_noowner","cost_agrb"]].sum(axis=1)
agricb= agricb.replace(0, np.nan)
agB = agricb[["hh", "profit_agrb"]]


sumb = agB.describe()/dollars



#%% Livestock

#Big Animals------------------------------------------------------------
ag6a = pd.read_stata('AGSEC6A.dta')
ag6a = ag6a[["HHID", "lvstid", "a6aq13a", "a6aq13b","a6aq14a","a6aq14b"]]
pd.value_counts(ag6a.lvstid).reset_index()
#Labour paid missing
ag6a.columns = ['HHID',"lvstid","bought", "p_bought", "sold", "p_sold"]

#Once computed the average prices we observed no one reported animals of categories 11 and 12 so we eliminate them.
#ag6a = ag6a[ag6a.LiveStockID!=11]
#ag6a = ag6a[ag6a.LiveStockID!=12]

#Obtain prices animals
prices = ag6a.groupby(by="lvstid")[["p_bought","p_sold"]].median()
p= prices.mean()
prices = prices.fillna(p)
prices["lvstid"] = np.array(prices.index.values)
prices.to_csv('prices_6a_2011.csv')

ag6a = pd.merge(ag6a, prices, on="lvstid", how='outer')
ag6a["value_bought"] = ag6a.bought*ag6a.p_bought_y
ag6a["value_sold"] = ag6a.sold*ag6a.p_sold_y
"""
ag6a["netsales_big"] = ag6a.value_sold.fillna(0) -ag6a.value_bought.fillna(0)
ag6a= ag6a.replace(0, np.nan) 
""" 
ag6a = ag6a.groupby(by='HHID')[["value_sold"]].sum()
ag6a["hh"] = np.array(ag6a.index.values)




#Small animals----------------------
ag6b = pd.read_stata('agsec6b.dta')
ag6b = ag6b[["HHID", "lvstid","a6bq13a","a6bq13b","a6bq14a","a6bq14b"]]
ag6b.columns = ["HHID", "lvstid", "bought", "p_bought", "sold", "p_sold"]
#pd.value_counts(ag6b.lvstid).reset_index()
prices = ag6b.groupby(by="lvstid")[["p_bought","p_sold"]].median()
prices["lvstid"] = np.array(prices.index.values)
prices.to_csv('prices_6b.csv')


ag6b = pd.merge(ag6b, prices, on='lvstid', how='outer')
ag6b["sold_val"] = ag6b["sold"]*ag6b["p_sold_y"]
"""
ag6b["bought_val"] = ag6b["bought"]*ag6b["p_sold_y"]
ag6b["netsales_small"] = ag6b["sold_val"].fillna(0) - ag6b["bought_val"].fillna(0)
"""
ag6b = ag6b.groupby(by="HHID")[["sold_val"]].sum()
ag6b["hh"] = np.array(ag6b.index.values)



#Poultry animals----------------------
ag6c = pd.read_stata('AGSEC6C.dta')
ag6c = ag6c[["HHID", "lvstid", "a6cq13a","a6cq13b","a6cq14a","a6cq14b"]]
ag6c.columns = ['HHID',"lvstid","bought", "p_bought", "sold", "p_sold"]


prices = ag6c.groupby(by="lvstid")[["p_bought","p_sold"]].mean()
prices.iloc[0,:] = prices.iloc[2,:]
prices.iloc[1,:] = prices.iloc[2,:]
prices["lvstid"] = np.array(prices.index.values)

prices.to_csv('prices_6c.csv')

ag6c = pd.merge(ag6c, prices, on="lvstid", how="outer")

ag6c["sold_val2"] = 4*ag6c["sold"]*ag6c["p_sold_y"]
"""
ag6c["bought_val"] = ag6c["bought"]*ag6c["p_bought_y"]
ag6c["netsales_small2"] = ag6c["sold_val"].fillna(0) - ag6c["bought_val"].fillna(0)
ag6c = ag6c.replace(0, np.nan)
"""
ag6c = ag6c.groupby(by='HHID')[["sold_val2"]].sum()

#ag6c.netsales_small2 = 4*ag6c.netsales_small2
ag6c["hh"] = np.array(ag6c.index.values)




# Livestock inputs----------------------
ag7 = pd.read_stata('AGSEC7B.dta')
ag7 = ag7[["HHID", "AGroup_ID","a7bq2e", "a7bq3f", "a7bq5d", "a7bq7c", "a7bq8c"]]
ag7 = ag7.groupby(by="HHID").sum()
ag7["animal_inp"] = ag7.loc[:,["a7bq2e","a7bq3f","a7bq5d","a7bq7c","a7bq8c"]].sum(axis=1)
ag7 = ag7[["animal_inp"]]
ag7["hh"] = np.array(ag7.index.values)
#COST




# Livestock Outputs-------------------------------------------------------------

#Meat sold-----------------------------------------------------------
ag8a = pd.read_stata('AGSEC8A.dta')
ag8a = ag8a[["HHID", "AGroup_ID","a8aq5"]]
values = ["a8aq5"]
index = ["HHID", "AGroup_ID"]
panel = ag8a.pivot_table(values=values, index=index)
ag8a = panel.sum(axis=0, level="HHID")
ag8a.columns = [["meat_sold"]]
del index, panel, values
ag8a["hh"] = np.array(ag8a.index.values)

# Milk bought and Sold------------------------------------------------
ag8b = pd.read_stata('agsec8b.dta')
ag8b = ag8b[["HHID", "AGroup_ID","a8bq5", "a8bq7", "a8bq9"]]
ag8b.columns = ["hh", "AGroup_ID", "own_consumption", "litres_sold", "milk_sold"]

#IMPORTANT PROBLEMS AT INPUTTING PRICES!!! IN MILK AND MANY OTHER PRODUCTS! OWN CONSUMPTION ALWAYS SEEMS TOO BIG VALUE

# Checking website for prices of food in uganda: http://www.infotradeuganda.com/index.php/market-information/food-prices.html
p=1800   #Price of milk last week in uganda march2018. Much lower than our average!!!!!
ag8b["milk_c"] = p*ag8b.own_consumption

ag8b = ag8b[["hh", "AGroup_ID", "milk_c", "milk_sold"]]
values = ["milk_c", "milk_sold"]
index = ['hh',"AGroup_ID"]
panel = ag8b.pivot_table(values=values, index=index)
ag8b = panel.sum(axis=0, level="hh")
ag8b["hh"] = np.array(ag8b.index.values)


# Eggs: 
ag8c = pd.read_stata('agsec8c.dta')
ag8c = ag8c[["HHID", "AGroup_ID","a8cq2", "a8cq3", "a8cq5"]]
ag8c.columns = ["hh", "AGroup_ID", "own_consumption", "quant_sold", "egg_sold"]
ag8c.own_consumption = 4*ag8c.own_consumption
ag8c.value_sold = 4*ag8c.egg_sold
ag8c["price"] =  ag8c.egg_sold/ag8c.quant_sold
price = ag8c["price"]
price.describe()
count_p = pd.value_counts(price).reset_index()
p = price.mean()
ag8c["egg_c"] = p*ag8c.own_consumption

ag8c = ag8c[["hh", "AGroup_ID", "egg_c", "egg_sold"]]
values = ["egg_c", "egg_sold"]
index = ['hh',"AGroup_ID"]
panel = ag8c.pivot_table(values=values, index=index)
ag8c = panel.sum(axis=0, level="hh")
ag8c["hh"] = np.array(ag8c.index.values)




#Extension service---------------------------------------------------
ag9 = pd.read_stata('agsec9.dta')
ag9 = ag9[["HHID", "a9q2","a9q9"]]
ag9.columns = ["hh", "a9q2", "consulting_cost"]
values = [ "consulting_cost"]
index = ['hh', "a9q2"]
panel = ag9.pivot_table(values=values, index=index)
ag9 = panel.sum(axis=0, level="hh")
ag9["hh"] = np.array(ag9.index.values)


#Machinery-----------------------------------------------------------
ag10 = pd.read_stata('AGSEC10.dta')
ag10 = ag10[["HHID", "itmcd", "a10q8"]]
ag10.columns = ["hh", "itemcd", "rent_tools_cost"]
values = [ "rent_tools_cost"]
index = ['hh', "itemcd"]
panel = ag10.pivot_table(values=values, index=index)
ag10 = panel.sum(axis=0, level="hh")
ag10["hh"] = np.array(ag10.index.values)



#Merge datasets------------------------------------------------------
livestock = pd.merge(ag6a, ag6b, on='hh', how='outer')
livestock = pd.merge(livestock, ag6c, on='hh', how='outer')
livestock = pd.merge(livestock, ag7, on='hh', how='outer')
livestock = pd.merge(livestock, ag8a, on='hh', how='outer')
livestock = pd.merge(livestock, ag8b, on='hh', how='outer')
livestock = pd.merge(livestock, ag8c, on='hh', how='outer')
livestock = pd.merge(livestock, ag9, on='hh', how='outer')
livestock = pd.merge(livestock, ag10, on='hh', how='outer')


del ag6c, ag7,ag8a,ag8b, ag8c, ag9,ag10, prices, p, index, count_p, panel, price, values
#Pass it to dollars to see if values make sense or not
livestock2 = livestock.loc[:, livestock.columns != 'hh']/2586.89

summaryl1 = livestock2.iloc[:,0:7].describe()
summaryl2 = livestock2.iloc[:,7:16].describe()
print(summaryl1.to_latex())
print(summaryl2.to_latex())


# Self-consumed production recovered by consumption questionaire:
animal_c = pd.read_csv("c_animal11.csv")
livestock = pd.merge(livestock, animal_c, on="hh", how="outer")
livestock.rename(columns={'own_value':'animal_c'}, inplace=True)
livestock.drop(["milk_c","egg_c"], axis=1, inplace=True)

sumlivestock = livestock.describe()

livestock["revenue"] =livestock.loc[:,["value_sold","sold_val","sold_val2","meat_sold","animal_c","milk_sold", "earned_draught", "sold_dung"]].sum(axis=1) 
livestock["cost"] = -livestock.loc[:,["animal_inp","consulting_cost","rent_tools_cost"]].sum(axis=1) 
livestock["profit_ls"] = livestock.loc[:,["revenue","cost"]].sum(axis=1)

ls = livestock[["hh","profit_ls"]]
ls = ls.dropna()

# Trimming 1% and 1% each tail
ls['percentiles'] = pd.qcut(ls["profit_ls"], [0.01,0.999], labels = False)
ls.dropna(axis=0, subset=['percentiles'], inplace=True)
ls.drop('percentiles', axis=1, inplace=True)

sumls = ls.profit_ls.describe()/dollars

#%% MERGE

farm = pd.merge(agA, agB, on="hh", how="outer")
farm = pd.merge(farm, ls, on="hh", how="outer")

farm["profit_agr"] = farm.loc[:,["profit_agr","profit_agra","profit_agrb"]].sum(axis=1)
farm["total_agrls"] = farm.loc[:,["profit_agr","profit_ls"]].sum(axis=1)
del farm["profit_agra"], farm["profit_agrb"]
farm.to_csv("income_agsec_1112.csv")


farm2 = farm.loc[:, farm.columns != 'hh']/2586.89
summaryfarm = farm2.describe()
print(summaryfarm.to_latex())
