telescope = SKAMid()
telescope.start_up()

subarray = SubArray(1)
subarray.allocate(ResourceAllocation(dishes=[Dish(1), Dish(2)]))

polaris = SubArrayConfiguration(SkyCoord.from_name('polaris'), 'polaris', receiver_band=1)
subarray.configure(polaris)
