import logging

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("error.log")
    ]
)

logger = logging.getLogger(__name__)

error_handler = logging.FileHandler("error.log")
error_handler.setLevel(logging.WARNING)
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger.addHandler(error_handler)
