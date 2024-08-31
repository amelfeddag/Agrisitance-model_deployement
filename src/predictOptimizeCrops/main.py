import logging
from .model.load_model import load_model, load_scaler
from .utils.predictions import predict_interactive

# Load the model and scaler
model_file = './src/predictOptimizeCrops/model/crop_model_simplified.joblib'
scaler_file = './src/predictOptimizeCrops/model/crop_scaler.joblib'
model = load_model(model_file)
scaler = load_scaler(scaler_file)

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def predict_crops_main(InputData): 
    (input_ph, input_temperature, input_rainfall, input_humidity, 
        input_nitrogen, input_phosphorus, input_potassium, input_o2) = InputData

    # Predict top 10 crops based on input data
    crops = predict_interactive(model, scaler, input_ph, input_temperature, input_rainfall, 
                                input_humidity, input_nitrogen, input_phosphorus, input_potassium, input_o2)
        
    return {"predicted_crops": crops}
