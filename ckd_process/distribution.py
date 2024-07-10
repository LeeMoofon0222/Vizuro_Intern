import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 讀取CSV文件
data = pd.read_csv('processed_kidney_disease_2(balance).csv')  # 替換 'your_data.csv' 為您的文件路徑

# 設定圖形的風格
sns.set(style="whitegrid")

# 繪製每個特徵的分布圖並保存
for column in data.columns:
    plt.figure(figsize=(10, 4))  # 設定圖形大小
    sns.histplot(data[column], kde=True)  # kde=True 會添加一條核密度估計曲線
    plt.title(f'Distribution of {column}')  # 設定圖形標題
    plt.xlabel(column)  # 設定x軸標籤
    plt.ylabel('Frequency')  # 設定y軸標籤
    
    # 保存圖形到檔案
    plt.savefig(f'{column}_distribution.png')  # 將圖片保存為PNG格式
    plt.close()  # 關閉圖形，釋放記憶體
