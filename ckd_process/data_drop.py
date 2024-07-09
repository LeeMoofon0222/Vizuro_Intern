import pandas as pd

file_path = 'processed_kidney_disease_3(balance).csv'
data = pd.read_csv(file_path)


data.drop(columns=['age'], inplace=True)
data.drop(columns=['pc'], inplace=True)
data.drop(columns=['pcc'], inplace=True)
data.drop(columns=['ba'], inplace=True)
data.drop(columns=['pcv'], inplace=True)
data.drop(columns=['bgr'], inplace=True)
data.drop(columns=['dm'], inplace=True)
data.drop(columns=['cad'], inplace=True)
data.drop(columns=['appet'], inplace=True)
data.drop(columns=['pe'], inplace=True)
data.drop(columns=['ane'], inplace=True)

data.to_csv('processed_kidney_disease_3(balance)(drop).csv', index=False)    