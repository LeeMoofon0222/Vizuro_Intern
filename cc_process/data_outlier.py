import pandas as pd


data = pd.read_csv('processed_data_v2.csv')

specified_columns = ['Age', 'Tenure', 'Usage Frequency','Support Calls', 'Payment Delay', 'Contract Length', 'Last Interaction']

for column in specified_columns:
    if column in data.columns:
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        data = data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]


data.to_csv('processed_data_v2.csv', index=False)