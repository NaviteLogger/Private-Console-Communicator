# The client's config file:
import os, dotenv

# Load the environment variables from the .env file
dotenv.load_dotenv()

# Get the server's IP address and port
SERVER_IP = os.getenv("SERVER_IP")
SERVER_PORT = os.getenv("SERVER_PORT")
