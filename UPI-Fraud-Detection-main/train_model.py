import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

# sample dataset (or use your dataset.csv)
data = pd.DataFrame({
    "amount": [1000, 50000, 2000, 70000, 1500, 80000],
    "time": [10, 23, 14, 2, 11, 1],
    "location": [0, 1, 0, 1, 0, 1],
    "fraud": [0, 1, 0, 1, 0, 1]
})

X = data[['amount', 'time', 'location']]
y = data['fraud']

model = LogisticRegression()
model.fit(X, y)

# save model
pickle.dump(model, open("model.pkl", "wb"))

print("Model created successfully 🚀")