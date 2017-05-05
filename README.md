# flask-common
A Flask extension with lots of common time-savers (file-serving, favicons, etc).


An example app:

```python
import time
from flask import Flask
from flask_common import Common

app = Flask(__name__)
app.debug = True

common = Common(app)

@app.route("/")
@common.cache.cached(timeout=50)
def hello():
    time.sleep(1)
    return "Hello World!"


if __name__ == "__main__":
    common.serve()
```

## Nicities

HTTP Headers:

- `X-Powered-By: Flask`.
- `X-Processed-Time: 0.000133037567139`.

Other nice things:

- `@common.cache.cached(timeout=50)` decorator for caching views in memory. 
- Favicon support (`/favicon.ico` redirects to `/static/favicon.ico`).

## Web Server: Gunicorn

Automatically uses Gunicorn for production (when `Flask.debug = False`), Flask's dev server for development. 

Configuration environment variables:

- `WEB_CONCURRENCY` for specifying the number of synchronous gunicorn workers. 
-  `PORT` for binding to a specific port. 

## File Server: WhiteNoise

Flask-Common automatically configures [WhiteNoise](http://whitenoise.evans.io) to serve your static files.
