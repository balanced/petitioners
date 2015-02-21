# FRL Flask Request Tracer

[![Build Status](https://secure.travis-ci.org/balanced/petitioners.png?branch=master)](http://travis-ci.org/balanced/petitioners) [![Latest Version](https://pypip.in/version/petitioners/badge.svg)](https://pypi.python.org/pypi/petitioners/) [![Downloads](https://pypip.in/download/petitioners/badge.svg)](https://pypi.python.org/pypi/petitioners/) [![Supported Python versions](https://pypip.in/py_versions/petitioners/badge.svg)](https://pypi.python.org/pypi/petitioners/) [![License](https://pypip.in/license/petitioners/badge.svg)](https://pypi.python.org/pypi/petitioners/)

Adds tracing to requests generated by Flask apps.

```python
@petitioners.register_flask_app('X-Request-Trace', 'Trace-')
class FlaskApp(flask.Flask):
    pass
```

Requests to the app will now generate response with headers tagged like

```
X-Request-Trace: Trace-123123
```

If this header already exists then it will be appended to like

```
X-Request-Trace: Trace-123123,Trace-123432
```

The current trace value can be accessed from the app via the `petitioner` property

```
import flask

print flask.current_app.petitioner
'[Trace-123123,Trace-123432]'
```
