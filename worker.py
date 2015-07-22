#!/usr/bin/env python
# encoding: utf-8
"""CLI for pyres worker."""

import logging
from optparse import OptionParser

from pyres import setup_logging, setup_pidfile
from pyres.worker import Worker

from settings import settings


def pyres_worker():
    """Worker CLI, lightly modified from pyres.
    """
    usage = 'usage: %prog [options] arg1'
    parser = OptionParser(usage=usage)

    parser.add_option('--host', dest='host', default=settings['host'])
    parser.add_option('--port', dest='port', type='int', default=settings['port'])
    parser.add_option('--password', dest='password', default=settings['password'])
    parser.add_option('-i', '--interval', dest='interval', default=None)
    parser.add_option('-l', '--log-level', dest='log_level', default='info')
    parser.add_option('-f', dest='logfile')
    parser.add_option('-p', dest='pidfile')
    parser.add_option('-t', '--timeout', dest='timeout')
    options, args = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
        parser.error("Argument must be a comma seperated list of queues")

    log_level = getattr(logging, options.log_level.upper(), 'INFO')
    setup_logging(procname="pyres_worker", log_level=log_level, filename=options.logfile)
    setup_pidfile(options.pidfile)

    interval = options.interval
    if interval is not None:
        interval = int(interval)

    timeout = options.timeout and int(options.timeout)

    queues = args[0].split(',')
    server = '{0}:{1}'.format(options.host, options.port)
    Worker.run(queues, server, options.password, interval, timeout=timeout)

if __name__ == '__main__':
    pyres_worker()
