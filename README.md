# Book API

A simple Flask REST API for managing a small book catalog with SQLite storage, JWT-protected write operations, and Swagger documentation.

## Overview

This project exposes endpoints to:

- list books with pagination and filtering
- retrieve a single book by ID
- create, update, and delete books
- authenticate with a demo login endpoint and receive a JWT token
- explore the API from the Swagger UI

## Tech stack

- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite
- Pydantic
- PyJWT
- Flasgger

## Project structure

```text
.
├── app.py                  # Flask app and API routes
├── models.py               # SQLAlchemy model definition
├── books.db                # SQLite database file
├── docker-compose.yml      # Docker Compose setup
├── Dockerfile              # Container image definition
└── book_service/
    └── requirements.txt    # Checked-in dependency file
```

## Features

- CRUD operations for books
- JWT authentication for write endpoints
- request validation with Pydantic
- SQLite persistence
- Swagger UI at `/swagger`
- author and year filtering on the books listing endpoint

## Data model

Each book contains:

- `id`
- `title`
- `author`
- `year`
- `isbn`

## Prerequisites

- Python 3.11 recommended
- pip

## Installation

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies.

Example:

```bash
cd Book-API
python -m venv .venv
source .venv/bin/activate
pip install Flask Flask-SQLAlchemy pydantic PyJWT flasgger
```

> Note: the repository currently includes `book_service/requirements.txt`, but the application also imports `pydantic`, `PyJWT`, and `flasgger`. Install those packages manually as shown above unless the dependency file is updated.

## Configuration

The app can use these environment variables:

- `SECRET_KEY`
- `JWT_SECRET_KEY`

If they are not set, the app falls back to built-in development defaults.

## Running locally

```bash
cd Book-API
python app.py
```

The API starts on:

- `http://127.0.0.1:5000`

Swagger UI is available at:

- `http://127.0.0.1:5000/swagger`

## Running with Docker Compose

```bash
cd Book-API
docker compose up --build
```

The container exposes port `5000`.

## Authentication

Write operations require a JWT in the `Authorization` header.

Header format:

```text
Authorization: Bearer <token>
```

Demo login credentials currently hardcoded in the app:

- username: `admin`
- password: `password`

### Get a token

```bash
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "password"
  }'
```

## API endpoints

| Method | Endpoint | Description | Auth required |
| --- | --- | --- | --- |
| GET | `/` | Health/welcome message | No |
| POST | `/login` | Authenticate and return a JWT token | No |
| GET | `/books` | List books with optional filters | No |
| GET | `/books/<id>` | Get a single book by ID | No |
| POST | `/books` | Create a new book | Yes |
| PUT | `/books/<id>` | Update an existing book | Yes |
| DELETE | `/books/<id>` | Delete a book | Yes |

## Using the books endpoint

### List books

Optional query parameters:

- `page`
- `author`
- `year`

Example:

```bash
curl "http://127.0.0.1:5000/books?page=1&author=George&year=1949"
```

### Create a book

```bash
curl -X POST http://127.0.0.1:5000/books \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "title": "1984",
    "author": "George Orwell",
    "year": 1949,
    "isbn": "9780451524935"
  }'
```

### Update a book

```bash
curl -X PUT http://127.0.0.1:5000/books/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "title": "Animal Farm",
    "author": "George Orwell",
    "year": 1945,
    "isbn": "9780451526342"
  }'
```

### Delete a book

```bash
curl -X DELETE http://127.0.0.1:5000/books/1 \
  -H "Authorization: Bearer <token>"
```

## Validation rules

### Book payload

- `title`: 1 to 50 characters
- `author`: 1 to 50 characters
- `year`: between 1800 and 2025
- `isbn`: 1 to 50 characters

### Login payload

- `username`: 1 to 30 characters
- `password`: 1 to 30 characters

## Notes

- The application uses SQLite and stores data in `books.db`.
- The books list is currently hardcoded to a page size of `2` items per page.
- The database tables are created automatically when the app starts through `python app.py`.

## Development status

This is a small learning-style API project and currently does not include a dedicated automated test suite or lint configuration in the repository.
