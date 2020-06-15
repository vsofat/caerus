#!/usr/bin/python3
import sys
sys.path.insert(0,"/var/www/caerus/")
sys.path.insert(0,"/var/www/caerus/caerus/")

import logging
logging.basicConfig(stream=sys.stderr)

from caerus import app as application