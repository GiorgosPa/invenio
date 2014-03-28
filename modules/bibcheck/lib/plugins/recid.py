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
from invenio.bibcheck_plugins import regexp
from invenio.search_engine import record_exists

def check_record(record):
    """ Checks the record on the fields 
        773__0, 999C50 and 785__w the value
        of those fields must contain 1-7 digits
        and a record with that recid must exist. """
    regexps = {
        '773__0' : '^\d{1,7}$',
        '999C50' : '^\d{1,7}$',
        '785__w' : '^\d{1,7}$'
    }
    regexp.check_record(record, regexps)
    #check if record exists
    if record.valid:
        for position, value in record.iterfields(['773__0', '999C50', '785__w']):
            recid = int(value)
            if record_exists(recid) <= 0:
                message = 'Field %s there is no record with record id: %s' % (position[0], recid)
                record.set_invalid(message)
