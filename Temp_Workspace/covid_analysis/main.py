# %%
import pandas
import numpy
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

# %%
data=pandas.read_csv('./states.csv')

# %%
data['Tested']=data['Tested'].fillna(0)

# %%
data

# %%
data.describe()

# %%
data.head()

# %%
data.tail()

# %%
correlation_matrix=data.corr()

# %%
correlation_matrix

# %%
data.info()

# %%
mhData=data[data.State=='Maharashtra']

# %%
tempData=mhData['Confirmed']-mhData['Recovered']-mhData['Deceased']-mhData['Other']

# %%
tempData

# %%
mhData['Active']=tempData

# %%
mhData.sort_values(by='Date')

# %%
mhData.plot(kind='line',x="Date",y="Confirmed",figsize=(20,10))

# %%
mhData.plot(kind='line',x="Date",y="Recovered",figsize=(20,10))

# %%
mhData.plot(kind='line',x="Date",y="Deceased",figsize=(20,10))

# %%
mhData.plot(kind='line',x="Date",y="Tested",figsize=(20,10))

# %%


# %%


# %%
mhData['Date']

# %%
x=mhData['Date']
y=mhData['Active']

# %%
plt.rcParams['figure.figsize'] = [20,10]

plt.plot(x,y)

# %%


# %%
