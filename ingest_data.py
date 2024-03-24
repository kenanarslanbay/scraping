import os
import pandas as pd
from sqlalchemy import create_engine
import urllib.parse
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy import create_engine, text


# Load environment variables from .env file
load_dotenv()

def create_estates_table(engine):
    """
    Creating table in db to be used in ingestion
    """
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS estates;"))
        conn.execute(text("""
            CREATE TABLE estates (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                image_urls TEXT[],
                price NUMERIC(12, 2)
            );
        """))

def get_db_engine():
    """
    Retrieve database connection details from environment variables
    """
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('POSTGRES_PORT', '5432')
    db = os.getenv('POSTGRES_DB')
    
    # Create a connection string with URL encoding
    connection_string = f'postgresql://{user}:{urllib.parse.quote(password)}@{host}:{port}/{db}'
    
    return create_engine(connection_string)

def ingest_data_to_postgresql(engine, table_name, csv_file):
    """
    Ingest the scraped data in data folder to table in db
    """
    try:
        print("Reading CSV file...")
        df = pd.read_csv(csv_file)
    
        # Convert the 'image_url' column to a list of lists (each containing a single URL)
        df['image_urls'] = df['image_urls'].apply(lambda x: x.split(';') if isinstance(x, str) else [])

        
        print("Inserting data into the PostgreSQL table...")
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False, dtype={'image_urls': sqlalchemy.types.ARRAY(sqlalchemy.types.Text)})
        
        print("Finished ingesting data into the PostgreSQL database")
    
    except Exception as e:
        print("An error occurred:", e)

if __name__ == '__main__':
    
    table_name = 'estates'  
    csv_file = os.getenv('CSV_FILE_PATH') 
    
    # Initialize database engine
    engine = get_db_engine()
    
    # Creating the table
    create_estates_table(engine)
    
    # Proceed to data ingestion
    ingest_data_to_postgresql(engine, table_name, csv_file)
