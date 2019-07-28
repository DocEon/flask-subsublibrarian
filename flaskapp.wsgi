#! /usr/bin/python3

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/srv/flask/subsublibrarian/")
sys.path.append("/home/root/.local/lib/python3.6/site-packages")
from flaskapp import app as application
application.secret_key = "tucker"
