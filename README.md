
# **News Article Analysis and Event Modeling**

## **Overview**

This project focuses on analyzing global news articles using data science techniques such as topic modeling and event detection. The results are visualized through an interactive Streamlit dashboard. The project is structured to be modular, with separate components for data processing, model building, and visualization.

## **Project Structure**


WEEK-0/
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI configuration
├── .vscode/                       # VS Code specific settings (if any)
├── docs/                          # Documentation files (if any)
├── notebooks/
│   └── parse_news_data.ipynb      # Jupyter notebook for parsing and analyzing news data
├── scripts/
│   ├── __init__.py                # Package initializer for the scripts module
│   ├── helper.py                  # Helper functions used across the project
│   └── topic_analysis.py          # Script for performing topic analysis
├── src/
│   ├── __init__.py                # Package initializer for the src module
│   ├── db/
│   │   ├── __init__.py            # Database initialization script
│   ├── dashboard.py               # Streamlit dashboard script
│   ├── data_loader.py             # Script for loading data into the database
│   └── helper.py                  # Additional helper functions specific to src
├── tests/
│   ├── __init__.py                # Package initializer for the tests module
│   └── test_sample.py             # Sample test file for testing functionality
├── venv/                          # Virtual environment directory
├── .env                           # Environment variables configuration file
├── .gitignore                     # Git ignore file to exclude unnecessary files from version control
├── Dockerfile                     # Dockerfile for containerizing the application
├── main.py                        # Main script to run the full project
└── requirements.txt               # Python dependencies list


## **Getting Started** 

### **Prerequisites**

- **Python 3.x** installed on your machine.
- **Virtual Environment**: It’s recommended to use a virtual environment to manage dependencies.
- **PostgreSQL**: Ensure you have PostgreSQL installed and running.

### **Installation**

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd WEEK-0
   ```

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Create a `.env` file in the root directory and add your environment variables (e.g., database credentials):
     ```
     DATABASE_URL=postgresql://username:password@localhost:5432/yourdatabase
     ```

### **Running the Project**

1. **Initialize the Database**:
   - The database initialization script is included in `src/db/__init__.py`. This script creates the necessary tables in your PostgreSQL database.

   ```bash
   python src/db/__init__.py
   ```

2. **Run the Streamlit Dashboard**:
   - To start the Streamlit dashboard, use the following command:
   ```bash
   streamlit run src/dashboard.py
   ```

3. **Run the Full Project**:
   - To run the full project locally, including executing the Jupyter notebook (`parse_news_data.ipynb`), initializing the database, creating tables, and launching the Streamlit dashboard, run:
   ```bash
   python main.py
   ```
   - The `main.py` script orchestrates the execution of the notebook, database initialization, and the dashboard launch.

### **Project Components**

- **Jupyter Notebooks**: 
  - The `parse_news_data.ipynb` notebook is used for initial data parsing and exploratory analysis.
- **Scripts**: 
  - The `scripts/` directory contains helper scripts like `helper.py` for common functions and `topic_analysis.py` for performing topic analysis.
- **Streamlit Dashboard**: 
  - The `src/dashboard.py` script sets up an interactive dashboard to visualize topics, events, and correlations derived from the news articles.
- **Database**: 
  - The `src/db/` directory contains scripts for setting up and managing the PostgreSQL database.
- **Testing**: 
  - The `tests/` directory includes test cases to ensure the functionality of the project components.

### **Deployment**

- **Docker**: 
  - A Dockerfile is provided for containerizing the application. To build and run the Docker image:
    ```bash
    docker build -t news_analysis .
    docker run -p 8501:8501 news_analysis
    ```
- **GitHub Actions**:
  - Continuous Integration (CI) is set up with GitHub Actions, configured in `.github/workflows/ci.yml`. This ensures that all pushes trigger automated testing and deployment steps.

### **Running Tests**

- You can run the tests using:
  ```bash
  pytest
  ```

### **Contributing**

Contributions are welcome! Please fork the repository and submit a pull request.

