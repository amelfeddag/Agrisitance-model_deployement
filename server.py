from flask import Flask, jsonify, request, make_response
import traceback
import logging

from src.predictOptimizeCrops.main import predict_crops_main

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def root():
    return jsonify({"message": "Welcome to Agrissistance Crop Prediction API"})

@app.route('/predict-crops', methods=['POST'])
def predict_crops():
    try:
        data = request.get_json()
        app.logger.info(f"Received data: {data}")
        
        input_data = (
            data.get('ph'), data.get('temperature'), data.get('rainfall'),
            data.get('humidity'), data.get('nitrogen'), data.get('phosphorus'),
            data.get('potassium'), data.get('o2')
        )

        app.logger.info('Predicting crops...')
        crop_data = predict_crops_main(input_data)
        
        return jsonify(crop_data)

    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        app.logger.error(traceback.format_exc())
        return make_response(jsonify({"error": str(e)}), 500)

if __name__ == '__main__':
    app.run(debug=True)
