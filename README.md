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
    curl -X POST http://localhost:5000/feedback -d '{"upvote":true, "client":"client3", "token":"zC92PlhJ1rbwbwsdbNA6aejcOsSXszaCBqZ8jD6z"}' -H 'Content-Type: application/json'
    ```

## Client side

1. Install opencv

    ```bash
       CLIENT_ID=client3 CLIENT_SECRET=zC92PlhJ1rbwbwsdbNA6aejcOsSXszaCBqZ8jD6z API_ADDRESS=https://apiserver.privatedomain.com/feedback pipenv run python first.py
    ```