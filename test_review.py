# -*- coding: utf-8 -*-

import mock
import pytest

import tasks

@pytest.fixture
def mock_queue(monkeypatch):
    q = mock.Mock()
    monkeypatch.setattr(tasks, 'q', q)
    return q

class TestReview:

    def test_unused_import(self, mock_queue):
        tasks.PythonReviewJob.perform('test.py', '3e01a4', 3, 7, 'import this', '')
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
        '''
        tasks.PythonReviewJob.perform('test.py', '3e01a4', 3, 7, 'import this', config)
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
        tasks.PythonReviewJob.perform('test.py', '3e01a4', 3, 7, 'import this', config)
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
