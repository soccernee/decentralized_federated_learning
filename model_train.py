import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

class MachineLearning():
    def __init__(self):
        all_data = pd.read_csv('diabetes.csv', header=0)

        self.X = all_data.iloc[:, 0:8].to_numpy()
        self.X_dict = {}
        self.y_dict = {}
        print("len X = ", len(self.X))

        self.y = all_data.iloc[:, 8].to_numpy()

        self.num_nodes = 5

        self.main()

    def set_num_nodes(self, num):
        self.num_nodes = num

    def baseline_reading(self):
        nn_total_accuracy = 0
        lr_total_accuracy = 0
        dt_total_accuracy = 0
        rf_total_accuracy = 0
        kn_total_accuracy = 0
        count = 0

        for i in range(0, 20):
            # Set aside the testing set
            (X_train, X_test, y_train, y_test) = train_test_split(self.X, self.y, test_size = .3)
            
            # print("X train: ", X_train)
            # print("y train: ", y_train)
            # print("X test: ", X_test)
            # print("y test: ", y_test)

            # establish a baseline accuracy
            nn_clf = MLPClassifier(solver='adam',activation='relu', alpha=1e-6, hidden_layer_sizes=(8, 8), max_iter = 1000)
            nn_clf.fit(X_train, y_train)
            y_pred_nn = nn_clf.predict(X_test)
            nn_accuracy = accuracy_score(y_test, y_pred_nn)
            nn_total_accuracy += nn_accuracy
            count += 1

            lr_clf = LogisticRegression(max_iter = 1000).fit(X_train, y_train)
            y_pred_lr = lr_clf.predict(X_test)
            lr_accuracy = accuracy_score(y_test, y_pred_lr)
            lr_total_accuracy += lr_accuracy

            dt_clf = DecisionTreeClassifier(max_depth=5).fit(X_train, y_train)
            y_pred_dt = dt_clf.predict(X_test)
            dt_accuracy = accuracy_score(y_test, y_pred_dt)
            dt_total_accuracy += dt_accuracy
            
            rf_clf = RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1).fit(X_train, y_train)
            y_pred_rf = rf_clf.predict(X_test)
            rf_accuracy = accuracy_score(y_test, y_pred_rf)
            rf_total_accuracy += rf_accuracy
            
            kn_clf = KNeighborsClassifier(3).fit(X_train, y_train)
            y_pred_kn = kn_clf.predict(X_test)
            kn_accuracy = accuracy_score(y_test, y_pred_kn)
            kn_total_accuracy += kn_accuracy

        print("nn avg. accuracy = ", (nn_total_accuracy / count))
        print("lr avg. accuracy = ", (lr_total_accuracy / count))
        print("dt avg. accuracy = ", (dt_total_accuracy / count))
        print("rf avg. accuracy = ", (rf_total_accuracy / count))
        print("kn avg. accuracy = ", (kn_total_accuracy / count))

    def split_data(self):
        # Set aside the testing set
        (X_train, X_test, y_train, y_test) = train_test_split(self.X, self.y, test_size = .3, random_state= 2)

        print("len X = ", len(X_train))
        self.X_dict[1] = X_train[0:80]
        self.X_dict[2] = X_train[81:160]
        self.X_dict[3] = X_train[161:240]
        self.X_dict[4] = X_train[241:320]
        self.X_dict[5] = X_train[321:400]
        self.X_leader = X_train[401:]

        self.y_dict[1] = y_train[0:80]
        self.y_dict[2] = y_train[81:160]
        self.y_dict[3] = y_train[161:240]
        self.y_dict[4] = y_train[241:320]
        self.y_dict[5] = y_train[321:400]
        self.y_leader = y_train[401:]

    def get_data_for_node(self, node_num):
        return self.X_dict[node_num], self.y_dict[node_num]
    
    def leader_train(self):
        lr_clf = LogisticRegression(max_iter = 1000).fit(self.X_leader, self.y_leader)
        return lr_clf.coef_
    
    def train_for_node(self, node_num):
        x, y = self.get_data_for_node(node_num)
        lr_clf = LogisticRegression(max_iter = 1000).fit(x, y)
        return lr_clf.coef_

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