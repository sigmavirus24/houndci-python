# -*- coding: utf-8 -*-
"""Parse Redis settings from environment."""

import os

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

parsed = urlparse(os.getenv('REDIS_URL', 'redis://localhost:6379'))
settings = {
    'host': parsed.hostname,
    'port': parsed.port,
    'password': parsed.password,
}
