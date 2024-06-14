#!/usr/bin/env python
# coding: utf-8

# #### Combining csv Files

# In[1]:


import pandas as pd


# In[2]:


df1 = pd.read_csv(r"C:\Users\hanna\OneDrive\Desktop\Jupyter Projects\AO3 Analysis\worksData_01_sql.csv")
df2 = pd.read_csv(r"C:\Users\hanna\OneDrive\Desktop\Jupyter Projects\AO3 Analysis\worksData_02_sql.csv")
df3 = pd.read_csv(r"C:\Users\hanna\OneDrive\Desktop\Jupyter Projects\AO3 Analysis\worksData_03_sql.csv")
df4 = pd.read_csv(r"C:\Users\hanna\OneDrive\Desktop\Jupyter Projects\AO3 Analysis\worksData_04_sql.csv")


# In[3]:


dfNew = pd.concat([df4, df3, df2, df1], ignore_index=True)


# In[4]:


dfNew.to_csv(r"C:\Users\hanna\OneDrive\Desktop\Jupyter Projects\AO3 Analysis\worksData_Cumulative.csv", index=False)


# In[ ]:




