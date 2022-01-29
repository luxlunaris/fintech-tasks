**About**

This is a simple API built inside docker with flask and redis that allows resizing of images.

You can push json payload with base64 image and size, then you get url, which will lead you to your request when it's complete.

All requests are being put in redis queue, from where a humble rq worker takes job and processes it.

**Usage**

```
docker-compose build

docker-compose up
```

You can connect to localhost:5000 to see Swagger UI documentation on this API.

**Run litners**

`flake8`

**Run autoformat**

`black --py36 api/ tests/`

`isort --apply --recursive`

**Run tests**

```
docker-compose build

docker-compose run --rm web bash

pytest -vv --cov=api tests/
```