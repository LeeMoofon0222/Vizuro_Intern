import pandas as pd


data_path = 'cc_test.csv' 
data = pd.read_csv(data_path)



data = data.iloc[:, 1:]

data.to_csv('cc_test(dropID).csv', index=False)