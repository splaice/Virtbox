import os
import sys
import logging

# basic logging
if 'DEBUG' in os.environ:
    debug = os.environ.get('DEBUG')
    if debug:
        log_file = os.path.join('/tmp', '%s.log' % debug)
        hdlr = logging.FileHandler(log_file, mode='w')
    else:
        hdlr = logging.StreamHandler(sys.stdout)
else:
    hdlr = logging.NullHandler()

logger = logging.getLogger('virtbox')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
