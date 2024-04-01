# Contract Testing
- This repo contains contract tests for TextNow APIs. Please follow the guidelines below for local development

### Pre-requisites
- Tools used for this project include **Python 3.11**, **Docker** to run a local **Pact** broker, and **Pipenv** for dependency management
- Install a minimum version of python3.11 which can be found [here](https://www.python.org/downloads/). **NOTE** - **DO NOT** install python3.11 using `Homebrew` as this causes issues.
- Install Docker and Docker compose (used to run local instance of Pact broker)
- Once python has been installed locally, install pipenv and pytest globally
```shell
$ pip3 install pipenv pytest
```
- Install other dependencies for the project using **pipenv** to a virtual environment
```shell
$ pipenv shell  // activates a virtual environment
$ pipenv install  // installs dependency libraries
```


### Adding Contract Tests
When adding contract tests, it's important to note that we are testing only the interaction between the consumer (client),
and the provider of the API. We use a **Pact Broker** to manage the contract (or pacts) between the consumer and the provider.
There will be cases where the provider has to have a certain state e.g. existing user, which is achieved by managing "provider states".
To manage provider states, we use a stand-alone flask app - **/src/state_app.py** to manage this.

We use the pact-python [library](https://github.com/pact-foundation/pact-python/blob/master/README.md) to write contract tests.

### Pre-Commit hooks
- Pre-commit hooks are used to ensure proper linting and unified file formatting for this project
- Initialize the pre-commits hooks
```shell
$ pre-commit install  // this needs to be run only once
```
- To run pre-commit hooks on all files in repo
```shell
$ pre-commit run --all-files
```

### Pact Versioning
- Each pact for a consumer has to have a unique version number. If there are modifications or any more tests added, the version
number will need to be updated before the pact test is run otherwise this could result in a race condition

