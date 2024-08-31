import os
import sys
# Adjust the Python path to include the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

import papermill as pm
from src.db.db_config import init_db
import pandas as pd
import subprocess

def main():
    # Initialize the database and create tables
    print("Initializing database...")
    init_db()
    
    print("Executing Jupyter notebook...")
    notebook_path = 'notebooks/parse_news_data.ipynb'  # Update this with the path to your notebook
    output_notebook_path = 'notebooks/parse_news_data_output.ipynb'
    
    # Run the notebook
    pm.execute_notebook(
        notebook_path,
        output_notebook_path
    )

    # Run the Streamlit dashboard
    print("Launching Streamlit dashboard...")
    dashboard_path = 'src/dashboards.py'
    subprocess.run(["streamlit", "run", dashboard_path])
    
    print("Project execution completed.")

if __name__ == "__main__":
    main()
