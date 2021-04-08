# FSND_capstone

## Table of Contents

## Project Motivation
This project serves as a proof that shows the reader the skills acquired by me in [Udacity's Full Stack
Developer NanoDegree program.](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044)
These include:
* Data Modeling for APIs.
* API Development and API Documentation.
* Identity and Access Management.
* Server Deployment and Containerization.

## Requirements:

### Data Modeling
* Flask | SQLAlchemy | Python:
    * DO NOT USE raw SQL (only where there are not SQLAlchemy equivalent expressions).
    * Appropiately use SQLAlchemy to define models.
    * Methods to serialize model data.
    * Helper methods to simplify API behavior such as insert, update and delete.
    * Appropiate primary and foreign key ids.
    * Correct data types for fields.

### API Architecture
* RESTful principles are followed throughout the project, including appropriate naming of endpoints, use of HTTP methods GET, POST, and DELETE.
* Ensure CRUD (Create, read, update, delete) endpoints are available, at least:
    * Two GET requests.
    * One POST request.
    * One PATCH request.
    * One DELETE request.
* Utilize the '@app.errorhandler' decorator to format error responses as JSON objects for at least four different status codes.

### Role Based Authentication:
Project includes a custom @requires_auth decorator that:
* Gets the Authorization header from the request.
* Decodes and verifies the JWT using the Auth0 secret.
* take an argument to describe the action.
> i.e. @require_auth(‘create:drink’)
  
* Raises an error if:
    * The token is expired.
    * The claims are invalid.
    * The token is invalid.
    * The JWT doesn’t contain the proper action.

Project includes at least two different roles that have distinct permissions for actions.
* These roles and permissions are clearly defined in the project README.

### Testing
* Include at least one test for expected success and error behavior for each endpoint using the unittest library.
* Include tests demonstrating role-based access control, at least two per role.

### Third-Party Authentication
Auth0 is set up and running at the time of submission.

All required configuration settings are included in a bash file which export:
* The Auth0 Domain Name.
* The JWT code signing secret.
* The Auth0 Client ID.

Configure roles-based access control (RBAC).
* Roles and permission tables are configured in Auth0.
* Access of roles is limited. Includes at least two different roles with different permissions.
* The JWT includes the RBAC permission claims.

### Deployment
* API is hosted live via Heroku.
* URL is provided in project README.
* API can be accessed by URL and requires authentication.
* Includes instructions to set up authentication.
* Instructions are provided in README for setting up authentication so reviewers can test endpoints at live application endpoint.

### Code Quality and Documentation
The code adheres to the PEP 8 style guide and follows common best practices, including:
* Variable and function names are clear.
* Endpoints are logically named.
* Code is commented appropriately.
* Secrets are stored as environment variables.

Project demonstrates reliability and testability.
* Application can be run with no errors and responds with the expected results.
* API test suite for endpoints and RBAC behavior runs without errors or failures.

Project demonstrates maintainability.
* Variable names are logical, code is DRY and well-commented where code complexity makes them useful.

### Last steps
Create a README which includes:
* Motivation for project.
* Project dependencies, local development and hosting instructions.
* Detailed instructions for scripts to install any project dependencies, and to run the development server.
* Documentation of API behavior and RBAC controls.

Create a reviewer_README which includes:
* URL where the application is hosted.
* Instructions to set up authentication.

### To Stand Out
* Create a frontend that works with your API - including a login that will redirect the user to Auth0. Let your work come to life on the screen!!
* Implement authorization with a tool other than email or Google. Add more options for your users’ authentication flow.
* Deploy your application and database on AWS. Checkout this link and this for Postgres to get started.


###  Udacity's proposal: Casting Agency Specifications.

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

* Models:
    * Movies with attributes title and release date.
    * Actors with attributes name, age and gender.


* Endpoints:
    * GET /actors and /movies
    * DELETE /actors/ and /movies/
    * POST /actors and /movies and
    * PATCH /actors/ and /movies/


* Roles:
    * Casting Assistant:
        * Can view actors and movies.
    * Casting Director:
        * All permissions a Casting Assistant has and:
            * Add or delete an actor from the database.
            * Modify actors or movies.
    * Executive Producer
        * All permissions a Casting Director has and:
            * Add or delete a movie from the database.


* Tests:
    * One test for success behavior of each endpoint.
    * One test for error behavior of each endpoint.
    * At least two tests of RBAC for each role.