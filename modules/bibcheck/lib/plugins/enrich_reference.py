# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2013 CERN.
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

""" Bibcheck plugin to check the id consistency of references' fields """
from invenio.bibrecord import record_get_field_instances, field_get_subfield_instances, field_get_subfield_values
from invenio.websearch import perform_request_search
def check_record(record):
	# doi = '999C5a':'0247_a'
	# isbn = '999C5i' : '020__a'
	# prep_ref_reference to arxiv eprint  = '999C5r' : ''
	# journal_ref = '999C5' : '773__p'
	# inspire_id = '999C50' : ''
	dictionary = {
	'a' : '0247_a',
	'i' : '020__a',
	'r' : '037__a',
	's' : '773__p',
	}

	for field_instance in record_get_field_instances(record,'999','C','5'):
		codes = field_get_subfield_codes(field_instance)
		if 'p' and 's' in codes:
			referenced_record = retrieve_referenced_record(field_instance)
		subfields = field_get_subfield_instances(field_instance)
		for code, value in subfields:
			if dictionary.haskey(code):
				if referenced_record.not_contains(dictionary[code]) and record.contains(code):
					referenced_record.addfield(record[code])

def retrieve_referenced_record(field_instance): # todo add collection as param?
	subfields = field_get_subfield_instances(field_instance)
	for code, value in subfields:
		if code == '0' and value:
			return value
	return ''
