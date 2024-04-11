import os

# MySQL Connection String
DB_CONNECTION_STRING = "mysql+pymysql://root:root@localhost/store_monitor"

# Path to the CSV files directory
CSV_FILES_DIR = os.path.join(os.getcwd(), 'csv_files')
