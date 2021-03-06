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


from virtbox.parsers import parse_createhd, parse_list_ostypes, parse_startvm


# setup module level logger
logger = logging.getLogger(__name__)


VBOXMANAGE_LIST_OSTYPES = os.path.join('parser_test_data',
    'vboxmanage_list_ostypes.txt')
VBOXMANAGE_STARTVM = os.path.join('parser_test_data',
    'vboxmanage_startvm.txt')


class ParseListOSTypesTestCase(testify.TestCase):
    @testify.setup
    def setup(self):
        with codecs.open(VBOXMANAGE_LIST_OSTYPES, 'r', 'utf-8') as stdout:
            self.stdout = stdout.read()

        self.stderr = ''

    def test_parse_ostypes_list(self):
        ostypes = parse_list_ostypes(self.stdout, self.stderr)
        testify.assert_equal(ostypes[0]['os_desc'], 'Other/Unknown')
        testify.assert_equal(ostypes[0]['os_type'], 'Other')


class ParseStartVMTestCase(testify.TestCase):
    @testify.setup
    def setup(self):
        self.test_uuid = 'f4b0a749-820b-43c2-967e-a7a5f539cfd7'
        with codecs.open(VBOXMANAGE_STARTVM, 'r', 'utf-8') as stdout:
            self.stdout = stdout.read()

        self.stderr = ''

    def test_parse_startvm(self):
        result = parse_startvm(self.stdout, self.stderr)
        testify.assert_equal(self.test_uuid, result['uuid'])


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
