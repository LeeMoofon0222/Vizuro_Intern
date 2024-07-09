import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 讀取資料
file_path = 'kidney_disease.csv'
data = pd.read_csv(file_path)

# 刪除ID列
data.drop(columns=['id'], inplace=True)

# 定義正常範圍
normal_ranges = {

    'age': (0, 100),  # 年齡
    'bp': (50, 150),  # 血壓(舒張壓與收縮壓)
    'sg': (1.005, 1.030),  # 尿比重
    'bgr': (50, 500),  # 隨機血糖
    'bu': (7, 400),  # 尿素氮
    'sc': (0.4, 12),  # 血清肌酐
    'sod': (100, 160),  # 鈉
    'pot': (3, 6),  # 鉀
    'hemo': (5, 20),  # 血紅蛋白
    'pcv': (15, 60),  # 血細胞壓積
    'wc': (4000, 18000),  # 白細胞計數
    'rc': (2, 6.5)  # 紅細胞計數
}

# 將al和su不等於0的值設置為1
data['al'] = data['al'].apply(lambda x: 'Exceed' if pd.notna(x) and x != 0 else "normal")
data['su'] = data['su'].apply(lambda x: 'Exceed' if pd.notna(x) and x != 0 else "normal")

# 指定需要填補的列
categorical_cols_to_fill = ['rbc', 'pc', 'pcc', 'ba', 'appet', 'htn', 'dm', 'cad', 'pe', 'ane','al','su']
numeric_cols_to_fill = ['age', 'bp', 'sg', 'bgr', 'bu', 'sc', 'sod', 'pot', 'hemo', 'pcv', 'wc', 'rc']

# '?' 替換為 NaN
data.replace('?', np.nan, inplace=True)

# 去除多餘空格
data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# String to 0,1
# data[['htn', 'dm', 'cad', 'pe', 'ane']] = data[['htn', 'dm', 'cad', 'pe', 'ane']].replace(to_replace={'yes': 1, 'no': 0})
# data[['rbc', 'pc']] = data[['rbc', 'pc']].replace(to_replace={'abnormal': 1, 'normal': 0})
# data[['pcc', 'ba']] = data[['pcc', 'ba']].replace(to_replace={'present': 1, 'notpresent': 0})
# data[['appet']] = data[['appet']].replace(to_replace={'good': 1, 'poor': 0, 'no': np.nan})
# data['classification'] = data['classification'].replace(to_replace={'ckd': 1.0, 'ckd\t': 1.0, 'notckd': 0.0, 'no': 0.0})

# # 檢測和處理離群值(90%)
# def remove_outliers(df, column):
#     df[column] = pd.to_numeric(df[column], errors='coerce')
#     if df[column].notna().sum() > 0:  # 確保列中有非NaN值
#         lower_bound = df[column].quantile(0.05)
#         upper_bound = df[column].quantile(0.95)
#         df[column] = np.where((df[column] < lower_bound) | (df[column] > upper_bound), np.nan, df[column])
#     return df

# for col in numeric_cols_to_fill:
#     data = remove_outliers(data, col)


# Replace outliers with NaN
for feature, (low, high) in normal_ranges.items():
    if feature in data.columns:
        data[feature] = pd.to_numeric(data[feature], errors='coerce')  # Ensure the column is numeric
        data.loc[(data[feature] < low) | (data[feature] > high), feature] = np.nan


# 刪除超過3個NaN的行
data_cleaned = data.dropna(thresh=len(data.columns) - 3)

# 填補指定類別型特徵的缺失值(用眾數填補)
for col in categorical_cols_to_fill:
    data_cleaned[col].fillna(data_cleaned[col].mode()[0], inplace=True)

# 填補指定數值型特徵的缺失值(用中位數填補)
for col in numeric_cols_to_fill:
    data_cleaned[col].fillna(data_cleaned[col].median(), inplace=True)

# 導出處理後的資料
output_file_path = 'processed_kidney_disease_7.csv'
data_cleaned.to_csv(output_file_path, index=False)

print(data_cleaned.head())