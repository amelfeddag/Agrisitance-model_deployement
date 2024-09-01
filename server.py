import json
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

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
def generate_business_plan():
    try:
        # Get the raw response from the API or request body
        raw_response = request.get_json()

        # Parse the raw response
        parsed_response = parse_api_response(raw_response)

        # Check if 'messages' key exists and parse the content
        if 'response' in parsed_response and 'messages' in parsed_response['response']:
            content = parsed_response['response']['messages'][0]['content']
            
            # Handle the case where content is a JSON string
            try:
                content_dict = json.loads(content)
            except json.JSONDecodeError as e:
                logging.error(f"Failed to decode JSON from content: {e}")
                return jsonify({"status": "error", "message": "Invalid JSON content in response"}), 500

            return jsonify({"status": "success", "data": content_dict})

        else:
            logging.error("Expected keys 'response' or 'messages' not found in response")
            return jsonify({"status": "error", "message": "Invalid response format"}), 500

    except (ValueError, TypeError, json.JSONDecodeError) as e:
        logging.error(f"Error in response handling: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"status": "error", "message": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)
