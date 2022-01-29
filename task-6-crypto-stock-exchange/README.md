**About**

This application is simulation of cryptocurrency stock exchange with registration and authentication.

It can maintain multiple processes.

**Setup**

For running this app you need to have Docker

```
docker-compose build

docker-compose up
```

**Usage**

Connect to 127.0.0.1:5000. Make an account, log yourself in and try it.

**Run linters**

`flake8`

**Run autoformat**

`isort --apply --recursive`

`black --py36 app/ tests/`

**Run tests**

```
docker-compose build

docker-compose run --rm server bash

pytest -vv --cov=app tests/


```


