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

The documentation is composed of three parts. The **Dashboard developer**, 
which explains how to use Webjive, step by step, for end user. The **developer**
part, which shows technical aspects of Webjive. And **External Resources** with
a list of useful documentation regarding Webjive and other tools. 

Official documentation
----------------------

In this documentation, only documents regarding SKA are reported. For the complete
documentation of Webjive and TangoGQL, please refer to the official documentation. 

Webjive
    Webjive is a web-based program that allows a user to create a visual 
    interface using widgetswhich may include charts, numerical indicators 
    or dials that interface to Tango device back end database.
    WebJive General documentation is available in the following link,
    : https://webjive.readthedocs.io/en/latest/index.html
    In the documentation you will find sections as: 

    * Architecture: a description of the Webjive Software Architecture
    * Widgets: the documentation of how the widgets works
    * `How to deploy a widget`_

    .. _How to deploy a widget: https://webjive.readthedocs.io/en/latest/widget.html

TangoGQL
    A GraphQL implementation for Tango, used by Webjive to access the Tango
    Controls Framework
    TangoGQL General documentation is available in the following link,
    : https://web-maxiv-tangogql.readthedocs.io/en/latest/

    In the documentation you will find sections as: 

    * `API Documentation`_
    * `Examples`_
    * TangoGQL features and convention

   .. _API Documentation: https://web-maxiv-tangogql.readthedocs.io/en/latest/api.html
   .. _Examples: https://web-maxiv-tangogql.readthedocs.io/en/latest/examples.html

Webjive authorization
    Webjive authorization (work in progress): https://webjive-auth.readthedocs.io/en/latest/

Webjive Dashboard
    Webjive Dashboard (work in progress): https://webjive-dashboards.readthedocs.io/en/latest/


.. toctree::
   :maxdepth: 2
   :caption: For dashboard developer:

   overview
   how_run
   quick_start


.. toctree::
   :maxdepth: 2
   :caption: For developer:

   services
   usage
   contribution
   device
   pubsub

.. toctree::
   :caption: External resources:

   Webjive <https://webjive.readthedocs.io/en/latest/index.html>
   TangoGQL <https://web-maxiv-tangogql.readthedocs.io/en/latest/index.html>
   Webjive authorization <https://webjive-auth.readthedocs.io/en/latest/>
   Webjive Dashboard <https://webjive-dashboards.readthedocs.io/en/latest/>



Prerequsities
-------------

To use this project, Docker >= v18 and GNU Make must be installed.

Development of the OSO-UI applications
--------------------------------------

The development of the OSO-UI webjive application suite is a collaboration between
software developers at the Max IV  Laboratory in Lund  and the SKA Buttons team.

Any development work on the webjive suite follows an agreed :doc:`./contribution`

