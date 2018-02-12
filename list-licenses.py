#!/usr/bin/env python

from __future__ import print_function
import pkg_resources
import csv
import sys
import os

if len(sys.argv) < 2:
    print("Pass the path to a requirements.txt file")
    sys.exit(1)

requirements_file = sys.argv[1]

if not os.path.isfile(requirements_file):
    print("Invalid file passed")
    sys.exit(2)

def get_pkg_license(pkgname):
    """
    Get the License from the packages metadata, or None if can't find it.
    """
    try:
        pkgs = pkg_resources.require(pkgname)
    except pkg_resources.RequirementParseError as e:
        print('WARNING: RequirementParseError happened when getting license for requirements line: "%s"' % pkgname, file=sys.stderr)
        return None
    try:
        pkg = pkgs[0]
    except IndexError as e:
        print('WARNING: could not get license for requirements line:  "%s"' % pkgname, file=sys.stderr)
        return None

    metadata_name = 'METADATA'
    license = ''
    home_page = ''
    if pkg.has_metadata(metadata_name):
        for line in pkg.get_metadata_lines(metadata_name):
            try:
                (k, v) = line.split(': ', 1)
                if k == "License":
                    license = v
                if k == 'Home-page':
                    home_page = v
            except:
                pass

    return {"license": license, "home_page": home_page}

csv_output = csv.writer(sys.stdout, delimiter='\t')
csv_output.writerow(['Library', 'URL', 'License'])

with open(requirements_file) as f:
    for line in f:
        name = line.split('==')[0]
        info = get_pkg_license(name)
        if info:
            csv_output.writerow([name, info['home_page'], info['license']])

sys.exit(0)
