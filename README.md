# Credit_Scoring
This work is dedicated to prediction of client credit scorings. The main goal is to estimate the solvency of clients and make a desicion about granting a loan to them or not.

Link for the dataset which was used for creating model:
https://raw.githubusercontent.com/evgpat/stepik_from_idea_to_mvp/main/datasets/credit_scoring.csv

The main problem of creating the model for credit scoring is disbalanced classes. In this case the oversampling was used to prepare the data for learning.

In this work a number of algorythms were tested to find the best one(logistic regression, SGD, Random Forest, XGBoost and CatBoost). The Random Forest Classifier was the best one among all. By means of Optuna the best hyperparameters were achived.

The web app was created with using the best model with the best hyperparameters.

Link for the final App:
https://creditscoring.streamlit.app/
