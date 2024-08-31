from flask import Flask, jsonify, request, make_response
import traceback
import logging

from src.predictOptimizeCrops.main import optimize_crops_main

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def root():
    return jsonify({"message": "Welcome to Agrissistance Crop Optimization API"})

@app.route('/optimize-crops', methods=['POST'])
def optimize_crops():
    try:
        data = request.get_json()
        app.logger.info(f"Received data: {data}")
        
        input_data = (
            data.get('crops'), data.get('total_budget'), data.get('total_area')
        )

        app.logger.info('Optimizing crops...')
        optimization_data = optimize_crops_main(input_data)
        
        return jsonify(optimization_data)

    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        app.logger.error(traceback.format_exc())
        return make_response(jsonify({"error": str(e)}), 500)

if __name__ == '__main__':
    app.run(debug=True)
