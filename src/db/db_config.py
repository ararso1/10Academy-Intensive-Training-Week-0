import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the database credentials from environment variables
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')

# Example of using these credentials in a connection string or database client
DATABASE_URL = f"postgresql+psycopg2://{db_username}:{db_password}@localhost:8000/news_Article" # type: ignore

# Create the engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    """
    Initialize the database by creating all tables defined in the models.
    """
    # Dynamically import the src.models module
    # models_module = __import__('src.models', fromlist=['*'])
    from db.models import Article,Topic, Event, Feature
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

def test_connection():
    """
    Test the connection to the database.
    """
    try:
        # Try to create a session and execute a simple SQL query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))  # type: ignore
            print("Connection to the database is successful:", result.fetchone())
    except Exception as e:
        print("Connection failed:", str(e))

if __name__ == "__main__":
    test_connection()
