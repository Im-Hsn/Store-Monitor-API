from flask import Flask
from controllers.store_controller import store_blueprint
from models.data_model import create_tables, load_csv_data
import threading
import time

app = Flask(__name__)
app.register_blueprint(store_blueprint)

# Function to periodically check for new data and load it into the database
def periodic_data_loader():
    while True:
        time.sleep(3600)  # Wait for 1 hour
        try:
            load_csv_data()
        except Exception as e:
            print(f"Error loading CSV data: {e}")

if __name__ == '__main__':

    try:
        create_tables()  # Create tables before starting the app

        periodic_loader_thread = threading.Thread(target=periodic_data_loader, daemon=True)
        periodic_loader_thread.start()

        app.run(debug=True)
    except Exception as e:
            print(f"Error running main: {e}")