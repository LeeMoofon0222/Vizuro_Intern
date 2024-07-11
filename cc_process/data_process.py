import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder

data = pd.read_csv('cc_test.csv')

data = data.iloc[:, 1:]

categorical_features = ['Subscription Type']


encoder = OrdinalEncoder(categories=[['Basic', 'Standard', 'Premium']])

data[categorical_features] = encoder.fit_transform(data[categorical_features])


data[categorical_features] = data[categorical_features].astype(int)

categorical_features = ['Contract Length']


encoder = OrdinalEncoder(categories=[['Monthly', 'Quarterly', 'Annual']])

data[categorical_features] = encoder.fit_transform(data[categorical_features])


data[categorical_features] = data[categorical_features].astype(int)
# data = pd.get_dummies(data, columns=categorical_features,dtype=int)

# data.rename(columns={
#     'Subscription Type_Basic': 'Basic',
#     'Subscription Type_Premium': 'Premium',
#     'Subscription Type_Standard': 'Standard',
#     'Contract Length_Annual': 'Annual',
#     'Contract Length_Monthly': 'Monthly',
#     'Contract Length_Quarterly': 'Quarterly',
# }, inplace=True)


#data[['Gender']] = data[['Gender']].replace(to_replace={'Male': 1, 'Female': 0})
# data[['Basic', 'Premium', 'Standard', 'Annual', 'Monthly', 'Quarterly']] = data[['Basic', 'Premium', 'Standard', 'Annual', 'Monthly', 'Quarterly']].replace(to_replace={'TRUE': 1, 'FALSE': 0})

grouped = data.groupby('Churn')

data = grouped.apply(lambda x: x.sample(grouped.size().min())).reset_index(drop=True)

data.to_csv('processed_data_v2.csv', index=False)