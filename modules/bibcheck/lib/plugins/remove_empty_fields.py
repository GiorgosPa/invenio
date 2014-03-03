#!/usr/bin/env python

##
## This file is part of Invenio.
## Copyright (C) 2014 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

from invenio.bibcheck_task import AmendableRecord
from invenio.bibrecord import record_xml_output, record_delete_field


def check_record(record):
    """ Bibcheck plugin to remove empty fields from records """
    remove_empty_subfields(record)
    remove_empty_tags(record)


def remove_empty_subfields(record):
    """ removes subfields with no value """
    for position, value in record.iterfield('%%%%%%'):
        if not value:
            message = 'remove empty subfield: ' + position
            record.delete_field(position, message)
            remove_empty_subfields(record)


def remove_empty_tags(record):
    """ removes tags with no subfields and no value """
    tags = record.keys()
    for position, dummy in record.iterfields(['%%%%%%', '%%%%%_']):
        tag = position[0][:3]
        if tag in tags:
            tags.remove(tag)

    for tag in tags:
        record_delete_field(record, tag)
        message = 'removed empty tag: ' + tag
        record.set_amended(message)


#testing
if __name__ == '__main__':
    record = {
        '001': [([], ' ', ' ', '1', 7)],
        '245': [([('a', ''), ('b', '')], ' ', ' ', '', 7)],
        '100': [([('a', 'Bella, Ludovica Aperio'), ('n', ''), ('a', '')], ' ', ' ', '', 7), ([('a', 'Galtieri, Angela Barbaro')], ' ', ' ', '', 8)],
        '700': [([('a', 'Bella, Ludovica Aperio'), ('c', '')], ' ', ' ', '', 7), ([('a', 'Galtieri, Angela Barbaro')], ' ', ' ', '', 8)]
    }
    print record_xml_output(record)
    record = AmendableRecord(record)
    record.holdingpen = True
    record.rule = {}
    record.rule["name"] = 'ATLAS'
    record.rule["holdingpen"] = 'True'
    check_record(record)
    print record_xml_output(record)
