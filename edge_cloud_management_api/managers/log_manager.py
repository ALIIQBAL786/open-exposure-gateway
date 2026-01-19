import logging
import sys

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Edge Cloud Management API")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
