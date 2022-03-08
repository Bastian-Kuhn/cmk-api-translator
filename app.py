#!/usr/bin/env python3
import os
if 'env' not in os.environ:
    os.environ['env'] = 'dev'
from application import app
