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
temporal workflow terminate --workflow-id=send-email-activity
```

## Curl commands

### subscribe

```bash
curl -X POST -d "email=test@example.com&message=hello" http://localhost:5000/subscribe/
```

### get-details

```bash
curl -X GET http://localhost:5000/get-details/
```

### unsubscribe

```bash
curl -X DELETE http://localhost:5000/unsubscribe/
```
