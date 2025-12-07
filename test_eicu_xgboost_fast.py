from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import torch
from pathlib import Path
import numpy as np
from numpy import nan
from pyhealth.datasets import SampleDataset, get_dataloader
from pyhealth.datasets import split_by_patient, get_dataloader
from pyhealth.models import LogisticRegression
from pyhealth.datasets import eICUDataset
from pyhealth.models.medlink import model
from pyhealth.tasks.mortality_prediction import MortalityPredictionEICU
import xgboost as xgb
from sklearn.metrics import roc_auc_score
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix, classification_report
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV

class TesteicuXGBoost:
    """Test cases for the XGBoost model on eICU dataset."""

    def setUp(self):

        #self.dfX = pd.read_csv('/Users/rosssponholtz/data/eicu-dsmall_0/eicu_mortality_prediction_samples.csv')
        #self.dfy = pd.read_csv('/Users/rosssponholtz/data/eicu-dsmall_0/eicu_mortality_prediction_labels.csv')
        self.dfX = pd.read_csv('/Users/rosssponholtz/data/eicu-combined/combined_samples.csv')
        self.dfy = pd.read_csv('/Users/rosssponholtz/data/eicu-combined/combined_labels.csv')

        self.dfX.drop(['mortality0'], axis=1, inplace=True)
        self.dfy["mortality"] = self.dfy["mortality"].astype(int)

    def hyperparameter_tuning(self):
        # Define the parameter grid for RandomizedSearchCV
        param_grid = {
            'n_estimators': [ 300],
            'max_depth': [  14],
            'learning_rate': [0.01],
            'subsample': [ 0.8, 0.9],
            'colsample_bytree': [0.4],
            'reg_alpha': [0.15],
            'reg_lambda': [ 0.15],
            'objective': ['binary:logistic']
        }

        xgb = XGBClassifier( eval_metric='auc')
        random_search = RandomizedSearchCV(estimator=xgb, param_distributions=param_grid, n_iter=50, cv=3, scoring='roc_auc', verbose=1, random_state=42, n_jobs=-1)
        random_search.fit(self.dfX, self.dfy)

        print("Best parameters found: ", random_search.best_params_)
        print("Best accuracy found: ", random_search.best_score_)



    def test_model_forward(self):
        """Test that the LogisticRegression model forward pass works correctly."""
        X_train, X_test, y_train, y_test = train_test_split(self.dfX, self.dfy, test_size=.2)

        #self.model = XGBClassifier(n_estimators=250, max_depth=9, learning_rate=0.01, subsample=0.6, colsample_bytree=0.4, reg_alpha=0.1, reg_lambda=0.1, objective='binary:logistic')      
        #self.model = XGBClassifier(n_estimators=300, max_depth=14, learning_rate=0.01, subsample=0.8, colsample_bytree=0.4, reg_alpha=0.15, reg_lambda=0.15, objective='binary:logistic')      
        self.model = XGBClassifier()      
        self.model.fit(X_train, y_train)
        # make predictions
        preds = self.model.predict(X_test)
        # evaluate predictions
        self.model.score(X_test,y_test)

        print(f"Model: {self.model}")
        print(f"Score: {self.model.score(X_test, y_test)}")
        print(f"Predictions: {self.model.predict(X_test)}")
        #print(f"Feature Importances: {self.model.feature_importances_}")
        #print(f"Selected Features: {self.model.selected_features}")
        print(f"Model: {self.model}")
        #print(f"Model: {self.model.steps}")
        print(f"Model: {self.model.get_params()}")
        print(f"Classification Report:\n{classification_report(y_test, preds)}")
        print(f"Confusion Matrix:\n{confusion_matrix(y_test, preds)}")
        print(f"ROC AUC Score: {roc_auc_score(y_test, preds)}")


def main():
    test = TesteicuXGBoost()
    test.setUp()
    #test.hyperparameter_tuning()
    test.test_model_forward()

if __name__ == "__main__":
    main()
