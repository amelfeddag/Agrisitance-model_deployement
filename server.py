import logging
from flask import Flask, jsonify, request, make_response
from asgiref.wsgi import WsgiToAsgi
import requests
import time
import json
import os

from src.predictOptimizeCrops.main import predict_optimize_crops_main
from src.generateBusinessPlan.main import generate_business_plan_main
from src.chatBot.chat_service import ChatRequest

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
async def root():
    logger.info("Root endpoint called")
    return jsonify({"message": "Welcome to Agrissistance Models API"})

@app.route('/generate-business-plan', methods=['POST'])
async def generate_business_plan():
    start_time = time.time()
    logger.info("Generate Business Plan endpoint called")

    try:
        data = request.get_json()
        logger.info(f"Received data: {data}")

        # Map the incoming data to the expected order of inputs
        model_inputs = (
            data.get('ph'),
            data.get('temperature'),
            data.get('rainfall'),
            data.get('humidity'),
            data.get('nitrogen'),
            data.get('phosphorus'),
            data.get('potassium'),
            data.get('o2'),
            data.get('total_budget'),
            data.get('total_area')
        )

        # Log model inputs to ensure they are correct
        logger.info(f"Model inputs: {model_inputs}")

        # Call the crop prediction function with the correct inputs
        cropData = predict_optimize_crops_main(model_inputs)
        if isinstance(cropData, str):
            cropData = json.loads(cropData)

        businessPlan = generate_business_plan_main(model_inputs, cropData)
        if isinstance(businessPlan, str):
            businessPlan = json.loads(businessPlan)

        logger.info(f"Generated business plan: {businessPlan}")
        logger.info(f"Generated crop data: {cropData}")

        return jsonify({
            "cropData": cropData,
            "businessPlan": businessPlan
        })

    except Exception as e:
        logger.error(f"Error generating business plan: {e}", exc_info=True)
        return make_response(jsonify({"detail": str(e)}), 500)

    finally:
        execution_time = time.time() - start_time  
        logger.info(f"Execution time: {execution_time:.2f} seconds")



@app.route("/chat", methods=['POST'])
async def chat():
    logger.info("Chat endpoint called")
    try:
        headers = {
            'Content-Type': 'application/json',
            'api_token': os.getenv('API_TOKEN')
        }
        payload = request.get_json()
        logger.info(f"Received chat request: {payload}")
        response = requests.post(
            os.getenv('API_URL'),
            json=payload,
            headers=headers
        )
        logger.info(f"Chat response: {response.json()}")
        return jsonify(response.json())
    
    except Exception as e:
        logger.error(f"Error during chat processing: {e}", exc_info=True)
        return make_response(jsonify({"detail": str(e)}), 500)
    

asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run()
