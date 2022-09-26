# -*- coding: utf-8 -*-
"""Visualization-covid19-Georgia.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nfyKJP7xlI-4w3tPABJxxyMCbJfcpzPk
"""



"""# Step 1: Loading in packages"""

# Packages related to loading and performing basic
# data transformation
import pandas as pd
import numpy as np

print('cell succesfully ran')

# Loading in packages for visualizations to help with data
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

sns.set_theme(style="whitegrid")
print('cell succesfully ran')

"""# Loading in Data"""

dataframe = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_Microcourse_Visualization/main/Data/Georgia_COVID/Georgia_COVID-19_Case_Data.csv')

dataframe

len(dataframe)

dataframe.shape

"""## Describing the varibales"""

dataframe.info()

list(dataframe)

dataframe['COUNTY'].value_counts()

dataframe_counties = dataframe['COUNTY'].value_counts()
dataframe_counties.head(20)

"""## Transforming Columns"""

dataframe['DATESTAMP']

from pandas.io.sql import date
## Creating a copy of the existing datestamp column, so we can keep
# the original version to overide if we wanted to.

dataframe['DATESTAMP_MOD'] = dataframe['DATESTAMP']
print(dataframe['DATESTAMP_MOD'].head(10))
print(dataframe['DATESTAMP_MOD'].dtypes)

dataframe

dataframe['DATESTAMP_MOD'] = pd.to_datetime(dataframe['DATESTAMP_MOD'])
dataframe['DATESTAMP_MOD'].dtypes

dataframe[['DATESTAMP', 'DATESTAMP_MOD']]

dataframe['DATESTAMP_MOD_DAY'] = dataframe['DATESTAMP_MOD'].dt.date
dataframe['DATESTAMP_MOD_DAY']

dataframe['DATESTAMP_MOD_YEAR'] = dataframe['DATESTAMP_MOD'].dt.year 
dataframe['DATESTAMP_MOD_MONTH'] = dataframe['DATESTAMP_MOD'].dt.month

dataframe['DATESTAMP_MOD_YEAR']

dataframe['DATESTAMP_MOD_MONTH']

dataframe

dataframe['DATESTAMP_MOD_MONTH_YEAR'] = dataframe['DATESTAMP_MOD'].dt.to_period('M') 
dataframe['DATESTAMP_MOD_MONTH_YEAR'].sort_values()

dataframe

dataframe['DATESTAMP_MOD_WEEK'] = dataframe['DATESTAMP_MOD'].dt.week 
dataframe['DATESTAMP_MOD_WEEK']

dataframe['DATESTAMP_MOD_QUARTER'] = dataframe['DATESTAMP_MOD'].dt.to_period('Q')  
dataframe['DATESTAMP_MOD_QUARTER']

dataframe['DATESTAMP_MOD_QUARTER'].sort_values()

dataframe['DATESTAMP_MOD_DAY_STRING'] = dataframe['DATESTAMP_MOD_DAY'].astype(str)
dataframe['DATESTAMP_MOD_WEEK_STRING'] = dataframe['DATESTAMP_MOD_WEEK'].astype(str)
dataframe['DATETIME_STRING'] = dataframe['DATESTAMP_MOD_MONTH_YEAR'].astype(str)

dataframe

"""## Getting the counties needed for our analysis

The counties we want to analyze are:


*   Cobb
*   Dekalb
*   Fulton
*   Gwinnett
*   Hall
"""

dataframe['COUNTY']

countlist = ['COBB', 'DEKALB', 'FULTON', 'GWINNETT', 'HALL']
countlist

selectCounties = dataframe[dataframe['COUNTY'].isin(countlist)]
len(selectCounties)

"""## Getting the specific date and time frame we want

`dataframe` = length 91,691
`selectCounties` = 2,830
`selectCountyTime = ???
"""

selectCountyTime = selectCounties

selectCountyTime['DATESTAMP_MOD_MONTH_YEAR']

selectCountyTime_april2020 = selectCountyTime[selectCountyTime['DATESTAMP_MOD_MONTH_YEAR'] == '2020-04']
len(selectCountyTime_april2020)

selectCountyTime_aprilmay2020 = selectCountyTime[(selectCountyTime['DATESTAMP_MOD_MONTH_YEAR'] == '2020-05') | (selectCountyTime['DATESTAMP_MOD_MONTH_YEAR'] == '2020-04')]
len(selectCountyTime_aprilmay2020)

selectCountyTime_aprilmay2020.head(50)

"""## Creating the final dataframe / Specific columns-features-attributes that we want"""

finaldf = selectCountyTime_aprilmay2020[[
    'COUNTY', 
    'DATESTAMP_MOD', 
    'DATESTAMP_MOD_DAY', 
    'DATESTAMP_MOD_DAY_STRING', 
    'DATETIME_STRING', 
    'DATESTAMP_MOD_MONTH_YEAR', 
    'C_New', #cases - new
    'C_Cum', #cases - total
    'H_New', #hospitalizations - new
    'H_Cum', #hospitalizations - total
    'D_New', #deaths - new
    'D_Cum', #deaths - total
]]

finaldf

"""# Looking at total covid cases by month"""

#dropping duplicated rows
finaldf_dropdups = finaldf.drop_duplicates(subset=['COUNTY', 'DATETIME_STRING'],keep='last')
finaldf_dropdups

pd.pivot_table(finaldf_dropdups, values='C_Cum', index='COUNTY',
               columns=['DATESTAMP_MOD_MONTH_YEAR'], aggfunc=np.sum)

vis1 = sns.barplot(x='DATESTAMP_MOD_MONTH_YEAR', y='C_Cum', data=finaldf_dropdups)

vis2 = sns.barplot(x='DATESTAMP_MOD_MONTH_YEAR', y='C_Cum', hue='COUNTY', data=finaldf_dropdups)

plotly1 = px.bar(finaldf_dropdups, x='DATETIME_STRING', y='C_Cum', color='COUNTY', barmode='group')
plotly1.show()

plotly2 = px.bar(finaldf_dropdups, x='DATETIME_STRING', y='C_Cum', color='COUNTY', barmode='stack')
plotly2.show()

"""## Looking at total covid cases by Day"""

daily = finaldf
daily
len(daily)

pd.pivot_table(daily, values='C_Cum', index='COUNTY', columns=['DATESTAMP_MOD_DAY'], aggfunc=np.sum)

tempdf = pd.pivot_table(daily, values='C_Cum', index='DATESTAMP_MOD_DAY', columns=['COUNTY'], aggfunc=np.sum)
tempdf.head(50)

startdate = pd.to_datetime('2020-04-26').date()
enddate = pd.to_datetime('2020-05-09').date()

maskFilter = (daily['DATESTAMP_MOD_DAY']>= startdate) & (daily['DATESTAMP_MOD_DAY']<= enddate)
dailySpecific = daily.loc[maskFilter]
dailySpecific

dailySpecific[dailySpecific['COUNTY'] == 'FULTON']

vis3 = sns.lineplot(data=dailySpecific, x='DATESTAMP_MOD_DAY', y='C_Cum')

vis4 = sns.lineplot(data=dailySpecific, x='DATESTAMP_MOD_DAY', y='C_Cum', hue='COUNTY')

plotly3 = px.bar(dailySpecific, x='DATESTAMP_MOD_DAY', y='C_Cum', color='COUNTY')
plotly3.show()

plotly4 = px.bar(dailySpecific, x='DATESTAMP_MOD_DAY', y='H_New', color='COUNTY', barmode='group')
plotly4.show()

plotly5 = px.bar(dailySpecific, x='DATESTAMP_MOD_DAY', y='H_Cum', color='COUNTY', barmode='group')
plotly5.show()

plotly6 = px.bar(dailySpecific, x='DATESTAMP_MOD_DAY', y='D_New', color='COUNTY', barmode='group')
plotly6.show()

plotly7 = px.bar(dailySpecific, x='DATESTAMP_MOD_DAY', y='D_Cum', color='COUNTY', barmode='group')
plotly7.show()

dailySpecific['newhospandDeathCovid'] = dailySpecific['D_New'].astype(int) + dailySpecific['H_New'].astype(int) + dailySpecific['C_New'].astype(int)
dailySpecific['newhospandDeathCovid']

dailySpecific['newhospandDeath'] = dailySpecific['D_New'].astype(int) + dailySpecific['H_New'].astype(int)
dailySpecific['newhospandDeath']

dailySpecific

plotly8 = px.bar(dailySpecific, 
                 x='DATESTAMP_MOD_DAY', 
                 y='newhospandDeathCovid', 
                 color='COUNTY', 
                 title='Georgia 2020 COVID Data: Total New Hospitilizations, Deaths, and COVID cases by County',
                 labels={
                     'DATESTAMP_MOD_DAY': 'Time (Month, Day, year)',
                     'newhospandDeathCovid': 'Total Count'
                 },
                 barmode='group')


plotly8.update_layout(
    xaxis = dict(
        tickmode='linear',
        type='category'
    )
)
plotly8.show()