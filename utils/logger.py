import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for detailed logs
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Logs to a file
        logging.StreamHandler()  # Logs to console
    ]
)

# Get a logger instance
logger = logging.getLogger("StreamlitApp")