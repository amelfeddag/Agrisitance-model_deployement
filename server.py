from flask import Flask, jsonify, request, make_response
from asgiref.wsgi import WsgiToAsgi
import time
import json

from src.predictOptimizeCrops.main import predict_optimize_crops_main

app = Flask(__name__)

@app.route('/')
async def root():
    return jsonify({"message": "Welcome to Agrissistance Crop Prediction and Optimization API"})

@app.route('/predict-optimize-crops', methods=['POST'])
async def predict_optimize_crops():
    start_time = time.time()

    try:
        data = request.get_json()
        input_data = (
            data.get('ph'), data.get('temperature'), data.get('rainfall'),
            data.get('humidity'), data.get('nitrogen'), data.get('phosphorus'),
            data.get('potassium'), data.get('o2'), data.get('total_budget'),
            data.get('total_area')
        )

        print('Predicting and optimizing crops...')
        crop_data = predict_optimize_crops_main(input_data)
        if isinstance(crop_data, str):
            crop_data = json.loads(crop_data)

        return jsonify(crop_data)

    except Exception as e:
        print(e)
        return make_response(jsonify({"detail": str(e)}), 500)

    finally:
        execution_time = time.time() - start_time  
        print(f"Execution time: {execution_time:.2f} seconds")

asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)