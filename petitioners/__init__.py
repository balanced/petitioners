from __future__ import unicode_literals

import functools
import threading

import coid
import flask
import ohmr

__version__ = '0.0.5'


class Petitioner(threading.local):

    def __init__(self, tracer_header_name, tracer_prefix, app=None):
        super(Petitioner, self).__init__()
        self.tracer_header_name = tracer_header_name
        self.petition_tracer = ohmr.Tracer(coid.Id(prefix=tracer_prefix))
        self.app = app

    def generate_petition(self):
        self.petition_tracer.reset()
        flask.current_app.petition = self.petition_tracer.id
        flask.current_app.petitioners = self.petitioners

    def petition_request(self, response):
        response.headers[self.tracer_header_name] = (
            ','.join(self.petitioners)
        )

        return response

    @property
    def petitioners(self):
        current = [self.petition_tracer.id]
        petitioners = flask.request.headers.get(self.tracer_header_name, '')
        if not petitioners:
            return current
        return petitioners.split(',') + current

    @classmethod
    def register(cls, app, tracer_name='X-Petitioners', tracer_prefix='OHM-'):
        app.petitioner = Petitioner(tracer_name, tracer_prefix, app)
        app.before_request(app.petitioner.generate_petition)
        app.after_request(app.petitioner.petition_request)
        return app

    def __repr__(self):
        app = self.app or 'Detached'
        return '<Petitioner ({}){}={}>'.format(
            app, self.tracer_header_name, self.petitioners)


def register_flask_app(tracer_name, tracer_prefix):
    """
    Registers a petitioner tracer onto a flask app when it is instantiated.
    """

    def register(app_cls):

        @functools.wraps(app_cls)
        def wrapper(*args, **kwargs):
            instance = app_cls(*args, **kwargs)
            Petitioner.register(instance, tracer_name, tracer_prefix)
            return instance

        return wrapper

    return register
