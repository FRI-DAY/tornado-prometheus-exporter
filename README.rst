Tornado Prometheus Exporter
===========================

Prometheus exporter for Tornado applications. Inspired by `Flask Prometheus Exporter <https://github.com/rycus86/prometheus_flask_exporter>`_.

*This is early alpha. At least, tests, proper docs are missing. Thus, it's not published to Pypi yet.*


Usage
-----

Instead of using ``tornado.web.Application`` as base class, use ``tornado_prometheus_exporter.Application``.


Exported Time Series
--------------------

``tornado_http_request_duration_seconds_{count,sum,bucket}`` with as many bucket series as there are buckets.

Additionally, `prometheus-client <https://github.com/prometheus/client_python>`_ exports system metrics by default.
