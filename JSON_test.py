'''
this is sample code from Python for data analysis
starting from  page 212

It demo JSON format that is not ready for analysis as each line is food with two lists: nutrients and portion sizes

for inline plots don't forget to start it with --matplotlib inline
'''

import json
import pandas as pd

import matplotlib.pyplot as plt
from IPython.display import display

## GET DATA
########################################## 


# read data
db = json.load(open('foods-2011-10-03.json'))
len(db) #Each entry is a dict containing all the data for a single food

# get keys from first food type 
db[0].keys() 
db[0]['nutrients'][0]

# load data to df
nutrients = pd.DataFrame(db[0]['nutrients'])
nutrients[:5]

## BASIC ANALYSIS
########################################## 

# specify a list of fields to extract to df
info_keys = ['description', 'group', 'id', 'manufacturer']
info = pd.DataFrame(db, columns=info_keys)
info[:5]
info.info()

pd.value_counts(info.group)[:10]


## ANALYSIS
########################################## 
'''
to do analysis on all of the nutrient data, it’s easiest to assemble the nutrients for each food into a single large table.
'''


nutrients = [] 
for rec in db: #get each list of food nutrients
  fnuts = pd.DataFrame(rec['nutrients']) #convert list to a df
  fnuts['id'] = rec['id'] #add a column for the food  id 
  nutrients.append(fnuts) #append the DataFrame to a list
nutrients = pd.concat(nutrients, ignore_index=True)

nutrients.duplicated().sum() # we got quite a few duplicates
nutrients = nutrients.drop_duplicates()

# rename columns
col_mapping = {'description' : 'food','group' : 'fgroup'}
info = info.rename(columns=col_mapping, copy=False)
info.info()

col_mapping = {'description' : 'nutrient','group' : 'nutgroup'}
nutrients = nutrients.rename(columns=col_mapping, copy=False)

#Now we are ready to merge info with  nutrients

ndata = pd.merge(nutrients, info, on='id', how='outer')
ndata.info()

## VISUALS
########################################## 
%matplotlib

result = ndata.groupby(['nutrient', 'fgroup'])['value'].quantile(0.5)
result['Zinc, Zn'].order().plot(kind='barh')

# find which food is most dense in each nutrient
by_nutrient = ndata.groupby(['nutgroup', 'nutrient'])
get_maximum = lambda x: x.xs(x.value.idxmax()) #inline function
get_minimum = lambda x: x.xs(x.value.idxmin())
max_foods = by_nutrient.apply(get_maximum)[['value', 'food']]

# make the food a little smaller
max_foods.food = max_foods.food.str[:50]
max_foods.ix['Amino Acids']['food']