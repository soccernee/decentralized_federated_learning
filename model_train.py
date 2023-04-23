from sklearn.neural_network import MLPClassifier
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score


init_train = pd.read_excel('diabetes_init_train.xlsx', header=None)
test = pd.read_excel('diabetes_test.xlsx', header=None)
node_2 = pd.read_excel('diabetes_node_2.xlsx', header=None)

X = init_train.iloc[:, 0:8].to_numpy()
y = init_train.iloc[:, 8].to_numpy()

X_test = test.iloc[:, 0:8].to_numpy()
y_test = test.iloc[:, 8].to_numpy()


X_node_2 = node_2.iloc[:, 0:8].to_numpy()
y_node_2 = node_2.iloc[:, 8].to_numpy()


clf = MLPClassifier(solver='adam',activation='relu', alpha=1e-6, hidden_layer_sizes=(8, 8), random_state=1, max_iter = 1000)
clf.fit(X, y)
init_coefs = clf.coefs_

y_pred = clf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(accuracy)
# print(clf.predict([[2,	158,	90	,0,	0,	31.6,	0.805,	66]]))


clf_new = MLPClassifier(solver='adam',activation='relu', alpha=1e-6, hidden_layer_sizes=(8, 8), random_state=1, max_iter = 1000)
clf_new.coefs_ = init_coefs
clf_new.fit(X_node_2, y_node_2)

y_pred_new = clf_new.predict(X_test)
print(y_pred_new)
accuracy = accuracy_score(y_test, y_pred_new)
print(accuracy)
new_coefs = clf_new.coefs_
print(new_coefs[0])


weights_merged = [(w1 * 95.0 + w2) / 100.0 for (w1, w2) in zip(init_coefs, new_coefs)]


clf_merged = MLPClassifier(solver='adam',activation='relu', alpha=1e-6, hidden_layer_sizes=(8, 8), random_state=1, max_iter = 1000)
clf_merged.fit(X, y)
clf_merged.coefs_ = weights_merged
y_pred_merged = clf_merged.predict(X_test)
accuracy = accuracy_score(y_test, y_pred_merged)
print(accuracy)

# updated_coefs = init_coefs[0]*0.95 + new_coefs[0]*0.05
# print(updated_coefs)
# updated_coefs_arr = np.array(updated_coefs)
# print(updated_coefs_arr)
# clf_updated = MLPClassifier(solver='adam',activation='relu', alpha=1e-6, hidden_layer_sizes=(8, 8), random_state=1, max_iter = 1000)
# clf_updated.coefs_ = updated_coefs_arr
# y_pred_updated = clf_updated.predict(X_test)
# accuracy = accuracy_score(y_test, y_pred_updated)
# print(accuracy)
