import logging  # Built-in Python module for logging messages
from datetime import datetime  # To generate a timestamp for log file naming
import os  # For file and directory path handling
from Project.Constants.constants import *  # Importing constant values (e.g., LOG_FOLDER_NAME)

# -----------------------------------------------
# GENERATE A TIMESTAMP FOR THE CURRENT RUN
# Example format: '2025-05-22_14-35-10'
# -----------------------------------------------
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

# -----------------------------------------------
# CREATE A UNIQUE LOG FILE NAME USING TIMESTAMP
# Example: 'log2025-05-22_14-35-10.log'
# -----------------------------------------------
LOG_FILE_NAME = f"log{CURRENT_TIME_STAMP}.log"

# -----------------------------------------------
# ENSURE THAT THE LOG DIRECTORY EXISTS
# Creates the directory if it doesn't exist
# LOG_FOLDER_NAME should be defined in constants
# -----------------------------------------------
os.makedirs(LOG_FOLDER_NAME, exist_ok=True)

# -----------------------------------------------
# COMPLETE FILE PATH FOR LOG FILE
# Example: 'logs/log2025-05-22_14-35-10.log'
# -----------------------------------------------
LOG_FILE_PATH = os.path.join(LOG_FOLDER_NAME, LOG_FILE_NAME)

# -----------------------------------------------
# CONFIGURE THE LOGGING MODULE
# - filename: specifies the log file
# - filemode='w': overwrites file each time
# - level=logging.INFO: logs INFO and higher-level messages
# - format: includes timestamp, level, and message
# -----------------------------------------------
logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


