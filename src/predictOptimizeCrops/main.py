import logging
from .utils.load_helpers import load_crop_financial_data
from .utils.display_results import display_optimal_allocation
from .optimization_algorithm.genetic_algorithm import run_genetic_algorithm

# Genetic Algorithm parameters (do not modify)
population_size = 200
num_generations = 800
mutation_rate = 0.2
crossover_rate = 0.8

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def optimize_crops_main(InputData): 

    (crops, total_budget, total_area) = InputData
    
    # Convert total_budget and total_area to integers because the following functions expect integers
    total_budget = int(total_budget)
    total_area = int(total_area)

    # Load crop financial data
    crop_finance_file = './src/predictOptimizeCrops/data/crop_finance.csv'
    cost_per_m2, weight_area, revenue_per_m2 = load_crop_financial_data(crop_finance_file, crops)

    # Run the genetic algorithm to optimize crop allocation
    best_solution = run_genetic_algorithm(crops, cost_per_m2, revenue_per_m2, total_area, total_budget, 
                                          population_size, num_generations, mutation_rate, crossover_rate)
    
    # Display the optimal allocation and expected returns
    OptimizationData = display_optimal_allocation(crops, best_solution, cost_per_m2, weight_area, revenue_per_m2, total_area, total_budget)

    return OptimizationData
