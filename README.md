# FSND_capstone

## Table of Contents
- [FSND_capstone](#fsnd-capstone)
  * [Project Motivation](#project-motivation)
  * [Project Structure](#project-structure)
    + [Main Files](#main-files)
    + [Project Key Dependencies](#project-key-dependencies)
  * [API Documentation](#api-documentation)
    + [Roles & Permissions](#roles---permissions)
    + [Available endpoints](#available-endpoints)
      - [GET `/actors`](#get---actors-)
      - [GET `/movies`](#get---movies-)
      - [POST `/actors`](#post---actors-)
      - [POST `/movies`](#post---movies-)
      - [POST `/appearances`](#post---appearances-)
      - [PATCH `/actors/<int:actor_id>`](#patch---actors--int-actor-id--)
      - [PATCH `/movies/<int:movie_id>`](#patch---movies--int-movie-id--)
      - [DELETE `/actors/<int:actor_id>`](#delete---actors--int-actor-id--)
      - [DELETE `/movie/<int:actor_id>`](#delete---movie--int-actor-id--)
      - [DELETE `/appearances`](#delete---appearances-)
  * [Testing](#testing)
  * [Local development](#local-development)
    + [Python 3.7](#python-37)
    + [Virtual Enviornment](#virtual-enviornment)
    + [PIP Dependencies](#pip-dependencies)
    + [Running the server](#running-the-server)
  * [FAQ](#faq)
    + [What are database migrations?](#what-are-database-migrations-)
    + [How to get a valid JWT from Auth0?](#how-to-get-a-valid-jwt-from-auth0-)
    
## Project Motivation
This project serves as a proof that shows the reader the skills acquired by me in [Udacity's Full Stack
Developer NanoDegree program.](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044)
These include:
* Data Modeling for APIs with SQLAlchemy.
  Internet Protocols and Communication.
* API Development in Flask.
* API Documentation and Testing.
* Identity and Access Management.
* Server Deployment and Containerization.

## Project Structure
### Main Files
```sh
  ├── README.md                   # The file you are currently reading.
  ├── app.py                # The main driver of the app.
  ├── Procfile              # File needed for Heroku deployment.
  ├── requirements.txt      # The dependencies we needed for running the project.
  ├── manage.py             # File to support models migrations on Heroku.
  ├── migrations            # Directory containing models migration files.
  ├── tests
  │   ├── __init__.py  
  │   ├── FSND_Capstone~    # Collection of requests importable by Postman.
  │   └── test_app.py       # Module containing unitests for the Flask API.
  ├── config
  │   ├── __init__.py  
  │   ├── dev_config.py     # Config file used when running the app in dev mode.
  │   └── test_config.py    # Config file used when running test suite.
  ├── auth
  │   ├── __init__.py
  │   ├── auth.py           # Module containing authentication logic.
  │   └── secrets.cfg       # File containing secrets (Shouldn't be shared)
  └── models
      ├── __init__.py 
      └── models.py         # SQLAlchemy models.
  ```

### Project Key Dependencies
- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.
- [SQLAlchemy ORM](https://www.sqlalchemy.org/) to be our ORM library of choice.
- [PostgreSQL](https://www.postgresql.org/) as our RDMS of choice.
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) for creating and running schema migrations.
- [Gunicorn](https://gunicorn.org/) pure-Python HTTP server for WSGI applications used in deployment.
## API Documentation
### Roles & Permissions
To work with the API, a proper login with a username assigned with a valid role must be satisfied.
The following table sums up the different possible roles that work with the API.

| Permission        | Description                   | Unauthorized | Casting Director Role | Executive Producer Role |
|-------------------|-------------------------------|:------------:|:---------------------:|:-----------------------:|
| `get:actors-detail` | Get actors data               |       -      |           X           |            X            |
| `get:movies-detail` | Get movies data               |       -      |           X           |            X            |
| `post:actors`       | Be able to post actors data   |       -      |           X           |            X            |
| `post:appearances`   | Be able to post appearances   |       -      |           X           |            X            |
| `patch:actors`      | Be able to update actors data |       -      |           X           |            X            |
| `delete:actors`     | Delete an actor               |       -      |           X           |            X            |
| `patch:movies`      | Be able to update movies data |       -      |           -           |            X            |
| `post:movies`       | Be able to post movies data   |       -      |           -           |            X            |
| `delete:appearances` | Delete an appearance          |       -      |           -           |            X            |
| `delete:movies`     | Delete a movie                |       -      |           -           |            X            |

### Available endpoints
#### GET `/actors` 
Fetches a JSON file describing actors.
- **Request arguments:** None 
- **Example response:**
```json
{
    "actors": [
        {
            "age": 20,
            "filmography": [
                "Rick & Morty"
            ],
            "gender": "Male",
            "id": 1,
            "name": "Leonardo Dicaprio"
        },
        ...
    ],
    "success": true
}
```

#### GET `/movies` 
Fetches a JSON file describing movies.
- **Request arguments:** None 
- **Example response:**
```json

{
    "movies": [
        {
            "cast": [
                "Leonardo Dicaprio"
            ],
            "id": 18,
            "release_date": "Fri, 20 Apr 1990 00:00:00 GMT",
            "title": "Rick & Morty"
        },
        ...
    ],
    "success": true
}
```

#### POST `/actors` 
Inserts a new actor record in the db.
- **Request body:** JSON
  - name:string 
  - birth_date:date, like '2000-01-01' 
  - gender:string
- **Example response:**
```json
{
    "new_actor": {
        "age": 30,
        "filmography": [],
        "gender": "male",
        "id": 35,
        "name": "Rick"
    },
    "success": true
}
```

#### POST `/movies` 
Inserts a new movie record in the db.
- **Request body:** JSON
  - title:string 
  - release_date:date, like '2000-01-01' 
- **Example response:**
```json
{
    "new_movie": {
        "cast": [],
        "id": 26,
        "release_date": "Fri, 20 Apr 1990 00:00:00 GMT",
        "title": "Rick & Morty"
    },
    "success": true
}
```

#### POST `/appearances` 
Given the corresponding IDs, links an actor and a movie in the db.
- **Request body:** JSON
  - actor_id:int 
  - movie_id:int
- **Example response:**
```json
{
    "new_appearance": {
        "actor": {
            "id": 15,
            "name": "Morty"
        },
        "movie": {
            "id": 15,
            "title": "Rick & Morty: The madness"
        }
    },
    "success": true
}
```
{
    "patched_movie": {
        "cast": [
            "Morty"
        ],
        "id": 15,
        "release_date": "Fri, 20 Apr 1990 00:00:00 GMT",
        "title": "Rick & Morty: The madness"
    },
    "success": true
}

#### PATCH `/actors/<int:actor_id>` 
Updates an existing actor record in the db.
- **Request arguments:**
  - actor_id:int
- **Request body:** JSON (Must include at least one of the following)
  - name:string 
  - birth_date:date, like '2000-01-01' 
  - gender:string
- **Example response:**
```json
{
    "patched_actor": {
        "age": 20,
        "filmography": [
            "Rick & Morty: The madness"
        ],
        "gender": "Male",
        "id": 15,
        "name": "Morty"
    },
    "success": true
}
```

#### PATCH `/movies/<int:movie_id>` 
Updates an existing movie record in the db.
- **Request arguments:**
  - movie_id:int
- **Request body:** JSON (Must include at least one of the following)
  - title:string 
  - release_date:date, like '2000-01-01' 
- **Example response:**
```json
{
    "patched_movie": {
        "cast": [
            "Morty"
        ],
        "id": 15,
        "release_date": "Fri, 20 Apr 1990 00:00:00 GMT",
        "title": "Rick & Morty: The madness"
    },
    "success": true
}
```

#### DELETE `/actors/<int:actor_id>` 
Delete an existing actor from the db.
- **Request arguments:**
  - actor_id:int
- **Example response:**
```json
{
    "delete": "10",
    "success": true
}
```

#### DELETE `/movie/<int:actor_id>` 
Delete an existing movie from the db.
- **Request arguments:**
  - movie_id:int
- **Example response:**
```json
{
    "delete": "10",
    "success": true
}
```
#### DELETE `/appearances` 
Delete an existing appearance from the db.
- **Request body:** JSON
  - actor_id:int
  - movie_id:int
- **Example response:**
```json
{
    "delete": {
        "actor_id": 10,
        "movie_id": 20
      },
    "success": true
}
```

## Testing
To run the tests, make sure that proper JWT tokens have been placed in [secrets.cfg](auth/secrets.cfg). Then, cd to
the [backend/tests](tests) folder and run the following command in the terminal: 
```
python test_app.py
```
## Local development

### Python 3.7

This project is intended to work with Python 3.7. Follow instructions to install python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

### Virtual Enviornment

It is recommended working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the [/backend](./backend) directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

### Running the server

From within the [backend/](backend/) directory first ensure you are working using your created virtual environment.

First set the environment variables running the following commands:

```bash
export FLASK_APP=api.py;
export FLASK_ENV=development;
```

>Alternatively in Windows PS:
>```bash
>$env:FLASK_APP="api"
>$env:FLASK_ENV="development"
>```

To run the server, execute:

```bash
flask run
```

## FAQ
### What are database migrations?
**Migrations** help us to manage modifications in our data schema over time, like a **version control** system.
A migration file keeps track of changes to our database schema (structure of our database), so that:

* We can encapsulate a set of changes to our database schema, made over time.
* We can quickly roll back changes. 
* We can test changes before we make them.

By doing this, migrations stack together in order to form the latest version of our database schema.

In python, we can achieve schema migration with the library **Flask-Migrate**, which allows us to:
* `flask db init`: Initialize a migration repository.
* `flask db migrate -m "Initial migration."`: Generate an initial migration.
* `flask db upgrade`: Apply an initial migration.
* `flask db downgrade`: Rollback applied migrations.

Also, Flask-Migrate gives us the following advantages:
* Auto-detects changes from the old version & new version of the SQLAlchemy models.
* Creates a migration script that resolves differences between the old & new versions.
* Gives fine-grain control to change existing tables.

Which is much better, because:
* We can keep existing schema structures, only modifying what needs to be modified.
* We can keep existing data.
* We isolate units of change in migration scripts that we can roll back to a “safe” db state.

More info at [Flask-Migrate docs](https://flask-migrate.readthedocs.io/).


### How to get a valid JWT from Auth0?
Once the domain and API have been set up in Auth0, to get a valid JWT login to the Auth0 authentication website for your API following this structure:
```shell
https://<DOMAIN>/authorize?audience=<API>&response_type=token&client_id=<CLIENT-ID>&redirect_uri=<REDIRECT-URI>&state=STATE
```
In this project the values are as follows:
* **DOMAIN**: `toblerone.eu.auth0.com`
* **API**: `FSND_Capstone`
* **CLIENT-ID**: `6hU4gMiWHReM9bDkXIvDttKcmyEJiAJ5`
* **REDIRECT-URI**: `https://localhost:8080/login-results`

Thus, making:
```shell
https://toblerone.eu.auth0.com/authorize?audience=FSND_Capstone&response_type=token&client_id=6hU4gMiWHReM9bDkXIvDttKcmyEJiAJ5&redirect_uri=https://localhost:8080/login-results&state=STATE
```

Which would give a token similar to this one:
```shell
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ino3R1NYdlNTYk9uOEgxZ2QxT0RUWiJ9.eyJpc3MiOiJodHRwczovL3RvYmxlcm9uZS5ldS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDk4ODM4MzIxODEwNTA5NDc4MTAiLCJhdWQiOiJGU05EX0NhcHN0b25lIiwiaWF0IjoxNjE4MDY5NjU3LCJleHAiOjE2MTgxNTQyNTcsImF6cCI6IjZoVTRnTWlXSFJlTTliRGtYSXZEdHRLY215RUppQUo1Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMtZGV0YWlsIiwiZ2V0Om1vdmllcy1kZXRhaWwiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.2yBhsdN60MU1kJxBTWltSVjscVcwrxgoc2qhQutf_kJJtq9a_AKO7nnYjxGNrv2S5bJTcRAeoqKSonexkCJ-su8KlOpWFtafjisKseBLtnDhNXUqbf4Chn3JW_K7p0XveHAYyR2aGuQ8JZ8ulssAQ9hGibHEKAl90O6xpAqrM09k7ZWCfjbZWjNDTAm2bQopVruhwo5lT17IHos1rlMb3ZdyW-CTSPC1VongRRozio9dvCYdo6B2BaNTaLBhiokipdLVo9tI8dyCoJQQJd_VERT5LFVO5vGLnvMYfUACjv0HSWitagynY7zNgbwysiQY0MXgqhbBwww6QN_ONG1A9A
```

