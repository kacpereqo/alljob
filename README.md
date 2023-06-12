
# alljob
Alljob is a it job offers aggregator

# Installation

### Requirements
- [Python 3.10](https://www.python.org/downloads/release/python-31011/)
- [Poetry](https://github.com/python-poetry/poetry)
- [Node](https://github.com/nodejs/node)

- poetry / pip
- python 3.10
- node
- working internet connection



## scrapper

This part of the code is responsible for downloading offers from the following websites:

 - [x] nofluffjobs.com
 - [x] justjoin.it
 - [ ] it.pracuj.pl
 - [x] bulldogjob.pl
 
downloaded data is serialized and sent to the MongoDB database.

##### Environment variables schema
Create an `.env` file in `services/scrapper/src` to make the scrapper working

```
DB_URI=[mongo db uri]
```

##### poetry
```
poetry install
poetry shell
cd ./services/scrapper/src/
poetry run python main.py
```

##### pip
```
pip install -r requirements.txt
cd ./services/scrapper/src/
python main.py
```

## backend

##### poetry
```
poetry install
poetry shell
cd .services/backend/src/
poetry run python main.py
```

##### pip
```
pip install -r requirements.txt
cd ./services/backend/src/
python main.py
```

  

##### Environment variables schema

Create an `.env` file in `services/backend/src` to make the backend working

```
PORT=[port]
HOST=[host]
DB_URI=[mongo db uri]
```

## frontend

```
cd ./frontend
npm install
npm run dev
```
