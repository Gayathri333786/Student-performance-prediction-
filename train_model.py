import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

data = pd.read_csv("student_data.csv")

X = data[['Attendance',
          'StudyHours',
          'Assignment',
          'InternalMarks']]

y = data['FinalMarks']

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

joblib.dump(model, "model.pkl")

print("model.pkl created successfully")
