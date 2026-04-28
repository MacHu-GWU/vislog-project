# -*- coding: utf-8 -*-

import pytest
from vislog import VisLog


def pytest_configure(config):
    config.addinivalue_line("markers", "no_toggle: skip the logger toggle fixture")

logger = VisLog(name="vis_logger_unit_test")

# --- Toggle: comment / uncomment to control log output during tests ---
SHOW_LOG = False
# SHOW_LOG = True
