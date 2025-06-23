# Verbio Test #

TBD

## Set Up

### Requirements

- Docker or any OCI Container compatible implementation
- Python 3+ (check the .python-version file to get the current version)
  - We recommend to manage the python versions with py-env
- Poetry (it's possible to use without be installed on the OS, but is a little trickier)

### Install the correct python version
- (Recommend) Using PyEnv: `pyenv install`
- Using Nix

### Init the project and install the scripts
- (Recommend) Using make: `make install`
- Running manually the commands (check the make `install` target for the current steps)
  - Install the project with poetry: `poetry install`
  - Install pre-commit scripts: `poetry run pre-commit install`

## Run tests

> Run all tests and coverage: `make test`

## License
This project is licensed for private use only. See the [LICENSE](./LICENSE) file for details.
