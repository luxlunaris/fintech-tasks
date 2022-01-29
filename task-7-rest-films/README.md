**About**

This is the RESTful API built on flask that allows you to work with movies, users and movie ratings made by users.

Built within docker. 

Swagger UI documentaion might be seen on localhost:5000 when application is up.

**Usage**

`docker-compose build`

`docker-compose up`

**Run linters**

`flake8`

**Run autoformat**

`isort --apply --recursive api/ tests/`

`black --py37 api/ tests/`

**Run tests**

```
docker-compose build

docker-compose run --rm server bash

pytest -vv --cov=api tests/
```

96% coverage