# alljob

_________________
## getting started
<br>

### requirements

- poetry
- python 3.10
- node

_________________
### installation

<br>

#### backend

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

##### .ENV schema
create `.env` file in `services/backend/src` to make backend working
```
PORT=[port]
HOST=[host]
DB_URI=[mongo db uri]
````

_________________
#### scrapper

create `.env` file in `services/scrapper/src` to make scrapper working
```
DB_URI=[mongo db uri]
````

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
_________________

#### frontend

```
cd ./frontend
npm install
npm run dev
```

