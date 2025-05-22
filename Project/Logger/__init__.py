import logging
from datetime import datetime
import os
from Project.Constants.constants import *

CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
LOG_FILE_NAME = f"log{CURRENT_TIME_STAMP}.log"

os.makedirs(LOG_FOLDER_NAME, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_FOLDER_NAME, LOG_FILE_NAME)

# Configure logging

logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


