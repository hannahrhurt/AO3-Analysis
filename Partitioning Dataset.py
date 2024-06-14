#!/usr/bin/env python
# coding: utf-8

# # The Necessity of Partitioning our Dataset

# While we are eternally grateful to the AO3 for ethically sourcing some data for us to analyze, the dataset given is unfortunately too large for us to analyze in SQl in one go. Attempting to upload the flat file yields the "Exception of type 'System.OutOfMemoryException' was thrown." So, we will instead, divide our dataset into 4 smaller files for which SQL will have an easier time processing one at a time.

# In[1]:


#pip install pandas


# In[2]:


import pandas as pd


# In[3]:


df = pd.read_csv(r"C:\Users\hanna\OneDrive\Desktop\Jupyter Projects\AO3 Analysis\20210226-stats\works-20210226.csv")


# In[4]:


df


# Now, the best way to segment this data is going to be by date. That is, separating each new file when the creation date is a new value will make it so that combining the synthesized files after the fact will be easier, as there will be no "creation date" day data segmented across two files.

# Since we are dividing this one file into 4, it will be best to start at the quarter, half, and three-quarter markers for what to do.

# In[5]:


df.iloc[round(len(df)/4)]


# In[6]:


df.iloc[round(len(df)/2)]


# In[7]:


df.iloc[round(len(df)/2+len(df)/4)]


# And now, we want to keep these creation dates in mind, but don't want to re-calculate this location every time. So, we will save these values for future use.

# In[8]:


date1 = df.iloc[round(len(df)/4)][0]
date2 = df.iloc[round(len(df)/2)][0]
date3 = df.iloc[round(len(df)/2+len(df)/4)][0]


# Given that we want to seperate the data so there are no "creation dates" shared across files, we need to find the first instance of every date# in the data.

# In[9]:


flag1 = True
flag2 = True
flag3 = True

for i in range(len(df)):
    if flag1 and df["creation date"][i] == date1:
        break1 = i
        flag1 = False
    elif flag2 and df["creation date"][i] == date2:
        break2 = i
        flag2 = False
    elif flag3 and df["creation date"][i] == date3:
        break3 = i
        break


# In[10]:


df1 = df[:break1]
df2 = df[break1:break2]
df3 = df[break2:break3]
df4 = df[break3:]


# Now, we finally display these dataframes to prove that the process worked and the data is evenly divided up with no overlapping "creation dates."

# In[11]:


df1


# In[12]:


df2


# In[13]:


df3


# In[14]:


df4


# Since these 4 new dataframes fulfill the requirements we set up, we now export these dataframes so that SQL can properly deal with them.

# In[15]:


df1.to_csv(r"C:\Users\hanna\OneDrive\Desktop\Jupyter Projects\AO3 Analysis\worksData_01.csv")
df2.to_csv(r"C:\Users\hanna\OneDrive\Desktop\Jupyter Projects\AO3 Analysis\worksData_02.csv")
df3.to_csv(r"C:\Users\hanna\OneDrive\Desktop\Jupyter Projects\AO3 Analysis\worksData_03.csv")
df4.to_csv(r"C:\Users\hanna\OneDrive\Desktop\Jupyter Projects\AO3 Analysis\worksData_04.csv")


# In[ ]:




