import logging
import os

logger = logging.getLogger(__name__)
level = os.environ.get('LOG_LEVEL', 'DEBUG')
logging.basicConfig(level=level)
