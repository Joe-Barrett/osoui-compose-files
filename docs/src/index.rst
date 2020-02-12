.. OSOUI-Compose-Files documentation master file, created by
   sphinx-quickstart on Mon Dec 17 14:01:07 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Integrated OSO-UI / TMC container environment
==============================================

This project defines a container environment that integrates OSO-UI
applications with TMC devices and a Tango control system. It
defines a set of docker-compose configurations for OSO-UI applications
and their dependencies so that a test integrated system can be
instantiated on a developer's laptop or workstation.

WebJive General documentation is available in the following link: https://webjive.readthedocs.io/en/latest/index.html

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   overview
   services
   usage
   contribution
   device
   architecture
   webjive_suite_candc
   webjive_suite_module_view
   pubsub
   tangogql
   features

Prerequsities
-------------

To use this project, Docker >= v18 and GNU Make must be installed.

Development of the OSO-UI applications
--------------------------------------

The development of the OSO-UI webjive application suite is a collaberation between
software developers at the Max IV  Laboratory in Lund  and the SKA OSO-UI team.

Any development work on the webjive suite follows an agreed :doc:`./contribution`

