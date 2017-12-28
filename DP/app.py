#!/usr/bin/env python3
import connexion
import logging


def get_calculation(points):
    return [points]


logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__)
app.add_api('swagger.yaml')
app.debug = True
app.run(port=8080, server='gevent')
