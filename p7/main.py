# project: p7
# submitter: txiong53
# partner: none
# hours: 5

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import cross_val_score



class UserPredictor():
    def __init__(self):
        self.pipe = None
        self.xcol = None
        
        # concatenate the browsing time to the dataset
    def concatFeature(self, users, log):
        self.xcol = ["user_id", "past_purchase_amt","age","seconds"]
        time = log.groupby("user_id").sum()
        users["index"] = users["user_id"]
        new = pd.concat([users.set_index("index") ,time["seconds"]], axis=1).fillna(0)
        return new
    
    
    def fit(self, train_users, train_logs, train_y):
        # add new feature
        new = self.concatFeature(train_users,train_logs)
        # model
        self.pipe = pipe = Pipeline([
            ("poly", PolynomialFeatures(degree=2)),
            ("std", StandardScaler()),
            ("lr", LogisticRegression(max_iter=100))
        ])
        # fit the model
        self.pipe.fit(new[self.xcol],train_y['y'])
        # cross val debug
        scores = cross_val_score(self.pipe, new[self.xcol], train_y["y"])
        print(f"AVG: {scores.mean()}, STD: {scores.std()}\n")
            
    def score(self,test_users,test_logs,test_y):
        new = self.concatFeature(test_users,test_logs)   
        return self.pipe.score(new[self.xcol],test_y['y'])

    def predict(self, test_users, test_logs):
        new = self.concatFeature(test_users,test_logs)
        return self.pipe.predict(new[self.xcol])
    