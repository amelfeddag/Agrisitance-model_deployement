import logging
from .model.load_model import load_model, load_scaler
from .utils.load_helpers import load_crop_financial_data
from .utils.predictions import predict_interactive
from .utils.display_results import display_optimal_allocation
from .optimization_algorithm.genetic_algorithm import run_genetic_algorithm

# Genetic Algorithm parameters (optimized)
population_size = 100
num_generations = 400
mutation_rate = 0.1
crossover_rate = 0.8

# Load the model and scaler
model_file = './src/predictOptimizeCrops/model/crop_model_simplified.joblib'
scaler_file = './src/predictOptimizeCrops/model/crop_scaler.joblib'
logging.info(f"Loading model from {model_file}")
model = load_model(model_file)
logging.info("Model loaded successfully")

logging.info(f"Loading scaler from {scaler_file}")
scaler = load_scaler(scaler_file)
logging.info("Scaler loaded successfully")

# Load crop financial data
crop_finance_file = './src/predictOptimizeCrops/data/crop_finance.csv'
logging.info(f"Loading crop financial data from {crop_finance_file}")

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def predict_optimize_crops_main(InputData):
    logging.info("Starting prediction and optimization process")
    
    (input_ph, input_temperature, input_rainfall, input_humidity, 
        input_nitrogen, input_phosphorus, input_potassium, input_o2, 
        total_budget, total_area) = InputData

    total_budget = int(total_budget)
    total_area = int(total_area)
    
    logging.info(f"Received input data: PH={input_ph}, Temp={input_temperature}, Rainfall={input_rainfall}, "
                 f"Humidity={input_humidity}, Nitrogen={input_nitrogen}, Phosphorus={input_phosphorus}, "
                 f"Potassium={input_potassium}, O2={input_o2}, Budget={total_budget}, Area={total_area}")

    crops = predict_interactive(model, scaler, input_ph, input_temperature, input_rainfall, 
                                input_humidity, input_nitrogen, input_phosphorus, input_potassium, input_o2)
    logging.info(f"Predicted crops: {crops}")
    
    cost_per_m2, weight_area, revenue_per_m2 = load_crop_financial_data(crop_finance_file, crops)
    logging.info("Loaded crop financial data successfully")

    logging.info("Running genetic algorithm for optimization")
    best_solution = run_genetic_algorithm(crops, cost_per_m2, revenue_per_m2, total_area, total_budget, 
                                          population_size, num_generations, mutation_rate, crossover_rate)
    logging.info("Genetic algorithm completed successfully")

    OptimizationData = display_optimal_allocation(crops, best_solution, cost_per_m2, weight_area, revenue_per_m2, total_area, total_budget)
    logging.info("Optimal allocation displayed successfully")
    
    return OptimizationData
