import pandas as pd
from sklearn.model_selection import train_test_split

data_path = 'reduced_data_int.csv'
data = pd.read_csv(data_path)

# 直接分割原始數據，不刪除任何列
train_data, test_data = train_test_split(data, test_size=0.3, random_state=42)

# 將訓練數據和測試數據保存到CSV檔案，包括所有列
train_data.to_csv('train_data.csv', index=False)
test_data.to_csv('test_data.csv', index=False)
