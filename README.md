# Full-Stack-Nanodegree-capstone-project

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process

## Motivation for project

Here I present you the capstone project of Udacity Fullstack Web Developer Nanodegree program which demonstrates the skillset of using Flask, SQLAlchemy, Auth0 and Heroku to develop and deploy a RESTful API with automated tests and user roles.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

For the purposes of the project in the repo there is `casting_agency_db_backup.sql`restore file.

Because of the fact that the automated tests are modifying the data, It is recommended to create 2 databases: one for test purposes and another for you to use the API.

In order to restore the database, please run the code below:

```shell
createdb casting_agency
psql casting_agency<casting_agency_db_backup.sql
```

Bear in mind that the Postgres should be running.

## Running the server

Before running the API, ensure you are working using your created virtual environment.

In `setup.sh` there are all the environment variables needed for the project. 

To run the app, execute the following code:

```shell
. ./setup.sh
flask run
```

In case the tokens provided in the file are expired and the API calls fails, please login again using the credentials provided, replace them in `setup.sh`and run `. ./setup.sh `again.

Also, the automated tests uses the token authentication headers from the file.

## Deployment

The project is deployed at:



Please use the Auth0 link below to generate new tokens for each role:

https://dev-06u0yfz9.eu.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=LaTOLLq06w9V4PZm4fqCGai45Nimx0Mc&redirect_uri=http://127.0.0.1:8080

You can use the credentials below to login:

- Casting assistant role:
  - email: `casting.assitant@udacity.com` password: `g_hNa67L?L-tb+.`
- Casting director role:
  - email: `casting.director@udacity.com` password: `?L-tb+.g_hNa67L`
- Executive producer role:
  - email: `executive.producer@udacity.com` password: `?L-thNa67Lb+.g_`

Generated tokens:

- Casting assistant role:
- Casting director role:
- Executive producer role:

## Running the test suite

Because of the fact that the automated tests are modifying the data, It is recommended to have 2 databases: one for test purposes and another for you to use the API.

Here are steps to follow before running the tests:

```
dropdb casting_agency_test
createdb casting_agency_test
psql casting_agency_test<casting_agency_db_backup.sql
python test_flaskr.py
```

It is recommended to recreate the db before every test suite run.

## API Reference

## Movies

### `GET /movies`

##### `Public`

- Fetches all the movies from the database
- Request arguments: None
- Returns: A list of movies contains id, title, genre and release_date for each movie

#### `Response`

```json
{
    "movies": [
        {
            "genre": "Drama",
            "id": 1,
            "release_date": "2002-08-02",
            "title": "Titanic"
        },
        {
            "genre": "Action",
            "id": 2,
            "release_date": "2001-08-02",
            "title": "Transoporter"
        },
        {
            "genre": "Fantasy",
            "id": 3,
            "release_date": "2001-08-02",
            "title": "Star Wars"
        }
    ],
    "success": true
}
```

### `POST /movies`

##### `Executive Producer`

- Creates a movie from the request's body
- Request arguments: None
- Returns: JSON object with success status and id of the newly created movie 

#### `Body`

```json
{
    "title": "Skyfall 3",
    "release_date": "2015-03-02",
    "genre": "Action"
}
```

#### `Response`

```json
{
    "movie_id": 4,
    "success": true
}
```

### `PATCH /movies/<int:id>`

##### `Casting Director or Executive Producer`

- Updates a movie using the information provided by request's body
- Request arguments: Movie id
- Returns: JSON of the updated movie and status

#### `Body`

```json
{
    "title": "Skyfall",
    "release_date": "2015-03-02"
}
```

#### `Response`

```json
{
    "movie": {
        "genre": "Action",
        "id": 4,
        "release_date": "2015-03-02",
        "title": "Skyfall"
    },
    "success": true
}
```

### `DELETE /movies/<int:id>`

##### `Executive Producer`

- Deletes a movie based the request argument
- Request arguments: Movie id
- Returns: JSON of the deleted movie id and success status

#### `Response`

```json
{
    "deleted": 4,
    "success": true
}
```

## Actors

### `GET /actors`

##### `Public`

- Fetches all the actors from the database
- Request arguments: None
- Returns:  A list of actors contains id, age, gender and name for each actor

#### `Response`

```
{
    "actors": [
        {
            "age": 55,
            "gender": "male",
            "id": 1,
            "name": "Jason Statham"
        },
        {
            "age": 56,
            "gender": "male",
            "id": 2,
            "name": "Liam Neeson"
        },
        {
            "age": 57,
            "gender": "female",
            "id": 3,
            "name": "Meryl Streep"
        }
    ],
    "success": true
}
```

### `POST /actors`

##### `Casting Director or Executive Producer`

- Creates an actor from the request's body
- Request arguments: None
- Returns:  JSON object with success status and id of the newly created actor

#### `Body`

```
{
            "name": "Daniel Kraig",
            "gender": "male",
            "age": 50
}
```

#### `Response`

```
{
    "actor_id": 4,
    "success": true
}
```

### `PATCH /actors/<int:id>`

##### `Casting Director or Executive Producer`

- Updates an actor by request body
- Request arguments: Actor id
- Returns: JSON with success status and the updated actor object

#### `Body`

```json
{
    "name": "Nina Dobrev",
    "gender": "female",
    "age": "33"
}
```

#### `Response`

```json
{
    "actor": {
        "age": 33,
        "gender": "female",
        "id": 4,
        "name": "Nina Dobrev"
    },
    "success": true
}
```

### `DELETE /actors/<int:id>`

##### `Casting Director or Executive Producer`

- Deletes an actor based the request argument
- Request arguments: Actor id
- Returns: JSON of success status and the deleted actor id

#### `Response`

```json
{
    "deleted": 4,
    "success": true
}
```

## Status Codes

- `200` : Request has been fulfilled
- `201` : Entity has been created
- `400` : Bad request
- `401` : Unauthorized
- `403` : Forbidden
- `404` : Resource not found
- `405` : Method not allowed
- `412` : Precondition for resource failed
- `422` : Request cant be processed