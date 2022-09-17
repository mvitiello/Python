"""
Created on Sun Sep 11 16:20:09 2022

@author: Miguel
"""

# libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# import data
file = 'Account.xlsx'
data_read = pd.ExcelFile(file)

# list sheets 
data_read.sheet_names

# read sheet
data_f = data_read.parse('Account')
data_p = data_read.parse('Last')


# head 
data_f.head()

# describe
data_f.info()

# plot Acum_loc_quantity
plt.figure(figsize=(10, 10))
plt.plot(data_f['Date'],data_f['Acum_loc_quantity'])
plt.xticks(rotation=90)
plt.title('Accumulative Money Invested')
plt.xlabel('Date')
plt.ylabel('Money Invested')
plt.show()
plt.savefig('Accum_Invested_Money.png')

# describe Accum Quantity in each month/year

# try

data_f.pivot_table(values = ['loc_quantity'], 
                   index = ['m', 'y'], 
                   aggfunc = np.sum)

# it is not the result require
# create a empty df
d_inv_by_month_years = pd.DataFrame()

# a for loop is used 
years = data_f['y'].drop_duplicates()

for k in years:
    d = data_f[data_f['y'] == k].pivot_table(values  = ['loc_quantity'], 
                                             index   = ['m', 'y'], 
                                             aggfunc = np.sum)
    # fill the df in every loop
    d_inv_by_month_years = pd.concat([d_inv_by_month_years, d])

# check
d_inv_by_month_years.head(20)

# describe Acum Quantity in each month/year
d_inv_by_years = data_f.pivot_table(values = ['loc_quantity'], 
                                    index = 'y', 
                                    aggfunc = np.sum)
d_inv_by_years.head()

# describe the data

# drop duplicates
data_f_nduplicates = data_f[['Name', 'Sector', 'Country',
                             'Category1', 'Category2','Category3']].drop_duplicates()

# by Tickers
d_byTickers = data_f.pivot_table(values = ['shares', 'loc_quantity'], 
                                 index = 'Name', 
                                 aggfunc = np.sum)

d_byTickers = d_byTickers.merge(data_p[['Name','Last']], left_on = 'Name', 
                                right_on = 'Name')
d_byTickers['Market_Value'] = d_byTickers['Last'] * d_byTickers['shares']
d_byTickers['Market_Value_%'] = d_byTickers['Market_Value']/d_byTickers['Market_Value'].sum()
d_byTickers = d_byTickers.merge(data_f_nduplicates, left_on = 'Name', 
                                right_on = 'Name')
print(d_byTickers)

# by sector
d_bySector = d_byTickers.pivot_table(values = 'Market_Value', 
                                     index = 'Sector', 
                                     aggfunc = np.sum)
d_bySector['Market_Value_%'] = d_bySector['Market_Value']/d_bySector['Market_Value'].sum()
print(d_bySector)

# by country
d_byCountry = d_byTickers.pivot_table(values = 'Market_Value', 
                                      index = 'Country', 
                                      aggfunc = np.sum)
d_byCountry['Market_Value_%'] = d_byCountry['Market_Value']/d_byCountry['Market_Value'].sum()
print(d_byCountry)

# by category1 (type of instrument)
d_byInstrument = d_byTickers.pivot_table(values = 'Market_Value', 
                                         index = 'Category1', 
                                         aggfunc = np.sum)
d_byInstrument['Market_Value_%'] = d_byInstrument['Market_Value']/d_byInstrument['Market_Value'].sum()
print(d_byInstrument)

# by category2 (exchange)
d_byExchange = d_byTickers.pivot_table(values = 'Market_Value', 
                                       index = 'Category2', 
                                       aggfunc = np.sum)
d_byExchange['Market_Value_%'] = d_byExchange['Market_Value']/d_byExchange['Market_Value'].sum()
print(d_byExchange)

# by category3 (asset allocation)
d_byAssetAlocation = d_byTickers.pivot_table(values = 'Market_Value', 
                                             index = 'Category3', 
                                             aggfunc = np.sum)
d_byAssetAlocation['Market_Value_%'] = d_byAssetAlocation['Market_Value']/d_byAssetAlocation['Market_Value'].sum()
print(d_byAssetAlocation)

# calculate simple and annualized return
simple_return = d_byTickers['Market_Value'].sum() / d_inv_by_years['loc_quantity'].sum() - 1
print('The simple return is {}%'.format(100*simple_return.round(4)))
annualized_return = (1+simple_return)**(1/(years.max()-years.min())) - 1
print('The annualized return is {}%'.format(100*annualized_return.round(4)))









