import threading
from typing import Dict
from flask import jsonify
import uuid
from .report_generator import generate_report
from .report_cache import report_cache

async def trigger_report() -> Dict[str, str]:
    report_id = uuid.uuid4().hex  # Generate a unique report ID
    report_cache[report_id] = {'status': 'Running'}  # Mark the report as running in the cache
    try:
        #Start a new thread to generate the report
        report_thread = threading.Thread(target=generate_report, args=(report_id,))
        report_thread.start()
        return {'report_id': report_id}  # Return the generated report ID
    except ValueError as e:
        # Handle the ValueError and return a custom error response
        return {'error': str(e)}, 400  # 400 Bad Request indicates client error
    except Exception as e:
        return {'error': f"An unexpected error occurred: {e}"}, 500  # 500 Internal Server Error for unexpected errors


def get_report(report_id: str):
    if report_id not in report_cache:
        return jsonify({'error': 'Invalid report_id'}), 404  # Report ID not found in cache

    report_info = report_cache[report_id]
    if report_info['status'] == 'Running':
        return jsonify({'status': 'Running'}), 200  # Return "Running" status if report is still being generated
    
    elif report_info['status'] == 'Complete':
        report_df = report_info['report']  # Retrieve the report DataFrame from the cache
        report_file_path = f"report_data/report_{report_id}.csv"
        
        # Save the report DataFrame as a CSV file
        report_df.to_csv(report_file_path, index=False)
        
        report_info = report_cache[report_id]
        return {'status': report_info['status']}, 200
    else:
        return jsonify({'error': 'Unknown status'}), 500  # Unknown status encountered