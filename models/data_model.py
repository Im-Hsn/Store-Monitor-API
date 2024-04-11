from sqlalchemy import create_engine, inspect, BigInteger
import pandas as pd
import os
from config import DB_CONNECTION_STRING, CSV_FILES_DIR

engine = create_engine(DB_CONNECTION_STRING)

store_status_path = os.path.join(CSV_FILES_DIR, 'store_status.csv')
store_hours_path = os.path.join(CSV_FILES_DIR, 'store_hours.csv')
store_timezones_path = os.path.join(CSV_FILES_DIR, 'store_timezones.csv')

# Function to create tables if they don't exist
def create_tables():
    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    for table_name, file_path in [
        ('store_status', store_status_path),
        ('store_hours', store_hours_path),
        ('store_timezones', store_timezones_path)
    ]:
        if table_name not in table_names:
            try:
                df = pd.read_csv(file_path)
                # Specify dtype for the store_id column
                if 'store_id' in df.columns:
                    dtype_mapping = {'store_id': BigInteger}
                else:
                    dtype_mapping = None

                df.to_sql(table_name, con=engine, if_exists='fail', index=False, dtype=dtype_mapping)
                print(f"Table '{table_name}' created successfully.")
            except FileNotFoundError:
                print(f"Error: {file_path} not found")
            except Exception as e:
                print(f"Error creating '{table_name}' table: {e}")

# Function to load CSV data into the database
def load_csv_data():
    for table_name, file_path in [
        ('store_status', store_status_path),
        ('store_hours', store_hours_path),
        ('store_timezones', store_timezones_path)
    ]:
        try:
            df = pd.read_csv(file_path)
            df.to_sql(table_name, con=engine, if_exists='replace', index=False)
            print(f"CSV data loaded into the '{table_name}' table.")
        except FileNotFoundError:
            print(f"Error: {file_path} not found")
        except Exception as e:
            print(f"Error loading CSV data for '{table_name}' table: {e}")

