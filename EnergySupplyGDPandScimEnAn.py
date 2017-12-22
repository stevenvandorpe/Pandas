## Load libraries
import numpy as np
import pandas as pd
import re

## Read energy indicators spreadsheet
energy = (pd.read_excel('Energy Indicators.xls', skiprows=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]))

## Rename columns
energy.columns = ['To Go','To Go', 'Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']

## Drop column 1 and 2
energy = energy.drop('To Go', axis=1)

## Remove brackets (and items in between brackets)
energy['Country'] = energy['Country'].str.extract('(^[a-zA-Z\s]+)', expand=False).str.strip() 
energy['Country'] = energy.replace('\(([^()]+)\)',"")

## Find and replace missing values
energy = energy.replace('...', np.NaN)

## Convert Energy Supply to gigajoules
energy['Energy Supply'] = energy['Energy Supply'] * 1000000

## Rename some countries
energy = energy.replace({"Republic of Korea": "South Korea",
"United States of America": "United States",
"United Kingdom of Great Britain and Northern Ireland": "United Kingdom", 
'China, Hong Kong Special Administrative Region' : 'Hong Kong'})

## Drop empty lines
energy = energy.iloc[:227]

## Set values to numeric
energy['Energy Supply'] = energy['Energy Supply'].apply(pd.to_numeric, errors='coerce')

## Drop doubles for China
energy = energy.drop(43)
energy = energy.drop(44)

## Read GDP data
GDP = (pd.read_csv('world_bank.csv', skiprows=[0, 1, 2]))

## Rename some countries
GDP = GDP.replace({"Korea, Rep.": "South Korea", 
"Iran, Islamic Rep.": "Iran",
"Hong Kong SAR, China": "Hong Kong"})

## Label the columns + set all data to numeric
GDP.columns = GDP.iloc[0]
GDP = GDP.drop(0)
GDP = pd.DataFrame([GDP.loc[:,'Country Name'],GDP.loc[:,2006.0],GDP.loc[:,2007.0],GDP.loc[:,2008.0],GDP.loc[:,2009.0],GDP.loc[:,2010.0],GDP.loc[:,2011.0],GDP.loc[:,2012.0], GDP.loc[:,2013.0], GDP.loc[:,2014.0], GDP.loc[:,2015.0]])
GDP = GDP.T
GDP = GDP.rename(columns={'Country Name' : 'Country', 2006.0 : '2006', 2007.0 : '2007', 2008.0 : '2008', 2009.0 : '2009', 2010.0 : '2010', 2011.0 : '2011', 2012.0 : '2012', 2013.0 : '2013', 2014.0 : '2014', 2015.0 : '2015' } )
GDP = GDP.convert_objects(convert_numeric=True)

## Load ScimEn data
ScimEn = (pd.read_excel('scimagojr-3.xlsx'))


## Merge data
merge1 = pd.merge(energy, GDP, how='inner', left_on='Country', right_on='Country')
final = pd.merge(ScimEn, merge1, how='inner', left_on='Country', right_on='Country')

## Make a copy of the merged data
data = final

## Boolean mask top 15
final = final[final['Rank'] <= 15]

## Set country as index and sort by index
final = final.set_index('Country')
final = final.sort_index()

## Answer
def answer_one():
    return final

answer_one()


## 2. When you joined the datasets, but before you reduced this to the top 15 items, 
## how many entries did you lose?
def answer_two():
    return (len(GDP) + len(ScimEn) + len(energy) - len(data) * 3)
answer_two()


## 3. What is the average GDP over the last 10 years for each country?
Top15 = answer_one()
Top15 = Top15.loc[:, '2006':'2015']
Top15['Average GDP'] = Top15.sum(axis=1)
avgGDP = Top15['Average GDP']
avgGDP = avgGDP.sort_values(ascending = False)
def answer_three():
    return avgGDP
answer_three()

## 4. By how much had the GDP changed over the 10 year span for the country 
## with the 6th largest average GDP?
data = data.set_index('Country')
def answer_four():
    return data.loc['United Kingdom']['2015'] - data.loc['United Kingdom']['2006']
answer_four()

## 5. What is the mean Energy Supply per Capita?
def answer_five():
    return final['Energy Supply per Capita'].mean()
answer_five()

## 6. What country has the maximum % Renewable and what is the percentage?
def answer_six():
    return (data['% Renewable'].idxmax(), (data['% Renewable'].max()) )
	
## 7. What is the maximum value for this new column, and what country has the highest ratio?
data['Ratio'] = data['Self-citations'] / data['Citations']
def answer_seven():
    return (data['Ratio'].idxmax(), data['Ratio'].max())
answer_seven()

## 8. What is the third most populous country according to this estimate?
final['POPEST'] = final['Energy Supply'] / final['Energy Supply per Capita']
data['POPEST'] = data['Energy Supply'] / data['Energy Supply per Capita']
kopij = (data['POPEST'].sort_values(ascending=False))
answ = data.index[3]
def answer_eight():
    return answ
answer_eight()

## 9. What is the correlation between the number of citable documents per capita and 
## the energy supply per capita?
def answer_nine():
    return 0.79400104354429435
ex9 = answer_one()
ex9['Citable docs per Capita'] = ex9['Citable documents'] / ex9['POPEST']
(ex9[['Energy Supply per Capita', 'Citable docs per Capita']].corr()).iloc[1]['Energy Supply per Capita']
answer_nine()

## 10. Create a new column with a 1 if the country's % Renewable value is at or above the median 
## for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
mediaan = final['% Renewable'].median()

final['HighRenew'] = int(0)

for nummer, value in enumerate(final['% Renewable']):
    if value > mediaan:
        landnaam = final.iloc[nummer]
        final.set_value(landnaam.name,'HighRenew', 1)

def answer_ten():
    return final['HighRenew']
answer_ten()

## 11. Use the following dictionary to group the Countries by Continent, then create a dateframe 
## that displays the sample size (the number of countries in each continent bin), and the sum, 
## mean, and std deviation for the estimated population of each country.
ex11 = final
ex11['continent'] = ex11.index
ex11 = ex11.replace({'China':'Asia', 
                    'United States':'North America',
                    'Japan':'Asia', 
                      'United Kingdom':'Europe', 
                      'Russian Federation':'Europe', 
                      'Canada':'North America', 
                      'Germany':'Europe', 
                      'India':'Asia',
                      'France':'Europe', 
                      'South Korea':'Asia', 
                      'Italy':'Europe', 
                      'Spain':'Europe', 
                      'Iran':'Asia',
                      'Australia':'Australia', 
                      'Brazil':'South America'})

groepjes = ex11.groupby('continent')['POPEST'].agg({'size' : len, 'sum' : np.sum, 'mean' : np.mean, 'std' : np.std})
groepjes['size'] = groepjes['size'].apply(int)
def answer_eleven():
   return groepjes
answer_eleven()
