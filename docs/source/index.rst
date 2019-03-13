.. OSOUI-Compose-Files documentation master file, created by
   sphinx-quickstart on Mon Dec 17 14:01:07 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SKA Engineering UI Compose Utilities
====================================
The following documentation outlines Docker Compose files which are useful to the SKA OSO-UI team during development.
This includes caveats and how to use them.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   tangogql
   webjive


Usage
=====
Prerequsities
-------------

Before using, the TangoGQL and WebJive repositories should be cloned and their
paths added to the `.env` file.

 - https://github.com/ska-telescope/tangogql
 - https://github.com/ska-telescope/webjive

Docker Compose should be installed on your system and the Docker daemon should
be running.

To Run
    Replace <service stack> with the stack name you want to run.

    `docker-compose -f <service stack>.yml up -d`

To Stop
    This command stops the services. The optional `--rmi` flag removes all 
    images relating to that service stack. All removes all images, local 
    removes only the images which were built locally.

    `docker-compose -f <service stack>.yml down [--rmi all|local]`

Logs
    This command displays the logs of a container for any chosen service stack.
    The services can be found in the individual pages of each stack.

    `docker-compose -f <service stack>.yml logs <service name>`

Status
    This command displays the status of all containers in the stack.

    `docker-compose -f <service stack>.yml ps`
