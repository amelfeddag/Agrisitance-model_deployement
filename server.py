from flask import Flask, jsonify, request, make_response
from asgiref.wsgi import WsgiToAsgi
import requests
import time
import json
import os

from src.predictOptimizeCrops.main import predict_optimize_crops_main
from src.generateBusinessPlan.main import generate_business_plan_main
from src.chatBot.chat_service import ChatRequest

app = Flask(__name__)

@app.route('/')
async def root():
    return jsonify({"message": "Welcome to Agrissistance Models API"})

@app.route('/generate-business-plan', methods=['POST'])
async def generate_business_plan():
    start_time = time.time()
    
    try:
        data = request.get_json()
        model_inputs = data.get('model_inputs')
        
        # Pass the model inputs to the crop prediction function
        cropData = predict_optimize_crops_main(model_inputs)
        if isinstance(cropData, str):
            cropData = json.loads(cropData)

        businessPlan = generate_business_plan_main(model_inputs, cropData)
        if isinstance(businessPlan, str):
            businessPlan = json.loads(businessPlan)

        print("Business Plan: ", businessPlan)
        print("Crop Data: ", cropData)

        return jsonify({
            "cropData": cropData,
            "businessPlan": businessPlan
        })
    
    except Exception as e:
        print(e)
        return make_response(jsonify({"detail": str(e)}), 500)
    
    finally:
        execution_time = time.time() - start_time  
        print(f"Execution time: {execution_time:.2f} seconds")


@app.route("/chat", methods=['POST'])
async def chat():
    try:
        headers = {
            'Content-Type': 'application/json',
            'api_token': os.getenv('API_TOKEN')
        }
        payload = request.get_json()
        response = requests.post(
            os.getenv('API_URL'),
            json=payload,
            headers=headers
        )
        return jsonify(response.json())
    
    except Exception as e:
        return make_response(jsonify({"detail": str(e)}), 500)
    

asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    app.run()
