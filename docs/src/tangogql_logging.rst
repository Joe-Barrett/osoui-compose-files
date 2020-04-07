TangoGQL Logging in SKA
=======================

TangoGQL logging system uses a file called `logging.yaml` by default 
to configure the logging capabilites.

Please refer to the TangoGQL Official Documentation for the logging details: https://web-maxiv-tangogql.readthedocs.io/en/latest/logging.html

To change the format of the logging, for example to the SKA standard one can simply  change this line:

.. code-block:: console

    format: "1|%(asctime)s.%(msecs)03dZ|%(levelname)s|%(threadName)s|%(funcName)s|%(filename)s#%(lineno)d|%(message)s"

Optional: There is a way to pass a new file to tangoGQL using the *LOG_CFG* var, and example can be found on the *tangogql.yml* file

.. code-block:: console

   version: "2.2"

    volumes:
    tangogql-logs: {}

    services:
    tangogql:
        image: web-maxiv-tangogql_tangoql:latest
        container_name: ${CONTAINER_NAME_PREFIX}tangogql
        network_mode: ${NETWORK_MODE}
        command: /bin/bash -c "source activate graphql && adev runserver tangogql/aioserver.py --app-factory=dev_run --port=5004"
        depends_on:
        - databaseds
        - redis
        volumes:
        - tangogql-logs:/var/log/tangogql
        - ./ska-logging.yaml:/tangogql/ska-logging.yaml
        environment:
        - LOG_CFG=ska-logging.yaml
        - TANGO_HOST=${TANGO_HOST}
        - LOG_PATH=/var/log/tangogql
        # If this is not set, the output of python is delayed and only shows when the docker container restarts
        - PYTHONUNBUFFERED=1
        labels:
        - "traefik.frontend.rule=Host:localhost; PathPrefix: /testdb/db, /testdb/socket, /testdb/graphiql; ReplacePathRegex: ^/testdb/((?:db|socket|graphiql.*?)/?)/?$$ /$$1"
        - "traefik.port=5004"

    redis:
        image: redis
        container_name: redis
        network_mode: ${NETWORK_MODE}

By default two files are created, one called *info.log* and *error.log* if using ska-logging file this files will go to
*/var/log/tangogql* 