# Verbio Test

Backend project using Python and FastAPI.

## Overview

### Oversized

This project intentionally includes more complexity than required, as detecting a palindrome is a relatively trivial
task. However, if the underlying process were more resource-intensive, it would make more sense to have an asynchronous
API and provide an alternative contract to retrieve information.

In such cases, we might consider other ways of API consumption, such as:

- WebHooks
- HTTP Live Streaming (to support long-lived connections)
- WebSockets
- Server-Sent Events, etc.

### Persistence

I chose not to implement a production-ready persistence layer, as I preferred to focus on implementation design rather
than specific technologies.

The architecture allows for easy swapping of the persistence mechanism. By simply implementing the repository contract
and updating the dependency injection (DI) container, you can switch to a different technology. The design aims to
follow the SOLID principles where possible.

### Testing

I’ve included only a few basic tests. In a production environment, the service should include more comprehensive
coverage, including other types of tests such as functional or integration tests. However, for this assessment, the
current tests should be enough to demonstrate my typical approach.

### TODO

I ran slightly short on time to include everything I would like. That said, I prefer to go over technical details in our
next meeting, where we can review the project together and I can answer all your questions.

## Set Up

### Requirements

- Docker or any OCI Container compatible implementation
- Python 3+ (check the [.python-version](.python-version) file to get the current version)
  - We recommend managing the python versions with py-env
- Poetry (it's possible to use without being installed on the OS, but is a little trickier)
- (Recommended) Make
- (Recommended) PyEnv

### Install the correct python version (check the [.python-version](.python-version) file!)
- (Recommend) Using PyEnv: `pyenv install`
- Using Nix

### Init the project and install the scripts
- (Recommend) Using make: `make install`
- Running manually the commands (check the make `install` target for the current steps)
  - Install the project with poetry: `poetry install`
  - Install pre-commit scripts: `poetry run pre-commit install`

### Start the project locally

- Once the environment is ready, run the make, `make run` and be fun!
- Check the OpenAPI swagger UI on: http://localhost:8000/docs

## TL;DR

Run everything with: `make install run`.

## Run tests

Run all tests and coverage: `make test`

## License
This project is licensed for private use only. See the [LICENSE](./LICENSE) file for details.
