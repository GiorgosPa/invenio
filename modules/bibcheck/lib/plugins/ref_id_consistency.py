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

	for field_instance in record_get_field_instances(record,'999','C','5'):
		# recid_set = set()
		# subfields = field_get_subfield_instances(field_instance)
		# for code, value in subfields:
		# 	field_to_search = dictionary.get(code)
		# 	if field_to_search and value:
		# 		recid = find_rec_by_field_and_value(field_to_search,value)
		# 		if recid:
		# 			recid_set.add(recid)
		# 	if code == '0' and value:
		# 		recid_set.add(value)
		recid_set = find_inspire_id_from_reference(field_instance)
		if len(recid_set) > 1:
			record.set_invalid("Several records referenced by reference %s" % ''.join(field_get_subfield_values(field_instance, 'x')))
		# codes = field_get_subfield_codes(field_instance)
		# codes=[code for code in codes if code in ['a','i','r','s','0']]


def find_inspire_id_from_reference(field_instance):
	""" reference field instance"""
	dictionary = {
		'a' : '0247_a',
		'i' : '020__a',
		'r' : '037__a',
		's' : '773__p'
	}
	recid_set = set()
	subfields = field_get_subfield_instances(field_instance)
	for code, value in subfields:
		field_to_search = dictionary.get(code)
		if field_to_search and value:
			recid = find_rec_by_field_and_value(field_to_search,value)
			if recid:
				recid_set.add(recid)
		if code == '0' and value:
			recid_set.add(value)
	return recid_set


def find_rec_by_field_and_value(field_to_search,value): # todo add collection as param?
	pattern = "%s:%s" % (field_to_search, value)
	result = perform_request_search(p=pattern, of="intbitset", cc="HEP")
	if result:
		return result[0]
	return ""