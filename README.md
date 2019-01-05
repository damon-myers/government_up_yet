# government_up_yet

Is the government up yet?

`government_up_yet` is a Flask service that uses News API to gather insight into whether the current government shutdown has ceased.

`frotend` contains a simple React page that queries the `government_up_yet` service to determine whether the shutdown has ended.

# Installing dependencies

## `frontend`
```
cd frontend
yarn install
```

## `government_up_yet`

If you don't have a `venv` yet:
```
cd government_up_yet
python -m venv venv
```

Otherwise:
```
source venv/bin/activate
pip install -r requirements.txt
```


# Starting the app

## `frontend`
```
cd frontend
yarn start
```

## `government_up_yet`
```
cd government_up_yet
export FLASK_APP=service.py
flask run
```
