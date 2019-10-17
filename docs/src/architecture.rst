Basic description of Webjive architecture
===================================================

This relates to a brief definition of Webjive architecture overview

Webjive communication protocol
------------------------------------------------

The communication between Webjive and TangoGQL is done by using WebSocket. 

WebSocket is a computer communications protocol, providing full-duplex communication channels over a single TCP connection.

The way Webjive works is that it opens a socket at the beginning of the runCanvas (pressing the Start button on dashboards) 
or at the selection of a device on the overview, this socket is only closed once the Edit button 
is pressed on the dashboards, or the user exits overview or webjive itself from the browser.

Webjive data injection points
------------------------------------------------

There are two injection points of data on Webjive, one for the dashboards, another for the overview.

* webjive/src/dashboard/components/RunCanvas/emmiter.ts (for dashboards)

* webjive/src/jive/state/api/tango/index.js (for overview)

On both this files there is a function called `socketUrl(tangoDB: string)` this is where the url for socket communication is defined

Webjive data injection type
------------------------------------------------

On the communication between Webjive and TangoGQL the type of data is defined by *Graphene-Python* which is a library for building GraphQL APIs in Python. 

This are two simple examples of data between Webjive and TangoGQL

* Data example passed to TangoGQL to subscribe to one attribute *double_scalar* on the device *sys/tg_test/1* 

.. code-block:: json

    {"type":"start","payload":{"query":"\nsubscription Attributes($fullNames: [String]!) {\n  attributes(fullNames: $fullNames) {\n    device\n    attribute\n    value\n    writeValue\n    timestamp\n  }\n}","variables":{"fullNames":["sys/tg_test/1/double_scalar"]}}}

* Data example passed to Webjive for the subscription of one attribute *double_scalar* on the device *sys/tg_test/1* 

.. code-block:: json

    {"type": "data", "payload": {"data": {"attributes": {"device": "sys/tg_test/1", "attribute": "double_scalar", "value": 181.01969624669448, "writeValue": 0.0, "timestamp": 1568211918.50133}}}}