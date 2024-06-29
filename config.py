import logging

# Configure logging
logging.basicConfig(
    filename='log.txt',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Disable Flask's default logging to stderr
log = logging.getLogger('werkzeug')
log.disabled = True
