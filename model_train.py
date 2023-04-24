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

        self.main()

    # A function to help determine what our baseline accuracy is (without any
    # distributed system and all of the data on a single machine) as well as 
    # what ML model performs best

    def print_model_accuracy(self, model):
        model_weights, num_data_points = model.get_model()
        print("model_weights = ", model_weights)
        print("num_data_points = ", num_data_points)

        # get the data from the model
        (X_train, X_test, y_train, y_test) = train_test_split(self.X, self.y, test_size = .3)

        lr_clf = LogisticRegression(max_iter = 1000).fit(X_train, y_train)
        lr_clf.coef_ = model_weights
        y_pred_lr = lr_clf.predict(X_test)
        lr_accuracy = accuracy_score(y_test, y_pred_lr)

        print("lr_accuracy = ", lr_accuracy)



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
        
        #
        # Turns out the Logistic Regression model consistently performed the best,
        # so we we will be using that model for our federated learning network.
        #

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
    
    def leader_train(self, node_model):
        lr_clf = LogisticRegression(max_iter = 1000).fit(self.X_leader, self.y_leader)
        node_model.update_model(list(lr_clf.coef_[0]), len(self.X_leader))
        print("~~ all done training leader ~~")
        return node_model
    
    def train_for_node(self, node_model):
        lr_clf = LogisticRegression(max_iter = 1000)
        lr_clf.coef_ = node_model.model_weights

        orig_size = node_model.num_model_data_points
        new_size = len(node_model.x_data)
        orig_percentage = orig_size / (orig_size + new_size)
        new_percentage = new_size / (orig_size + new_size)

        lr_clf.fit(node_model.x_data, node_model.y_data)

        new_weights = list(lr_clf.coef_[0])
        weights_merged = [(w1 * orig_percentage + w2 * new_percentage) for (w1, w2) in zip(node_model.model_weights, new_weights)]
        node_model.update_model(weights_merged, node_model.num_model_data_points + len(node_model.x_data))
        return node_model

    def main(self):
        # self.baseline_reading()

        self.split_data()

train = MachineLearning()