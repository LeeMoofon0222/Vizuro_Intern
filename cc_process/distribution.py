import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


data = pd.read_csv('reduced_data_v2.csv')

sns.set(style="whitegrid")


for column in data.columns:
    plt.figure(figsize=(10, 5))
    sns.histplot(data[column], kde=True)
    plt.title(f'Distribution of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.savefig(f'{column}_distribution.png')
    plt.close()
