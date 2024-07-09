import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, roc_curve, auc, classification_report, f1_score
import matplotlib.pyplot as plt
import seaborn as sns

# Load the training data
data_path = 'processed_kidney_disease_3(balance)(drop).csv'
data = pd.read_csv(data_path)

# Prepare the training data
X_train = data.drop('classification', axis=1)
y_train = data['classification']

# Load the testing data
test_data_path = 'processed_new_dataset(balance)(rename).csv'
test_data = pd.read_csv(test_data_path)

# Prepare the testing data
X_test = test_data.drop('classification', axis=1)
y_test = test_data['classification']

# Initialize and train the Random Forest classifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate the confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
# Calculate F1 score
f1 = f1_score(y_test, y_pred)

# Calculate ROC curve and AUC
fpr, tpr, thresholds = roc_curve(y_test, model.predict_proba(X_test)[:, 1])
roc_auc = auc(fpr, tpr)

# Display the confusion matrix and AUC
print("Confusion Matrix:")
print(conf_matrix)
print(f"ROC AUC: {roc_auc:.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Plot ROC curve
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
# Display F1 score and accuracy on the plot
plt.text(0.02, 0.97, f'F1 Score: {f1:.2f}\nAccuracy: {accuracy:.2f}', fontsize=12, verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', alpha=0.5))
plt.legend(loc="lower right")
plt.show()

# Visualize the confusion matrix
plt.figure(figsize=(6, 4))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues")
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Confusion Matrix')
plt.show()
