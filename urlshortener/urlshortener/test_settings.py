# Settings for testing

from settings import *

# Don't need debug for tests
DEBUG = False
TEMPLATE_DEBUG = False

# SQLIte3 database for faster testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# No need for South
SOUTH_TESTS_MIGRATE = False
SKIP_SOUTH_TESTS = True
SKIP_RACKSPACE_API = True

import logging
logging.disable(logging.CRITICAL)


