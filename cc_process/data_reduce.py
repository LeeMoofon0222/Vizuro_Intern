import pandas as pd

# 讀取數據
data = pd.read_csv('processed_data_v3.csv')

# 檢查各組數據量以決定是否能平均分配
print(data['Churn'].value_counts())

# 假設您希望每個 Churn 組別各有 300 筆，總共 600 筆
# 這需要確保每組至少有 300 筆，或者按實際比例調整
sample_per_group = 300

# 分組並抽樣
grouped = data.groupby('Churn')
balanced_sample = grouped.apply(lambda x: x.sample(n=sample_per_group, random_state=42)).reset_index(drop=True)

# 保存結果
balanced_sample.to_csv('reduced_data_v3.csv', index=False)
