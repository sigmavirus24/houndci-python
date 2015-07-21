============
hound-python
============

.. image:: https://img.shields.io/circleci/project/jmcarp/hound-python.svg
    :target: https://circleci.com/gh/jmcarp/hound-python
    :alt: Circle CI

Python review service for Hound.

Setup
=====
::

    ./bin/setup

Run
===
::

    PYTHONPATH=$(pwd):$PYTHONPATH pyres_worker python_review

Test
====
::

    py.test
