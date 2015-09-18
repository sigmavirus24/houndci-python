# -*- coding: utf-8 -*-

import mock
import pytest

import review

@pytest.fixture
def mock_queue(monkeypatch):
    q = mock.Mock()
    monkeypatch.setattr(review, 'q', q)
    return q

class TestReview:

    def test_unused_import(self, mock_queue):
        config = '''
        [flake8]
        exclude=
        '''
        review.PythonReviewJob.perform({
            'commit_sha': '3e01a4',
            'config': config,
            'content': 'import this',
            'filename': 'test.py',
            'patch': 7,
            'pull_request_number': 3,
        })
        violations = [
            {'line': 1, 'message': "'this' imported but unused"},
            {'line': 1, 'message': 'no newline at end of file'},
        ]
        payload = {
            'class': 'CompletedFileReviewJob',
            'args': [{
                'filename': 'test.py',
                'commit_sha': '3e01a4',
                'pull_request_number': 3,
                'patch': 7,
                'violations': violations,
            }],
        }
        mock_queue.push.assert_called_with('high', payload)

    def test_unused_import_ignored(self, mock_queue):
        config = '''
        [flake8]
        ignore=F401
        exclude=
        '''
        review.PythonReviewJob.perform({
            'commit_sha': '3e01a4',
            'config': config,
            'content': 'import this',
            'filename': 'test.py',
            'patch': 7,
            'pull_request_number': 3,
        })
        violations = [{'line': 1, 'message': 'no newline at end of file'}]
        payload = {
            'class': 'CompletedFileReviewJob',
            'args': [{
                'filename': 'test.py',
                'commit_sha': '3e01a4',
                'pull_request_number': 3,
                'patch': 7,
                'violations': violations,
            }],
        }
        mock_queue.push.assert_called_with('high', payload)

    def test_unused_import_excluded(self, mock_queue):
        config = '''
        [flake8]
        ignore=F401
        exclude=test*
        '''
        review.PythonReviewJob.perform({
            'commit_sha': '3e01a4',
            'config': config,
            'content': 'import this',
            'filename': 'test.py',
            'patch': 7,
            'pull_request_number': 3,
        })
        payload = {
            'class': 'CompletedFileReviewJob',
            'args': [{
                'filename': 'test.py',
                'commit_sha': '3e01a4',
                'pull_request_number': 3,
                'patch': 7,
                'violations': [],
            }],
        }
        mock_queue.push.assert_called_with('high', payload)
