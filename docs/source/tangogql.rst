========
TangoGQL
========
This compose file runs TangoGQL with the SKA Tango database and database 
device server to provide test devices. This does *not* include any operable 
devices and should be considered the bare minimum to simply test the 
stack works.

Services
========
tangodb
-------
This container houses the Tango MySQL database

databaseds
----------
This container hosts the Tango device server for the database.

tangogql
--------
The container for the TangoGQL service. Makes queries and connections to the 
databaseds container on port 10000

redis
-----
Possibly data storage for the logs, currently not sure.
