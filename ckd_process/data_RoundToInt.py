import pandas as pd


data_path = 'processed_kidney_disease_2(predict).csv' 
data = pd.read_csv(data_path)


rounded_data = data.select_dtypes(include=['number']).round()
integer_data = rounded_data.astype(int)


non_numeric_data = data.select_dtypes(exclude=['number'])


final_data = pd.concat([integer_data, non_numeric_data], axis=1)

final_data = final_data.iloc[:, 1:]

final_data.to_csv('processed_kidney_disease_2(predict)(RTI).csv', index=False)
