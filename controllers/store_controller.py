from flask import Blueprint, Response, jsonify, request
from typing import Dict, Union
from services.report_routes import trigger_report, get_report

store_blueprint = Blueprint('store', __name__)

@store_blueprint.route('/trigger_report', methods=['POST'])
async def trigger_report_route() -> Union[Dict[str, str], Response]:
    # Call trigger_report function
    try:
        result = await trigger_report()
        if isinstance(result, dict):
            return jsonify(result)  # Return JSON response if result is a dictionary
        else:
            return result  # Return the response directly if it's a Flask Response object
    except ValueError as e:
        return jsonify({'error': str(e)}), 400  # Return 400 Bad Request on Value Error
    except Exception as e:
        return jsonify({'error': f"An unexpected error occurred: {e}"}), 500  # Return 500 Internal Server Error

@store_blueprint.route('/get_report', methods=['GET'])
def get_report_route() -> Union[Dict[str, str]]:
    report_id = request.args.get('report_id')  # Retrieve report_id from request parameters
    if not report_id:
        return {'error': 'Report ID is required'}, 400  # Return error if report_id is missing
    try:
        return get_report(report_id)  # Retrieve report data
    except Exception as e:
        return {'error': f"An unexpected error occurred: {e}"}, 500  # Return 500 Internal Server Error
