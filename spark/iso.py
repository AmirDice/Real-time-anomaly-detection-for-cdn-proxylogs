# Isolation Forest and Logistic Regression
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load the data
data = pd.read_csv('./data/CDN_train.csv', delimiter=',')

# Unsupervised Isolation Forest
iso = IsolationForest(contamination = 'auto', random_state = 42)
isol = iso.fit_predict( data.iloc[:, data.columns != 'Time'] )

# Split the dataset
data = data.iloc[:, data.columns != 'Time'] 
i = round(len(data)*.8)
## 80% of the data
X_train = np.asarray(data[0:i])
y_train = np.asarray(isol[0:i])
## 20% of the data
X_valid = np.asarray(data[i+1:len(data)])
y_valid = np.asarray(isol[i+1:len(isol)])

