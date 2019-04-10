Usage
=====

To pull the required Docker images from the SKA Docker registry, execute:

.. code-block:: console

   # download all required Docker images
   make pull

Optional: the images can be pulled from an alternate registry and/or
account by supplying the DOCKER_REGISTRY_HOST and DOCKER_REGISTRY_USER
Makefile variables respectively, e.g.,

.. code-block:: console

   # download foo/tango-cpp, foo/tango-jive, etc. from a registry at
   # localhost:5000
   make DOCKER_REGISTRY_HOST=localhost:5000 DOCKER_REGISTRY_USER=foo pull

To start WebJive and a minimal Tango system, execute:

.. code-block:: console

   # start WebJive and a Tango control system
   make up

To start TMC devices, execute:

.. code-block:: console

   # start TMC devices
   make tmc

Optional applications and device servers can be launched by calling the
*start* make target followed by the name of the service. For example:

.. code-block:: console

   # run Jive
   make start jive
   # run tangotest
   make start tangotest

To display the status of the Docker services, execute

.. code-block:: console

   # print status of Docker services
   make status

Running services can be stopped individually or as a whole using the
*stop* make target or *down* make target respectively. For instance,

.. code-block:: console

   # stop just the tangotest device server, leaving other services running
   make stop tangotest
   # stop all services and tear down the system
   make down

After starting the WebJive containers and any required additional containers, navigate to
`http://localhost:22484/testdb` to access WebJive. The following credentials can be used:

Username
    user1

Password
    abc123
