# Subscription tutorial

## Install

Install [poetry](https://python-poetry.org/docs/).

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Install project dependencies.

```bash
poetry install
```

## Run

```python
poetry run python run_worker.py
poetry run python run_flask.py
```

## Terminate

```bash
temporal workflow terminate --workflow-id=example@example.com
```

## Curl commands

### subscribe

Use the curl command to send a POST request to `http://localhost:5000/subscribe` with the email address as a JSON payload.

```bash
curl -X POST -H "Content-Type: application/json" -d '{"email": "example@example.com"}' http://localhost:5000/subscribe
```

### get-details

The email address should be included in the query string parameter of the URL.

```bash
curl -X GET -H "Content-Type: application/json" http://localhost:5000/get_details?email=example@example.com

```

### Unsubscribe

Send a `DELETE` request with the email address in a JSON payload:

```bash
curl -X DELETE -H "Content-Type: application/json" -d '{"email": "example@example.com"}' http://localhost:5000/unsubscribe
```
