# Contract Testing
We currently have situation where there is a gap (in time) between when changes are made to Backend APIs (provider), and when clients (consumer)
ingest or implement these changes. These could lead to breaking changes being released to stage or production or significant time
passing before the consumers realize that they need to make changes.

These are the key reasons for implementing contract testing which aims is to fill the gap between changes made to the specific provider,
and what the consumer expects.

This repo contains contract tests for TextNow APIs. Please follow the guidelines below for local development

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
The pact tests are from the consumer driven point of view and grouped into logical areas e.g. UserConsumer class, handles all interactions
with the API **/api2.0/users/**, the EmailConsumer class handles all interactions with the API **/api2.0/email/**

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

### Running Tests (local development)
- Start the pact broker container using the docker-compose file
- Note that an environment variables file **default.env** located in the same place as the **docker-compose.yml** file
is required as this where the environment variables **FLASK_SERVER_PORT**, and **TN_ADMIN_SECRET** are set.
Ensure the contents of **default.env** have the following remaining environment variables
```dotenv
FLASK_SERVER_PORT=5001
TN_ADMIN_SECRET=*******
PACT_BROKER_ALLOW_PUBLIC_READ=true"
PACT_BROKER_BASIC_AUTH_USERNAME=pactbroker
PACT_BROKER_BASIC_AUTH_PASSWORD=pactbroker
PACT_BROKER_DATABASE_URL="postgres://postgres:root@pact-postgres/postgres"
POSTGRES_USER=postgres
POSTGRES_PASSWORD=root
POSTGRES_DB=postgres
```
- Start the containers using the command below
```shell
$ docker-compose up -d
```
- Run tests from the terminal using **pytest** with the **--broker-url** argument
- Note: The first time you run the pact tests after starting the pact broker, the provider tests
will fail as the pacts have not been registered initially. You would need to run the command below again. Another work around
is to run the individual consumer tests to register the pacts with the broker.
```shell
$ pytest -v tests --broker-url=http://<pact_broker_username>:<pact_broker_password@localhost:9292
```
- Run individual pact tests from the terminal using
```shell
$ pytest -v tests/<test_name> --broker-url=http://<pact_broker_username>:<pact_broker_password@localhost:9292
```

