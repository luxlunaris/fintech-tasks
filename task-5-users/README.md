**About**

This flask app allows you to create client catalog with name, photo, phone number and e-mail data.

**Usage**

```
set FLASK_APP=server/wsgi.py

flask run
```

**Run linters**

`flake8`

**Run autoformat**

`black --py36 server/ tests/`

`isort --apply --recursive server/ tests/`

**Run tests**

`pytest -vv -cov=server tests/`