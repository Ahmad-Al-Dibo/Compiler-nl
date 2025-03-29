import logging
import datetime as dt
from tools.system_variabels import ADMIN_ERRORS
logging.basicConfig(filename='error.log', level=logging.ERROR)

def log_error(error_code):
    try:
        error_details = ADMIN_ERRORS.get(error_code, "Unknown error")
        logging.error(f"{error_code}: {error_details['message']} - {dt.datetime.now()}")
    except Exception as e:
        raise e
