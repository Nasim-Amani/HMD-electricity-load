# -*- coding: utf-8 -*-
"""calendar features.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17Uli1SPh1cDOd0m0N3-WsRW3LiBn0pGQ

[Feature Engineering of DateTime Variables](https://www.kaggle.com/code/nextbigwhat/feature-engineering-of-datetime-variables)


[Seasonal-Trend decomposition using LOESS for multiple seasonal components (MSTL)](https://github.com/KishManani/MSTL/blob/main/mstl_decomposition.ipynb)
"""

import pandas as pd

df=pd.read_csv("df_replaced.csv" )

df['datetime'] = pd.to_datetime(df['datetime'] , utc=True)
#df.set_index('datetime', inplace=True)

# Shift the 'Load' column one hour ahead
df['Load_previous_hour'] = df['Load'].shift(1)

# Drop rows with missing values (NaN) resulting from the shift
df.dropna(inplace=True)



# Shift the 'Load' column 24 hours ahead
df['Load_same_hour_previous_day'] = df['Load'].shift(24)

# Drop rows with missing values (NaN) resulting from the shift
df.dropna(inplace=True)


# Shift the 'Load' column 168 hours ahead
df['Load_same_hour_previous_week'] = df['Load'].shift(168)

# Drop rows with missing values (NaN) resulting from the shift
df.dropna(inplace=True)

#df.head()

df['year'] = df['datetime'].dt.year
df['month'] = df['datetime'].dt.month
df['day'] = df['datetime'].dt.day
df['day_of_week'] = df['datetime'].dt.day_of_week
df['day_of_year'] = df['datetime'].dt.day_of_year
#df[['datetime','date_issued:year','date_issued:month','date_issued:day','date_issued:day_of_week','date_issued:day_of_year']].head()

"""Month1:
5am to 11am
14pm to 18 pm

Month2:
5am to 11am
14pm to 18 pm

Month3:
7am to 12am
16pm to 20 pm

Month4:
7am to 12am
15pm to 20 pm

Month5:
6am to 12am
18pm to 20 pm

Month6:
6am to 12am
-

Month7:
6am to 12am
-

Month8:
6am to 12am
-
Month9:
6am to 12am
-

Month10:
6am to 11am
14pm to 19pm

Month11:
6am to 11am
15pm to 18pm

Month12:
5am to 11am
14pm to 18pm

"""

def day_part(hour):
    if hour in [4,5]:
        return "dawn"
    elif hour in [6,7]:
        return "early morning"
    elif hour in [8,9,10]:
        return "late morning"
    elif hour in [11,12,13]:
        return "noon"
    elif hour in [14,15,16]:
        return "afternoon"
    elif hour in [17, 18,19]:
        return "evening"
    elif hour in [20, 21, 22]:
        return "night"
    elif hour in [23,24,1,2,3]:
        return "midnight"


# utilize it along with apply method
df['hour'] = df['datetime'].dt.hour
df['date_issued:day_part'] = df['hour'].apply(day_part)
#df.head()

from sklearn.preprocessing import LabelEncoder

# Perform label encoding
label_encoder = LabelEncoder()
df['day_part_encoded'] = label_encoder.fit_transform(df['date_issued:day_part'])
df.drop('date_issued:day_part', axis=1, inplace=True)
#df.head()

import numpy as np

df['is_year_start'] = df['datetime'].dt.is_year_start
df['is_quarter_start'] = df['datetime'].dt.is_quarter_start
df['is_month_start'] = df['datetime'].dt.is_month_start
df['is_month_end'] = df['datetime'].dt.is_month_end

df['is_weekend'] = np.where(df['day_of_week'].isin([3,4]), 1,0)

#df[['datetime','date_issued:is_year_start','date_issued:is_quarter_start','date_issued:is_month_start','date_issued:is_month_end']].head()

df['week_number'] = df['datetime'].dt.isocalendar().week

#df.to_csv('all_features2.csv', index=False)

df.set_index('datetime', inplace=True)

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Calculate correlation matrix
corr_matrix = df.corr()

# Create a heatmap plot of correlation values
plt.figure(figsize=(15, 8))
sns.heatmap(corr_matrix, annot=True, cmap='RdYlBu')
plt.title('Correlation Heatmap')
plt.show()



import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
plt.figure(figsize=(15, 8))

# Calculate correlation matrix
corr_matrix = df.corr()

# Create a triangular mask for upper diagonal
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

# Create a heatmap plot of correlation values
sns.heatmap(corr_matrix, annot=True, cmap='RdYlBu', mask=mask)
plt.title('Correlation Heatmap')
plt.show()

