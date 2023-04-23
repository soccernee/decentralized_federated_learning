import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class MachineLearning():
    def __init__(self):
        all_data = pd.read_excel('diabetes.xlsx', header=None)

        self.X = all_data.iloc[:, 0:8].to_numpy()
        print("len X = ", len(self.X))
        print("X = ", self.X[0:12])

        self.y = all_data.iloc[:, 8].to_numpy()

        self.num_nodes = 5

        self.main()

    def set_num_nodes(self, num):
        self.num_nodes = num

    def baseline_reading(self):
        total_accuracy = 0
        count = 0

        for i in range(0, 10):
            # Set aside the testing set
            (X_train, X_test, y_train, y_test) = train_test_split(self.X, self.y, test_size = .3)
            
            # print("X train: ", X_train)
            # print("y train: ", y_train)
            # print("X test: ", X_test)
            # print("y test: ", y_test)

            # establish a baseline accuracy
            clf = MLPClassifier(solver='adam',activation='relu', alpha=1e-6, hidden_layer_sizes=(8, 8), max_iter = 1000)
            clf.fit(X_train, y_train)
            y_pred = clf.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            total_accuracy += accuracy
            count += 1
    
        print("total_accuracy = ", total_accuracy)
        print("count = ", count)

        print("avg. accuracy = ", (total_accuracy / count))

    def split_data(self):
        # Set aside the testing set
        (X_train, X_test, y_train, y_test) = train_test_split(self.X, self.y, test_size = .3)

        # split by number of nodes
        X_split = []
        Y_split = []
        for i in range(self.num_nodes):
            start = 80 * i
            end = 80 *(i+1)
            print("start: ", start)
            print("end: ", end)

            X_split[i] = self.X[start:end]
            Y_split[i] = self.y[start:end]
            print(X_split)
            print(Y_split)

    # initial code, function not be run
    def parking_lot(self):
        node_2 = pd.read_excel('diabetes_node_2.xlsx', header=None)
        X_node_2 = node_2.iloc[:, 0:8].to_numpy()
        y_node_2 = node_2.iloc[:, 8].to_numpy()

        clf = MLPClassifier(solver='adam',activation='relu', alpha=1e-6, hidden_layer_sizes=(8, 8), random_state=1, max_iter = 1000)
        clf.fit(X, y)
        init_coefs = clf.coefs_

        y_pred = clf.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        print("accuracy: ", accuracy)
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
        print("y_pred_merged: ", y_pred_merged)
        accuracy = accuracy_score(y_test, y_pred_merged)
        print(accuracy)


    def main(self):
        self.baseline_reading()

        self.split_data()



train = MachineLearning()


# updated_coefs = init_coefs[0]*0.95 + new_coefs[0]*0.05
# print(updated_coefs)
# updated_coefs_arr = np.array(updated_coefs)
# print(updated_coefs_arr)
# clf_updated = MLPClassifier(solver='adam',activation='relu', alpha=1e-6, hidden_layer_sizes=(8, 8), random_state=1, max_iter = 1000)
# clf_updated.coefs_ = updated_coefs_arr
# y_pred_updated = clf_updated.predict(X_test)
# accuracy = accuracy_score(y_test, y_pred_updated)
# print(accuracy)

# 80 rows per node
# 250 to test
# 118 for the leader