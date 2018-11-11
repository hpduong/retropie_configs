# coding: utf-8
# Created on: 04.01.2018
# Author: Roman Miroshnychenko aka Roman V.M. (roman1972@gmail.com)
"""
General classes and functions for interacting with Kodi
"""

from __future__ import absolute_import
import sys as _sys
from xbmc import *
from .utils import PY2 as _PY2, patch_module as _patch_module

if _PY2:
    _patch_module(_sys.modules[__name__])
