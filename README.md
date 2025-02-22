## get started ##

git clone clone https://github.com/TaylonSopeletto/ambra

### setting up django for the first time ###

`virtualenv venv`

`venv\Scripts\activate`

`pip install -r requirements.txt`

`python3 manage.py migrate`

`python3 manage.py runserver`

## set up webpack ##

`cd store/static`

`npm i`

`npm run watch`

## FYI ##

javascript and css in dev mode should be edited here `/store/static/resources`

the files in `/store/static/public` are the compiled version


