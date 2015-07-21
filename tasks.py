# -*- coding: utf-8 -*-

import configparser

import pep8
import flake8.main as flake8

import pyres

DEFAULT_CONFIG = {}

q = pyres.ResQ()

class PythonReviewJob(object):

    queue = 'python_review'

    @staticmethod
    def perform(filename, commit_sha, pull_request_number, patch, content, config):
        opts = {}
        opts.update(DEFAULT_CONFIG)
        opts.update(parse_config(config))
        violations = [
            {'line': error[0], 'message': error[3]}
            for error in check_code(content, filename, **opts)
        ]
        payload = {
            'class': 'CompletedFileReviewJob',
            'args': [{
                'filename': filename,
                'commit_sha': commit_sha,
                'pull_request_number': pull_request_number,
                'patch': patch,
                'violations': violations,
            }],
        }
        q.push('high', payload)

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
