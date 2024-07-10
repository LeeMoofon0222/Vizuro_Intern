import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, roc_curve, auc, f1_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# 讀取預測結果和測試數據
predicted_data = pd.read_csv('integer_data.csv')
actual_data = pd.read_csv('test_data.csv')

# 確保數據行數一致
predicted_data = predicted_data.head(actual_data.shape[0])

# 假設 'classification' 是標籤列名
y_pred = predicted_data['classification']
y_true = actual_data['classification']

# 計算準確率
accuracy = accuracy_score(y_true, y_pred)

# 計算F1分數
f1 = f1_score(y_true, y_pred)

# 計算混淆矩陣
conf_matrix = confusion_matrix(y_true, y_pred)

# 計算ROC曲線和AUC
fpr, tpr, thresholds = roc_curve(y_true, y_pred, pos_label=1)
roc_auc = auc(fpr, tpr)

# 繪製ROC曲線
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.text(0.02, 0.97, f'F1 Score: {f1:.2f}\nAccuracy: {accuracy:.2f}', fontsize=12, verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', alpha=0.5))
plt.legend(loc="lower right")
plt.show()

# 可視化混淆矩陣
plt.figure(figsize=(6, 4))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues")
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Confusion Matrix')
plt.show()
