# -*- coding: utf-8 -*-
"""Python review task."""

import pyres

import flake
from settings import settings

q = pyres.ResQ(
    '{0}:{1}'.format(settings['host'], settings['port']),
    settings['password'],
)

class PythonReviewJob(object):

    queue = 'python_review'

    @staticmethod
    def perform(filename, commit_sha, pull_request_number, patch, content, config):
        opts = {}
        opts.update(flake.parse_config(config))
        violations = [
            {'line': error[0], 'message': error[3]}
            for error in flake.check_code(content, filename, **opts)
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
