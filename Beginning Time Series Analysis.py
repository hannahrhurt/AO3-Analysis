#!/usr/bin/env python
# coding: utf-8

# # Various Time Series Analysis

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import pymannkendall as mk

import math
import datetime
import scipy

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from pmdarima.arima import auto_arima


# In[2]:


df = pd.read_csv(r"C:\Users\hanna\OneDrive\Desktop\Jupyter Projects\AO3 Analysis\worksData_Cumulative.csv")


# In[3]:


df


# To begin our time series analysis, we ought to try and model our time series so that we can use that model to predict future values.

# ## Time Series Modeling

# When modeling a time series, we need our time-series data to be stationary to get any workable model.

# In[4]:


plt.plot(df.index, df["number_of_works"])
plt.show()


# Even the most rudimentary analysis of plotting shows an upward trend in the number of works over time, and so this is not a stationary series.

# In[5]:


plt.plot(df.index, df["number_of_works"])
plt.axis((0,1000,0,10000))
plt.show()


# In[6]:


plt.plot(df.index, df["number_of_works"])
plt.axis((3000,4000,0,10000))
plt.show()


# Based on preliminary observations, we can tell there is definitely a trend, for wich we will take the difference. We also suspect that variance grows with time, and so we will most likely use a logarithmic function before taking the difference.

# ## Seasonal Component?

# If we were wanting to model this variable for purposes of prediction, which we will attempt, we first need to uncover whether or not there is a seasonal component to our data. This will allow us to determine if we ought to fit our data for an ARMIA or SARIMA model.

# In[7]:


plt.plot(df["creation_date"], df["number_of_works"])
plt.show()


# Clearly from the graph above, our variable "creation_date" is formatted as strings, and not as date objects. In order to graph with dates in mind, we first need to convert "creation_date" strings into "creation date2" date objects.

# In[8]:


df["creation date2"] = [dt.datetime.today()]*len(df)

for i in range(len(df)):
    df.loc[i, "creation date2"] = dt.datetime.strptime(df["creation_date"][i], "%m/%d/%Y")
    

df["creation date2"]


# In[9]:


plt.plot(df["creation date2"], df["number_of_works"])
plt.show()


# In[10]:


plt.figure(figsize=(20,5))
plt.plot(df["creation date2"], df["number_of_works"])
#plt.figure(figsize=(20,5))

plt.axvline(dt.datetime(2009, 1, 1), color="red")
plt.axvline(dt.datetime(2010, 1, 1), color="red")
plt.axvline(dt.datetime(2011, 1, 1), color="red")
plt.axvline(dt.datetime(2012, 1, 1), color="red")
plt.axvline(dt.datetime(2013, 1, 1), color="red")
plt.axvline(dt.datetime(2014, 1, 1), color="red")
plt.axvline(dt.datetime(2015, 1, 1), color="red")
plt.axvline(dt.datetime(2016, 1, 1), color="red")
plt.axvline(dt.datetime(2017, 1, 1), color="red")
plt.axvline(dt.datetime(2018, 1, 1), color="red")
plt.axvline(dt.datetime(2019, 1, 1), color="red")
plt.axvline(dt.datetime(2020, 1, 1), color="red")
plt.axvline(dt.datetime(2021, 1, 1), color="red")

plt.show()


# Unfortunately, with this many data points, it is difficult to determine if there is a seasonal component or not. Thus, we turn our attention towards more numeric means of calculation (e.g. seasonal_decompose). Unfortunately, seasonal_decompose requires that an item have a datetime index, so we must reconstruct a new dataframe with a datetime index.

# In[11]:


df2 = pd.DataFrame(df["number_of_works"].copy())


# In[12]:


df2.index = df["creation date2"]
df2.index = pd.DatetimeIndex(df2.index)
idx = pd.date_range(df2.index[0], df2.index[len(df2)-1])
df2 = df2.reindex(idx, fill_value = 0)


# In[13]:


df2


# In[14]:


result = seasonal_decompose(df2["number_of_works"])

result.plot()
plt.show()


# In[15]:


plt.figure(figsize=[20,5])
result.seasonal.plot()
plt.axis((15000,15020,-100,180))
plt.show()


# Very clearly as seen above, there does exist a seasonal component, with a period of 7. This makes sense, as our data is timed daily, and with 7 days to a week, it would make sense for our data to lull and spike throughout the week.
# 
# Given that we can confirm that we have a seasonal component, we will need to use SARIMA rather than ARIMA to get our data stationary. Thankfully, either way, we can use the auto_arima function to run through several variations to determine the best combination of AR, MA, and Seasonal Components.

# In[16]:


acfPlot = plot_acf(df2["number_of_works"])
pacfPlot = plot_pacf(df2["number_of_works"])


# In[17]:


arima_model = auto_arima(df2["number_of_works"], start_p=0, d=1, start_q=0, max_p=5, max_d=5, max_q=5, start_P=0, D=1, start_Q=0,
                         max_P=5, max_D=5, max_Q=5, m=7, seasonal=True, stepwise=True, trace=True, random_state=5, n_fits=50)


# In[18]:


arima_model.summary()


# Now, as we can see above, the SARIMA (or SARIMAX in this instance) model that has the best AIC score is SARIMAX(5,1,0)(5,1,0,7). We also notice that the P>|z| values for each component are less than 0.05, and so they are all significant. The next step is to check our diagnostic plots for anything out of the ordinary.

# In[19]:


diagnosticPlots1 = arima_model.plot_diagnostics(figsize=(7,5))


# Now, very clearly, we don't have a normal distribution, as seen by the histogram, qq-plot, and standardized residuals. Our first attempt to fix this would be to take the log of our data. This will also possibly result in a different SARIMAX model chosen, but if that model passes all of our tests, then all the better.

# In[20]:


for index, values in df2.iterrows():
    if df2.loc[index, "number_of_works"] == 0:
        df2.loc[index, "number_of_works"] = 1


# In[21]:


df2["number_of_works_log"] = [0.1]*len(df2)

for index, values in df2.iterrows():

    df2.loc[index, "number_of_works_log"] = math.log(df2.loc[index, "number_of_works"])


# In[22]:


arima_model = auto_arima(df2["number_of_works_log"], start_p=0, d=1, start_q=0, max_p=5, max_d=5, max_q=5, start_P=0, D=1, start_Q=0,
                         max_P=5, max_D=5, max_Q=5, m=7, seasonal=True, stepwise=True, trace=True, random_state=5, n_fits=50)


# In[23]:


arima_model.summary()


# Similarly as above, we see that the model with the best AIC score is SARIMAX(5,1,0)(5,1,0,7). The P>|z| values for eac component are less tan 0.05, and so they are all significant, and none of the coefficients are significantly smaller as to have little impact. As with above, the next step is to check our diagnostic plots for anything out of the ordinary.

# In[24]:


diagnosticPlots1 = arima_model.plot_diagnostics(figsize=(7,5))


# Similarly as can be seen above, our residuals aren't quire normally distributed, have different variances throughout the time period, and have problems with outliers messing with the model. Unfortunately, for the time being, this is the best we have. In further analysis, we will be using these flawed, but hopefully robust models to attempt predicting future values using cross-validation techniques, and will also be using other transformations to determine if there is a better form the data can take for a more accurate model to take form.

# In[ ]:




