import pandas as pd


file_path = 'processed_new_dataset(balance).csv'
data = pd.read_csv(file_path)


data.rename(columns={
    'Bp': 'bp',
    'Sg': 'sg',
    'Al': 'al',
    'Su': 'su',
    'Rbc': 'rbc',
    'Bu': 'bu',
    'Sc': 'sc',
    'Sod': 'sod',
    'Pot': 'pot',
    'Hemo': 'hemo',
    'Pcv': 'pcv',
    'Wbcc': 'wc',
    'Rbcc': 'rc',
    'Htn': 'htn',
    'Class': 'classification'
}, inplace=True)

data.to_csv('processed_new_dataset(balance)(rename).csv', index=False)
