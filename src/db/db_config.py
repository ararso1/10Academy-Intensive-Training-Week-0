from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost:8000/news_Article"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def test_connection():
    try:
        # Try to create a session and execute a simple SQL query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1")) # type: ignore
            print("Connection to the database is successful:", result.fetchone())
    except Exception as e:
        print("Connection failed:", str(e))

if __name__ == "__main__":
    test_connection()
