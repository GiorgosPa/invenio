# -*- coding: utf-8 -*-
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
from invenio.bibrecord import record_add_field, record_xml_output, record_delete_field
from invenio.bibcheck_plugins import remove_empty_fields


def check_record(record):
    """ Bibcheck plugin to remove duplicate fields from records """
    fields = []
    for position, value in record.iterfields(['%%%%%_','%%%%%%']):
        if (position[0], value) not in fields:
            fields.append((position[0], value))
        else:
            message = 'remove duplicate subfield: %s with value: %s ' % (position, value)            
            print message
            record.delete_field(position, message)
            tag = position[0][:3]
    if record.amended:
        remove_empty_fields.remove_empty_tags(record)
