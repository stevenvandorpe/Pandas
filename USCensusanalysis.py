census_df = pd.read_csv('census.csv')
census_df = census_df.where(census_df['SUMLEV'] == 50)
listofstatesori = list(census_df['STNAME'].unique())
census_df = census_df.dropna()
df = census_df
my_list = []
testlist = ['Alabama', 'Texas']

for state in listofstatesori:
    my_list.append((df[df['STNAME'] == state].count())[1])
    
my_list

eindelijk = pd.Series(my_list, index=listofstatesori)

eindelijk.sort_values(axis=0, ascending=False, inplace=True)

eindelijk.index[0]


census_df = census_df.where(census_df['SUMLEV'] == 50)
census_df = census_df.dropna()
columns_to_keep = ['CTYNAME', 'STNAME', 'CENSUS2010POP']
ds = census_df[columns_to_keep]

listofstatesori = list(ds['STNAME'].unique())
testlist = ['North Dakota', 'Ohio', 'Rhode Island']

listtop3 = []

for state in listofstatesori:
    if state != 'District of Columbia':
        newdf = ds[ds['STNAME'] == state].nlargest(3, 'CENSUS2010POP')
        tuti = newdf.iloc[0]['CENSUS2010POP'] + newdf.iloc[1]['CENSUS2010POP'] +  newdf.iloc[2]['CENSUS2010POP']
        listtop3.append([tuti, state])
                
finallist = []
for e in [4,42,12]:
  finallist.append(pd.Series(listtop3).sort_values(ascending=False)[e][1])

def answer_six():
    return finallist
	
	
columns_to_keep = ['CTYNAME', 'STNAME', 'POPESTIMATE2010', 'POPESTIMATE2011', 'POPESTIMATE2012', 'POPESTIMATE2013', 'POPESTIMATE2014', 'POPESTIMATE2015']
ds = census_df[columns_to_keep]

ds['BIGESTDIFINPOP'] = ds['POPESTIMATE2015'] - ds['POPESTIMATE2010']

ds.sort('BIGESTDIFINPOP', inplace=True, ascending=False)

def answer_seven():
    return ds.iloc[0]['CTYNAME']
	
	
tries = []


for e in range(3142):
    eerder = []
    if census_df.iloc[e]['REGION'] == 1 or census_df.iloc[e]['REGION'] == 2:
        if census_df.iloc[e]['POPESTIMATE2015'] > census_df.iloc[e]['POPESTIMATE2014']:
            if census_df.iloc[e]['CTYNAME'] == 'Washington County':
                eerder.append(census_df.index[e])
                eerder.append(census_df.iloc[e]['STNAME'])
                eerder.append(census_df.iloc[e]['CTYNAME'])
                tries.append(eerder)
                
def answer_eight():
    frame = pd.DataFrame(tries)
    
    frame = frame.set_index(0)
    frame.columns = ['STNAME', 'CTYNAME']    
    return frame