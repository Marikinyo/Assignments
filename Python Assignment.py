#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd

import json

from datetime import datetime, timedelta


# In[2]:


features = pd.read_excel('features.xlsx')


# In[3]:


# print(features)


# ## Task Description

# In[4]:


for i in range(len(features)):
    print(features['Logic'][i], '\n', features['If missing value'][i])
    print()
    print('************')


# ## Useful functions

# In[5]:


# replace '' strings with np.nan if any exists
# drop np.nan values and reindex the dataframe
def clean_data(df, column_name):
    df.replace('', np.nan, inplace=True)
    df.dropna(subset=column_name, inplace=True)
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


# In[6]:


def flatten_contracts(df, column_name, contracts_list = []):
    for contracts in df[column_name]:
        if isinstance(contracts, list):
            for contract in contracts:
                contracts_list.append(contract)
        elif isinstance(contracts, dict):
            contracts_list.append(contracts)
    
    return contracts_list


# In[7]:


# convert a list of dictionaries to dataframe
def list_to_dataframe(list_of_data):
    df = pd.DataFrame(list_of_data)
    return df


# In[8]:


def convert_to_datetime(df, column_names):
    if isinstance(column_names, list):
        for column_name in column_names:
            df[column_name] = pd.to_datetime(df[column_name])
    else:
        df[column_names] = pd.to_datetime(df[column_names])
    return df


# ## Loading and proccess the data

# In[9]:


data = pd.read_csv("data.csv")
data.head()


# In[10]:


# Remove Nan values
clean_data(data, ['contracts']).head()


# In[11]:


# json loads
data['contracts'] = data['contracts'].apply(lambda x: json.loads(x) if pd.notnull(x) else np.nan)
data.head()


# In[12]:


# flatten_contracts(data, 'contracts')


# In[13]:


# create dataframe using 'contracts' value
contracts_df = list_to_dataframe(flatten_contracts(data, 'contracts'))
contracts_df.head()


# In[14]:


contracts_df.shape


# In[15]:


# # clean the dataframe and remove empty values
# df_cleaned = clean_data(contracts_df, column_name=['contract_id'])
# df_cleaned.head()  


# In[16]:


# df_cleaned.shape


# In[17]:


print(type(contracts_df['claim_date'][0]))
print(type(contracts_df['contract_date'][0]))


# In[18]:


columns_to_clean = ['claim_date', 'contract_date']
convert_to_datetime(contracts_df, columns_to_clean)
contracts_df.head()


# In[19]:


print(type(contracts_df['claim_date'][0]))
print(type(contracts_df['contract_date'][0]))


# ### number of claims for last 180 days

# In[20]:


print(features['Logic'][0], '\n', features['If missing value'][0])


# In[21]:


df_claims = contracts_df.drop_duplicates(subset='claim_id')


# In[22]:


# difference between the claim_date and today's date in days
df_claims['days_since_claim'] = (datetime.today() - df_claims['claim_date']).dt.days


# In[23]:


df_claims['claim_flag'] = [1 if days <= 180 else 0 for days in df_claims['days_since_claim']]


# In[24]:


print(features['Feature'][0])


# In[25]:


tot_claim_cnt_l180d = [df_claims['claim_flag'].sum() if df_claims['claim_flag'].sum() > 0 else -3]
print('number of claims for last 180 days:', tot_claim_cnt_l180d[0])


# ### Sum of exposue of loans

# In[26]:


print(features['Logic'][1], '\n', features['If missing value'][1])


# In[27]:


# field "bank" is not in ['LIZ', 'LOM', 'MKO', 'SUG']
df_loans = contracts_df[~contracts_df['bank'].isin(['LIZ', 'LOM', 'MKO', 'SUG'])]
# null values should be handled separately
df_loans = df_loans.dropna(subset=['bank'])


# In[28]:


# remove rows from df_loans dataframe where contract_date is null
clean_data(df_loans, column_name=['contract_date'])


# In[29]:


print(features['Feature'][1])


# In[30]:


df_loans['loan_summa'].dtype


# In[31]:


disb_bank_loan_wo_tbc = df_loans['loan_summa'].sum()

if disb_bank_loan_wo_tbc == 0:
    disb_bank_loan_wo_tbc = -1
elif disb_bank_loan_wo_tbc == np.nan:
    disb_bank_loan_wo_tbc = -3

print('Sum of exposue of loans without TBC loans:', disb_bank_loan_wo_tbc)


# ### Number of days since last loan

# In[32]:


print(features['Logic'][2], '\n', features['If missing value'][2])


# In[33]:


# remove rows where 'summa' is nan
loans_df = clean_data(contracts_df, ['summa'])
loans_df.head()


# In[34]:


loans_df['summa'].dtype


# In[35]:


today = pd.to_datetime(datetime.today())

# difference between today and contract_date calculating in days
loans_df['day_since_last_loan'] = (today - loans_df['contract_date']).dt.days


# In[36]:


# In case no claims at all, then put -3 as a value of this feature.
loans_df.loc[loans_df['claim_id'].isnull() | (loans_df['claim_id'] == ''), 'day_since_last_loan'] = -3

# In case no loans at all, then put -1 as a value of this feature.
loans_df.loc[(loans_df['loan_summa'] == 0) | (loans_df['loan_summa'].isnull()), 'day_since_last_loan'] = -1


# In[37]:


# final result
loans_df


# In[ ]:





# In[ ]:





# In[ ]:




