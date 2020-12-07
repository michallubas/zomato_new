import pickle
import pandas as pd
import numpy as np
import sklearn
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import train_test_split

import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('Zomato_df.csv')

df.drop('Unnamed: 0', axis=1, inplace=True)
# print(df.head())

x = df.drop('rate', axis=1)
y = df['rate']

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=10)


class Hello():
    def test(self):
        return 'helloooooooo'

    def suma(self, list):
        return sum(list)


nic = Hello()

# Preparing data Tree
ET_Model = ExtraTreesRegressor(n_estimators=120)
ET_Model.fit(X_train, y_train)

predictions = ET_Model.predict(X_test)

# saving model to disk
pickle.dump(nic, open('model.pkl', 'wb'))
# pickle.dump(ET_Model, open('model.pkl', 'wb'))


# print(predictions)
