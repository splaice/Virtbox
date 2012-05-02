# -*- coding: utf-8 -*-
"""
This module contains the unit tests for the parsers module.

:copyright: (c) 2012 by Sean Plaice
:license: ISC, see LICENSE for more details.
"""

import logging
import testify


from virtbox.parsers import parse_createhd


# setup module level logger
logger = logging.getLogger(__name__)


class ParseCreateHDTestCase(testify.TestCase):
    def test_parse_createhd(self):
        txt = "Disk image created. UUID: e0bfd47f-5a29-4c5e-b325-79c4d032a02f"
        txt2 = "Disk image created. UUID: 00bfd47f-5a29-4c5e-b325-79c4d032a02f"
        out2 = parse_createhd(txt2)
        out = parse_createhd(txt)
        testify.assert_equal(out2['uuid'],
                '00bfd47f-5a29-4c5e-b325-79c4d032a02f')
        testify.assert_equal(out['uuid'],
                'e0bfd47f-5a29-4c5e-b325-79c4d032a02f')
