import pandas as pd

file_path = 'processed_kidney_disease_2.csv'
data = pd.read_csv(file_path)

original_class_1_count = data[data['classification'] == 0].shape[0]

drop_ratio = 0.22 

class_1_data = data[data['classification'] == 0]

n_drop = int(len(class_1_data) * drop_ratio)

drop_indices = class_1_data.sample(n=n_drop, random_state=42).index

data_dropped = data.drop(drop_indices)

new_class_1_count = data_dropped[data_dropped['classification'] == 0].shape[0]

data_dropped.to_csv('processed_kidney_disease_2(balance).csv', index=False)