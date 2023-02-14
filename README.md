# Dynamic notes

Dynamic Notes is a simple User CRUD API built with FastAPI and SQLAlchemy. This API allows you to create, read, update and delete users, as well as creating, reading, updating and deleting notes associated with each user.

## Features

* User management (create, read, update, delete)
* Note management (create, read, update, delete)
* Secure password hashing and verification

## Endpoints
* /docs - Swagger UI documentation

* /user: create a new user
* /auth/login: authenticate a user and return a JWT token
* /notes: manage notes (create, read, update, delete)
* /users: manage users (read, update, delete)

## Built With
- [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM for database management 
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation and settings management
- [Passlib](https://passlib.readthedocs.io/en/stable/index.html) - Password hashing and verification

## Author
Oluwaseun Tanimola - [GitHub](https://github.com/Oluwaseun241)