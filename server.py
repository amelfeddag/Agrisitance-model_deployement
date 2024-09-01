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


def parse_api_response(response):
    """
    Parses the API response and returns it as a dictionary.

    Parameters:
    - response: The raw response from the API, which could be in various formats.

    Returns:
    - A dictionary containing the parsed response.
    """
    try:
        if isinstance(response, str):
            # Attempt to parse as JSON
            try:
                parsed_response = json.loads(response)
            except json.JSONDecodeError as e:
                logging.error(f"Failed to decode JSON from string: {e}")
                raise ValueError("The API response is a string but not valid JSON.")
        elif isinstance(response, dict):
            # If it's already a dictionary, return as-is
            parsed_response = response
        else:
            # Handle unexpected types
            raise TypeError(f"Unexpected response type: {type(response)}")

        return parsed_response

    except Exception as e:
        logging.error(f"Error parsing API response: {e}")
        raise e


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
        logger.info(f"Crop data returned: {cropData}")

        if isinstance(cropData, str):
            logger.info("Converting cropData from string to JSON")
            cropData = json.loads(cropData)

        # Call the business plan generation function
        businessPlan = generate_business_plan_main(model_inputs, cropData)
        logger.info(f"Business plan returned: {businessPlan}")

        if isinstance(businessPlan, str):
            logger.info("Converting businessPlan from string to JSON")
            businessPlan = json.loads(businessPlan)

        logger.info(f"Final business plan: {businessPlan}")
        logger.info(f"Final crop data: {cropData}")

        return jsonify({
            "cropData": cropData,
            "businessPlan": businessPlan
        })

    except json.JSONDecodeError as json_err:
        logger.error(f"JSON decoding error: {json_err}", exc_info=True)
        return make_response(jsonify({"detail": "Invalid JSON format returned"}), 500)
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
