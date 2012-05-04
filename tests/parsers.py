# -*- coding: utf-8 -*-
"""
This module contains the unit tests for the parsers module.

:copyright: (c) 2012 by Sean Plaice
:license: ISC, see LICENSE for more details.
"""

import logging
import os
import codecs
import testify


from virtbox.parsers import parse_createhd, parse_list_ostypes


# setup module level logger
logger = logging.getLogger(__name__)


VBOXMANAGE_LIST_OSTYPES = os.path.join('parser_test_data',
    'vboxmanage_list_ostypes.txt')


class ParseCreateHDTestCase(testify.TestCase):
    def test_parse_createhd(self):
        txt = "Disk image created. UUID: e0bfd47f-5a29-4c5e-b325-79c4d032a02f"
        txt2 = "Disk image created. UUID: 00bfd47f-5a29-4c5e-b325-79c4d032a02f"
        out2 = parse_createhd(txt2, '')
        out = parse_createhd(txt, '')
        testify.assert_equal(out2['uuid'],
                '00bfd47f-5a29-4c5e-b325-79c4d032a02f')
        testify.assert_equal(out['uuid'],
                'e0bfd47f-5a29-4c5e-b325-79c4d032a02f')


class ParseListOSTypesTestCase(testify.TestCase):
    @testify.setup
    def setup(self):
        with codecs.open(VBOXMANAGE_LIST_OSTYPES, 'r', 'utf-8') as input:
            self.txt = input.read()

    def test_parse_ostypes_list(self):
        ostypes = parse_list_ostypes(self.txt, '')
        testify.assert_equal(ostypes[0]['os_desc'], 'Other/Unknown')
        testify.assert_equal(ostypes[0]['os_type'], 'Other')
