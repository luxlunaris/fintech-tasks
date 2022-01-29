**About**

This aiohttp webserver allows you using chat rooms. 

**Usage**

```
docker-compose build

docker-compose up
```

After running the app, you may connect to localhost:5000/ and see list of chats. Choose any and enjoy chatting.

You can connect to localhost:5000/api/doc/ to see Swagger UI documentation on additional endpoints (create and delete chats).

**Run litners**

`flake8`

**Run autoformat**

`black --py36 api/ tests/`

`isort --apply --recursive`

**Run tests**

After running the app, in new console:

```
docker-compose run --rm web bash

pytest -vv --cov=api tests/
```