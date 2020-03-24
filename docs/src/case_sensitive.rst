TangoGQL Case Sensitive Convention
==================================

Tango Controls Framework uses ZMQ to manage events. ZMQ is not case
sensitive so, it is necessary to define a convention to use upper case
and lower case. 

The Tango convention is to uses only lower case in Tango attribute name. But
it accepts also the upper case. Also different tools, as POGO, permit to 
declare an attribute name with a different style of the lower case. 

The situation can create conflicts when TangoGQL uses ZMQ to pass attribute 
names that are not case sensitive. 

In order to avoid conflicts, TangoGQL transforms every attribute name in lower 
case. In this way, also if the attribute name doesn't follow the Tango Naming 
convention, the communication with TangoGQL proceed without problems. 