import csv
import sys

import oet.domain as domain

scan_sequence_file = sys.argv[1]

subarray = domain.SubArray(1)

print('Reading scan sequence from {}'.format(scan_sequence_file))
with open(scan_sequence_file, 'r') as csv_file:

    for row in csv.reader(csv_file, delimiter=','):
        exported_cdm, scan_duration = row

        print('Configuring sub-array {} using CDM from {}'.format(subarray.id, exported_cdm))
        subarray.configure_from_file(exported_cdm)

        print('Scanning for {} seconds'.format(scan_duration))
        # subarray.scan(scan_duration)
