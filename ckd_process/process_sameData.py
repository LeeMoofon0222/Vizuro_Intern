import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

file_path = 'processed_kidney_disease_6.csv'
data1 = pd.read_csv(file_path)
file_path2 = 'new_kidney_disease.csv'
data2 = pd.read_csv(file_path2)

data1.drop(columns=['age'], inplace=True)
data1.drop(columns=['pc'], inplace=True)
data1.drop(columns=['pcc'], inplace=True)
data1.drop(columns=['ba'], inplace=True)
data1.drop(columns=['bgr'], inplace=True)
data1.drop(columns=['dm'], inplace=True)
data1.drop(columns=['cad'], inplace=True)
data1.drop(columns=['appet'], inplace=True)
data1.drop(columns=['pe'], inplace=True)
data1.drop(columns=['ane'], inplace=True)

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

data2.rename(columns={
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


# 預處理 data2（已在您的代碼中完成重命名）
# 確保 data2 中的列與 data1 一致

# 數據集分割
X_train = data1.drop(columns=['classification'])
y_train = data1['classification']
X_test = data2.drop(columns=['classification'])
y_test = data2['classification']

# 隨機森林模型訓練
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# 進行預測
predictions = rf.predict(X_test)

# 計算準確度
accuracy = accuracy_score(y_test, predictions)
print("Accuracy:", accuracy)

