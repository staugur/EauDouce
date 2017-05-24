# -*- coding: utf-8 -*-
"""
    EauDouce.super_debug
    ~~~~~~~~~~~~~~

    This is the entry file for the flask application performance monitoring and debugging model.

    :copyright: (c) 2017 by Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

from main import app
from config import GLOBAL
from werkzeug.contrib.profiler import ProfilerMiddleware

if __name__ == "__main__":
    Host = GLOBAL.get('Host')
    Port = GLOBAL.get('Port')
    app.config['PROFILE'] = True
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [30])
    app.run(debug=True, host=Host, port=int(Port))
