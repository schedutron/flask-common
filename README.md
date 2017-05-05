# flask-common
A Flask extension with lots of common time-savers (file-serving, favicons, etc).

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