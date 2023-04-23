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
new_coefsArr = np.asarray(new_coefs)
print(new_coefsArr)
updated_coefs = init_coefs*0.95 + new_coefsArr*0.05

clf_updated = MLPClassifier(solver='adam',activation='relu', alpha=1e-6, hidden_layer_sizes=(8, 8), random_state=1, max_iter = 1000)
clf_updated.coefs_ = updated_coefs
y_pred_updated = clf_updated.predict(X_test)
accuracy = accuracy_score(y_test, y_pred_updated)
print(accuracy)
