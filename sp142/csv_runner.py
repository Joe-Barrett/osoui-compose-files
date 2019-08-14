"""
This file runs an 'observation' by loading Configuration Data Model
instances from a file and using them to configure a Sub-Array.

This script assumes the telescope is in standby and that all
resources are unallocated.
"""
import csv
import sys

import oet.domain as domain

if len(sys.argv) != 2:
    print('Usage: csv_runner <name of CSV file>')
    sys.exit(0)

scan_sequence_file = sys.argv[1]

print('Starting telescope (setting DISH master devices to online)')
telescope = domain.SKAMid()
telescope.start_up()

print('Allocating two dishes to sub-array #1')
subarray = domain.SubArray(1)
allocation = domain.ResourceAllocation(dishes=[domain.Dish(1), domain.Dish(2)])
subarray.allocate(allocation)

print('Reading scan sequence from {}'.format(scan_sequence_file))
with open(scan_sequence_file, 'r') as csv_file:

    for row in csv.reader(csv_file, delimiter=','):
        exported_cdm, scan_duration = row

        print('Configuring sub-array {} using CDM from {}'.format(subarray.id, exported_cdm))
        subarray.configure_from_file(exported_cdm)

        print('Scanning for {} seconds'.format(scan_duration))
        print('### NO-OP AS SubArrayNode.Scan() IS NOT IMPLEMENTED YET ###')
        # subarray.scan(scan_duration)
