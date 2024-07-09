import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


file_path = 'kidney_disease.csv'
data = pd.read_csv(file_path)


data.drop(columns=['id'], inplace=True)

# '?' 替換為 NaN
data.replace('?', np.nan, inplace=True)

# 填補數值型特徵的缺失值(找到中位數填補缺失值)
numeric_features = data.select_dtypes(include=[np.number]).columns.tolist()
for col in numeric_features:
    data[col].fillna(data[col].median(), inplace=True)

# 填補類別型特徵的缺失值(找到眾數填補缺失值)
categorical_features = data.select_dtypes(include=[object]).columns.tolist()
for col in categorical_features:
    data[col].fillna(data[col].mode()[0], inplace=True)

# 檢測和處理離群值(四分位法)(將離群值替換為上下界)
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df[column] = np.where(df[column] < lower_bound, lower_bound, df[column])
    df[column] = np.where(df[column] > upper_bound, upper_bound, df[column])

# for col in numeric_features:
#     remove_outliers(data, col)

# 去除多餘空格
data = data.applymap(lambda x: x.strip() if type(x) == str else x)

# String to 0,1
data[['htn', 'dm', 'cad', 'pe', 'ane']] = data[['htn', 'dm', 'cad', 'pe', 'ane']].replace(to_replace={'yes': 1, 'no': 0})
data[['rbc', 'pc']] = data[['rbc', 'pc']].replace(to_replace={'abnormal': 1, 'normal': 0})
data[['pcc', 'ba']] = data[['pcc', 'ba']].replace(to_replace={'present': 1, 'notpresent': 0})
data[['appet']] = data[['appet']].replace(to_replace={'good': 1, 'poor': 0, 'no': np.nan})
data['classification'] = data['classification'].replace(to_replace={'ckd': 1.0, 'ckd\t': 1.0, 'notckd': 0.0, 'no': 0.0})


output_file_path = 'processed_kidney_disease_1.csv'
data.to_csv(output_file_path, index=False)

print(data.head())


#------Drop outline rows-----

# import pandas as pd
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt

# # 讀取上傳的數據集
# file_path = 'kidney_disease.csv'
# data = pd.read_csv(file_path)

# # 刪除第一列 'id'
# data.drop(columns=['id'], inplace=True)

# # 將數值型特徵中的 '?' 替換為 NaN
# data.replace('?', np.nan, inplace=True)

# # 填補數值型特徵的缺失值(找到中位數填補缺失值)
# numeric_features = data.select_dtypes(include=[np.number]).columns.tolist()
# for col in numeric_features:
#     data[col].fillna(data[col].median(), inplace=True)

# # 填補類別型特徵的缺失值(找到眾數填補缺失值)
# categorical_features = data.select_dtypes(include=[object]).columns.tolist()
# for col in categorical_features:
#     data[col].fillna(data[col].mode()[0], inplace=True)

# # 檢測並刪除離群值(四分位法)
# def remove_outliers(df, column):
#     Q1 = df[column].quantile(0.25)
#     Q3 = df[column].quantile(0.75)
#     IQR = Q3 - Q1
#     lower_bound = Q1 - 1.5 * IQR
#     upper_bound = Q3 + 1.5 * IQR
#     return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# for col in numeric_features:
#     data = remove_outliers(data, col)

# # 去除多餘空格
# data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# # 將特定列的值進行替換
# data[['htn', 'dm', 'cad', 'pe', 'ane']] = data[['htn', 'dm', 'cad', 'pe', 'ane']].replace(to_replace={'yes': 1, 'no': 0})
# data[['rbc', 'pc']] = data[['rbc', 'pc']].replace(to_replace={'abnormal': 1, 'normal': 0})
# data[['pcc', 'ba']] = data[['pcc', 'ba']].replace(to_replace={'present': 1, 'notpresent': 0})
# data[['appet']] = data[['appet']].replace(to_replace={'good': 1, 'poor': 0, 'no': np.nan})
# data['classification'] = data['classification'].replace(to_replace={'ckd': 1.0, 'ckd\t': 1.0, 'notckd': 0.0, 'no': 0.0})

# # 將處理後的數據集導出成csv文件
# output_file_path = 'processed_kidney_disease_3.csv'
# data.to_csv(output_file_path, index=False)

# print(data.head())


#-------Drop nan lines-------

# import pandas as pd
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt

# # 讀取上傳的數據集
# file_path = 'kidney_disease.csv'
# data = pd.read_csv(file_path)

# # 刪除第一列 'id'
# data.drop(columns=['id'], inplace=True)

# # 將數值型特徵中的 '?' 替換為 NaN
# data.replace('?', np.nan, inplace=True)

# # 去除多餘空格
# data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# # 將特定列的值進行替換
# data[['htn', 'dm', 'cad', 'pe', 'ane']] = data[['htn', 'dm', 'cad', 'pe', 'ane']].replace(to_replace={'yes': 1, 'no': 0})
# data[['rbc', 'pc']] = data[['rbc', 'pc']].replace(to_replace={'abnormal': 1, 'normal': 0})
# data[['pcc', 'ba']] = data[['pcc', 'ba']].replace(to_replace={'present': 1, 'notpresent': 0})
# data[['appet']] = data[['appet']].replace(to_replace={'good': 1, 'poor': 0, 'no': np.nan})
# data['classification'] = data['classification'].replace(to_replace={'ckd': 1.0, 'ckd\t': 1.0, 'notckd': 0.0, 'no': 0.0})

# # 刪除包含 NaN 的行
# data.dropna(inplace=True)


# # 將處理後的數據集導出成csv文件
# output_file_path = 'processed_kidney_disease_2.csv'
# data.to_csv(output_file_path, index=False)

# print(data.head())