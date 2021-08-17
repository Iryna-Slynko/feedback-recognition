# feedback-recognition

## Server side

```powershell
$env:FLASK_APP = "server"
pip install pipenv
pipenv install
pipenv run flask db migrate
pipenv run flask run
```

Access: initial user password 'secret'

## API

```powershell
$env:FLASK_APP = "api"
pipenv run flask run
```

### Add data

1. Login to the site.
1. Create a client. Copy token.
1. Run command:

    ```bash
    curl -X POST http://localhost:5000/feedback -d '{"upvote":true, "client":"client21", "token":"DV6fxJZt86SQ8E3JiTOwTrj0emYcYV7psOfpkP0h"}' -H 'Content-Type: application/json'
    ```

## Client size

1. Install opencv
    ```bash
        pipenv run python first.py
    ```