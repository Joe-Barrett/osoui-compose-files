"""
This file contains an example itango session that exercises the OET and TMC
functionality for SP-142.

To run these commands, start the integrated environment and connect to the
OET with:

  make ds-config
  make import_dashboards
  make mvp
  make oet
  docker attach oet

... and the commands at the command prompt.

"""

# start up the telescope, turning DISH master devices on
telescope = SKAMid()
telescope.start_up()

# Create a sub-array and allocate two dishes to it
subarray = SubArray(1)
allocation = ResourceAllocation(dishes=[Dish(1), Dish(2)])
subarray.allocate(allocation)

# Configure the sub-array to point at Polaris using RX band 1
polaris = SubArrayConfiguration(SkyCoord.from_name('polaris'), 'polaris', receiver_band='1')
subarray.configure(polaris)

# (optional) deallocate all sub-array resources
subarray.deallocate()

# (optional) send the telescope to STANDBY
telescope.standby()