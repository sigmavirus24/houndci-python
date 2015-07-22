# -*- coding: utf-8 -*-
"""Utilities for working with flake8."""

import configparser

import pep8
import flake8.main as flake8

def parse_config(config):
    parser = configparser.RawConfigParser()
    parser.read_string(config)
    try:
        return dict(parser['flake8'])
    except KeyError:
        return {}

def check_code(code, filename, **kwargs):
    flake8_style = flake8.get_style_guide(**kwargs)
    flake8_style.options.report = QuietReport(flake8_style.options)
    if flake8_style.excluded(filename):
        return []
    return flake8_style.input_file(None, lines=code.splitlines(True))

class QuietReport(pep8.StandardReport):
    def get_file_results(self):
        return sorted(self._deferred_print)
