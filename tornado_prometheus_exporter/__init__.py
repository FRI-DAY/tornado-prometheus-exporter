from logging import getLogger

from prometheus_client import Histogram, start_http_server
from prometheus_client import REGISTRY as DEFAULT_REGISTRY
from tornado.web import Application as _Application

log = getLogger('tornado_prometheus_exporter')


class Application(_Application):
    """ Adds Prometheus integration to Tornado """
    def __init__(self, *args, **kwargs):
        """
        :param prometheus_static_labels: Labels that get statically applied to
            the generated metrics.
        :param prometheus_registry: Prometheus registry that metrics are
            registered to.
        :param int prometheus_port: If not None, start prometheus server with
            given registry on given port.
        :param prometheus_buckets: Gets passed to prometheus_client.Histogram.
        """
        super(Application, self).__init__(*args, **kwargs)

        self.static_labels = kwargs.pop('static_labels', {})
        self.registry = kwargs.pop('registry', DEFAULT_REGISTRY)

        port = kwargs.pop('prometheus_port', None)
        buckets = kwargs.pop('prometheus_buckets', None)

        default_labels = ['handler', 'method', 'status']
        histogram_kwargs = {
            'labelnames': default_labels + list(self.static_labels.keys()),
            'registry': self.registry,
        }
        if buckets is not None:
            histogram_kwargs['buckets'] = buckets
        self.request_time_histogram = Histogram(
            'tornado_http_request_duration_seconds',
            'Tornado HTTP request duration in seconds',
            **histogram_kwargs,
        )
        if port is not None:
            log.info('Starting Prometheus exporter on port %s', port)
            start_http_server(port, registry=self.registry)

    def log_request(self, handler):
        """ Adds request metrics to the Prometheus export """
        super(Application, self).log_request(handler)
        self.request_time_histogram \
            .labels(
                handler=type(handler).__name__.lower(),
                method=handler.request.method.lower(),
                status=int(handler.get_status()),
                **self.static_labels) \
            .observe(handler.request.request_time())
