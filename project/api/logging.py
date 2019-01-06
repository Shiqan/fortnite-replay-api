import logging
import os

logger = logging.getLogger(__name__)
level = os.environ.get('LOG_LEVEL')
logging.basicConfig(level=level)
