# This file will be solely responsible for connecting to the PostgreSQL database.
import psycopg2, os
from dotenv import load_dotenv

# Get the environment variables
load_dotenv()


# Connect to the PostgreSQL database
def connect():
    try:
        connection = psycopg2.connect(
            user=os.getenv("POSTGRESQL_DB_USER"),
            password=os.getenv("POSTGRESQL_DB_PASSWORD"),
            host=os.getenv("POSTGRESQL_DB_HOST"),
            port=os.getenv("POSTGRESQL_DB_PORT"),
            database="postgres",
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL database, error: ", error)
