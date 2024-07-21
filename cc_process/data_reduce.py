import pandas as pd

data = pd.read_csv('processed_data_int.csv')

print(data['Churn'].value_counts())

sample_per_group = 300


grouped = data.groupby('Churn')
balanced_sample = grouped.apply(lambda x: x.sample(n=sample_per_group, random_state=42)).reset_index(drop=True)


balanced_sample.to_csv('reduced_data_int.csv', index=False)
