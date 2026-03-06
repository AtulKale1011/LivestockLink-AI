import joblib

model = joblib.load("model/model.pkl")
district_encoder = joblib.load("model/district_encoder.pkl")
animal_encoder = joblib.load("model/animal_encoder.pkl")
FEATURES = joblib.load("model/features.pkl")

def get_model():
    return model

def get_encoders():
    return district_encoder, animal_encoder

def get_features():
    return FEATURES