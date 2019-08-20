"""
This file contains an example itango session that exercises the OET and TMC
functionality for SP-142.

To run these commands, start the integrated environment and connect to the
OET with:

  make ds-config
  make import_dashboards
  make mvp
  docker attach oet

... and then execute the commands below at the command prompt.

"""

# change directory to this folder
  cd /host/sp354

# start up the telescope, turning DISH master devices on
telescope = SKAMid()
telescope.start_up()

# Create a sub-array and allocate two dishes to it
subarray = SubArray(1)
allocation = ResourceAllocation(dishes=[Dish(1), Dish(2)])
subarray.allocate(allocation)

# Load and configure a sub-array from a CDM definition file
# This CDM configures for a Band 1 observation of Polaris.
subarray.configure_from_file('polaris_b1.json')

# scan for 10 seconds
subarray.scan(10.0)

# We can't reconfigure a sub-array yet, so mark the end of
# the observation
subarray.end_sb()

# (optional) deallocate all sub-array resources
subarray.deallocate()

# (optional) send the telescope to STANDBY
telescope.standby()