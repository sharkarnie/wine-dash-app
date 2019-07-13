# Wine Dash App

This is a dash app to visualise wine data from the UCI Machine Learning Repository.

The app is available at https://apps.sharkarnie.com/wine-dash/

The wine datasets are publicly available for research. The details are described in [Cortez et al., 2009]:

P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis.
Modeling wine preferences by data mining from physicochemical properties.
In Decision Support Systems, Elsevier, 47(4):547-553. ISSN: 0167-9236.


# Local Installation Instructions

## Install
```bash
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt  
```  

## Run the app

1. Run development server
```bash
(venv) $ python app.py
```

1. Run via gunicorn
```bash
(venv) $ gunicorn --bind 0.0.0.0:8080 wsgi:server
```

1. Run via Docker
```bash
(venv) $ make docker_build
(venv) $ make docker_run
```
1. Go to http://localhost.8080/wine-dash/
