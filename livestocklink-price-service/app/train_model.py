import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor


df = pd.read_csv("app/data/maharashtra_livestock_economic_weekly.csv")

print("Dataset loaded:", df.shape)


df["date"] = pd.to_datetime(df["date"])
df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)
df["year"] = df["date"].dt.year


district_encoder = LabelEncoder()
animal_encoder = LabelEncoder()

df["district_encoded"] = district_encoder.fit_transform(df["district"])
df["animal_encoded"] = animal_encoder.fit_transform(df["animal_type"])


FEATURES = [
    "district_encoded",
    "animal_encoded",
    "week_of_year",
    "year",
    "feed_cost_index",
    "water_availability_index",
    "disease_risk_index",
    "climate_risk_index",
    "festival_flag",
    "export_demand_index"
]

TARGET = "price"

X = df[FEATURES]
y = df[TARGET]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


model = XGBRegressor(
    n_estimators=500,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

print("Training model...")
model.fit(X_train, y_train)


preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)

print("Model trained successfully.")
print("Mean Absolute Error:", round(mae, 2))


joblib.dump(model, "app/model/model.pkl")
joblib.dump(district_encoder, "app/model/district_encoder.pkl")
joblib.dump(animal_encoder, "app/model/animal_encoder.pkl")
joblib.dump(FEATURES, "app/model/features.pkl")

print("Model and encoders saved successfully.")