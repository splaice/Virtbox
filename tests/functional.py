# -*- coding: utf-8 -*-
"""
This module contains the functional tests for using virbox.

:copyright: (c) 2012 by Sean Plaice
:license: ISC, see LICENSE for more details.
"""

import logging
import testify

from virtbox.models import Manage
from virtbox.utils import (
        generate_vm,
        generate_hd,
        generate_ctl,
        #delete_vm,
        #delete_hd,
        #delete_ctl
)


# setup module level logger
logger = logging.getLogger(__name__)


class VirtboxFunctionalTestCase(testify.TestCase):
    @testify.setup
    def setup(self):
        self.vm = generate_vm()
        self.hdd = generate_hd()
        self.ctl = generate_ctl(vmname=self.vm['name'])
        self.memory = "1024"
        self.rtcuseutc = "on"
        self.iso_path = '/tmp/fedora.iso'
        Manage.modifyvm(vm_uuid=self.vm['uuid'], memory=self.memory,
                rtcuseutc=self.rtcuseutc)
        Manage.storageattach(vmname=self.vm['name'],
                name=self.ctl['name'], port='0', device='0',
                storage_type='hdd', medium=self.hdd['filename'])
        Manage.storageattach(vmname=self.vm['name'],
                name=self.ctl['name'], port='1', device='0',
                storage_type='dvddrive', medium=self.iso_path)

    #@testify.teardown
    #def teardown(self):
    #    delete_ctl(**self.ctl)
    #    delete_hd(**self.hdd)
    #    delete_vm(**self.vm)

    def test_start_and_stop_vm(self):
        result = Manage.startvm(vm_name=self.vm['uuid'], start_type='gui')
        testify.assert_equal(self.vm['uuid'], result['uuid'])
        # this looks hacky but waiting on these operations finishing will
        # be handled in the biz logic at a higher level
        #Manage.controlvm(vm_uuid=self.vm['uuid'], action='poweroff')
