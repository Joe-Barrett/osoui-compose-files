Docker services
===============

The main content of this project is a set of Docker Compose files
that define the containers (services) to run.

The following Docker services are defined:

+-----------------+------------------------------------------------+
| Docker service  | Description                                    |
+=================+================================================+
| tangodb         | MariaDB database holding TANGO database tables |
+-----------------+------------------------------------------------+
| databaseds      | TANGO database device server                   |
+-----------------+------------------------------------------------+
| tangogql        | GraphQL interface to Tango control system      |
+-----------------+------------------------------------------------+
| redis           | Redis in-memory key/value database             |
+-----------------+------------------------------------------------+
| webjive         | WebJive container                              |
+-----------------+------------------------------------------------+
| auth            | WebJive authentication service                 |
+-----------------+------------------------------------------------+
| dashboards      | WebJive session persistence service            |
+-----------------+------------------------------------------------+
| mongodb         | Database for WebJive session persistence       |
+-----------------+------------------------------------------------+
| dishmaster      | TMC Dish LMC master Tango device               |
+-----------------+------------------------------------------------+
| dishleafnode    | TMC Dish leaf node Tango device                |
+-----------------+------------------------------------------------+
| subarraynode1   | TMC SubArrayNode Tango device #1               |
+-----------------+------------------------------------------------+
| subarraynode2   | TMC SubArrayNode Tango device #2               |
+-----------------+------------------------------------------------+
| centralnode     | TMC CentralNode Tango device                   |
+-----------------+------------------------------------------------+
| rsyslog-tmc     | rsyslog container for TMC devices              |
+-----------------+------------------------------------------------+
| tangotest       | TANGO test device                              |
+-----------------+------------------------------------------------+
| jive            | Jive - Tango GUI application                   |
+-----------------+------------------------------------------------+
| traefik         | Reverse proxy used for WebJive HTTP routing    |
+-----------------+------------------------------------------------+

