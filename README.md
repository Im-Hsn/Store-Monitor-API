### Store-Monitor-API

This project is a Flask application that generates reports on store uptime and downtime based on data stored in a database. It provides APIs for triggering report generation and retrieving the generated reports.

#### Technologies Used in Anaconda Environment:

- **Python**: The core programming language used for application development.
- **Flask**: A micro web framework used for building the web application.
- **SQLAlchemy**: A Python SQL toolkit and Object-Relational Mapping (ORM) library used for interacting with the MySQL database.
- **Pandas**: A powerful data manipulation and analysis library used for handling CSV data and processing data in DataFrames.
- **PyMySQL**: A pure-Python MySQL client library used for connecting to the MySQL database.
- **Pytz**: A Python library used for working with time zones and date/time manipulation.

#### Setup in VSCode:

**Launch Configuration:**
- Configured a launch configuration in VSCode's `launch.json` file to run the Flask application.
- Set the Python interpreter path to the one provided by the Anaconda environment (`C:\\Users\....\\python.exe`).

**Environment Variables:**
- Specified environment variables in the launch configuration, including:
  - `FLASK_APP`: Set to `app.py` to specify the entry point of the Flask application.
  - `FLASK_ENV`: Set to `development` to run the Flask app in development mode.
  - `FLASK_DEBUG`: Set to `1` to enable debug mode for the Flask application.
  - `PYTHONPATH`: Set to `${workspaceRoot}` to include the current workspace directory in Python's module search path.

**Debugging:**
- Enabled debugging using VSCode's debug functionality (`"type": "debugpy"`).
- Configured VSCode to run Flask in debug mode (`"FLASK_DEBUG": "1"`).
- Set up breakpoints and inspected variables during debugging sessions.

#### MVC Directory Structure:

```
- app.py
- config.py
- controllers/
    - store_controller.py
- models/
    - data_model.py
- report_data/ (directory to save CSV files from GET requests)
- csv_files/ (directory that contains the data as csv)
- services/
    - report_cache.py
    - report_generator.py
    - report_routes.py
```

#### File Responsibilities:

1. **app.py**: 
   - Entry point of the Flask application.
   - Registers blueprints, initializes the Flask app, creates periodic data loading thread, and runs the app.
   
2. **config.py**:
   - Contains configurations like database connection string and paths to CSV files.

3. **controllers/store_controller.py**:
   - Defines routes and handlers for store-related operations like triggering and getting reports.

4. **models/data_model.py**:
   - Handles database operations like creating tables and loading CSV data into the database.

5. **report_data/**:
   - Directory for storing CSV files generated from GET requests.

6. **services/report_cache.py**:
   - Manages caching of generated reports to avoid regenerating them unnecessarily.

7. **services/report_generator.py**:
   - Generates reports by fetching data from the database, processing it, and caching the results.

8. **services/report_routes.py**:
   - Defines routes and handlers for triggering report generation and retrieving generated reports.


#### Achievements:

- **Flask Application Setup**:
  - Configured Flask application with routes and controllers.
  - Implemented periodic data loading mechanism to update the database from CSV files.

- **Database Management**:
  - Created tables in the database based on CSV files.
  - Loaded CSV data into the database to keep it updated.

- **Report Generation**:
  - Implemented report generation logic to calculate store uptime and downtime.
  - Cached generated reports to optimize performance and avoid redundant calculations.

- **API Functionality**:
  - Created APIs that follow a trigger + poll architecture, allowing users to initiate report generation and check its status.
  - Designed error handling mechanisms to provide meaningful responses in case of errors or incomplete report generation.

- **Code Quality and Optimization**:
  - Structured the code in a modular and well-organized manner, adhering to best practices and handling corner cases effectively.
  - Employed type hints and documentation to enhance code readability and maintainability.
  - Optimized code for efficient database reads and CSV output generation, ensuring that it runs within a reasonable amount of time.

#### Backend APIs Development:

- Implemented `/trigger_report` endpoint to initiate report generation based on the provided data stored in the database.
- Developed `/get_report` endpoint to retrieve the status of the report or the generated CSV file.
- Designed the APIs to handle input/output requirements specified in the problem statement.

#### Data Management:

- Stored the provided CSV data into a relevant database.
- Implemented database operations to create tables, load CSV data, and fetch required data for report generation.
- Ensured that the data in the database is updated periodically to reflect changes in store status.

#### Report Generation:

- Designed a report generation system that calculates store uptime and downtime based on business hours and store status observations.
- Implemented logic to extrapolate uptime and downtime from periodic polls to the entire time interval within business hours.
- Ensured that uptime and downtime calculations are accurate and considerate of time zone differences.

#### Code Quality and Optimization:

- Structured the code in a modular and well-organized manner, adhering to best practices and handling corner cases effectively.
- Employed type hints and documentation to enhance code readability and maintainability.
- Optimized code for efficient database reads and CSV output generation, ensuring that it runs within a reasonable amount of time.