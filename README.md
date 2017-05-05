# flask-common
A Flask extension with lots of common time-savers (file-serving, favicons, etc).


An example app:

```python
from flask import Flask
from flask_common import Common
import time

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

- `X-Powered-By=Flask`.
- `X-Processed-Time: 0.000133037567139`.
- Favicon support.
- `@common.cache.cached(timeout=50)`.

## Web Server: Gunicorn

- `WEB_CONCURRENCY`
-  `PORT`

## File Server: WhiteNoise

Flask-Common automatically configures [WhiteNoise](http://whitenoise.evans.io) to serve your static files.