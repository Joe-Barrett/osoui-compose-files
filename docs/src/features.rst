TangoGQL Features Toggle
========================

TangoGQL has a function called features toggle capable of controling
some features such as pub/sub. There is a file inside tangogql/ called 
tangogql.ini, the file looks like this:

.. code-block:: console

  # this configuration file is used to hold details of which features
  # currently enabled in TangoGQL ( True = enabled False = disabled)

  [feature_flags]
  # Publish Subscribe is currently disabled for SKA
  publish_subscribe = False


Changing the `publish_subscribe = True` will enabled pub/sub on TangoGQL,
in this case, TangoGQL will try to Subscribe to changeEvents on the device,
if it fails it tries PeriodicEvents, and if that fails it falls back to
polling
