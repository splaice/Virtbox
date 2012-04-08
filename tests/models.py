# -*- coding: utf-8 -*-
"""
This module contains the unit tests for the models module.

:copyright: (c) 2012 by Sean Plaice
:license: ISC, see LICENSE for more details.
"""

import testify
import uuid as pyuuid
from virtbox.models import Manage
from virtbox.errors import VirtboxCommandError, VirtboxManageError


class ManageCreateTestCase(testify.TestCase):
    @testify.setup
    def setup_vm_info(self):
        self.vm_name = 'foobar'
        self.vm_ostype = 'Linux'
        self.vm_str_uuid = 'cd9ceb52-3852-40c0-8937-2c782b48b6ed'
        self.vm_uuid = pyuuid.uuid4()

    @testify.teardown
    def cleanup_create_vm(self):
        Manage.unregister_vm(name=self.vm_name, delete=True)

    def test_create_vm(self):
        vm_info = Manage.create_vm(name=self.vm_name, ostype=self.vm_ostype)
        testify.assert_equal(vm_info['name'], self.vm_name, 'name mismatch')
        testify.assert_gt(len(vm_info['file_path']), 0, 'no file_path set')
        testify.assert_gt(len(vm_info['uuid']), 0, 'no uuid set')

    def test_create_vm_no_ostype(self):
        vm_info = Manage.create_vm(name=self.vm_name)
        testify.assert_equal(vm_info['name'], self.vm_name, 'name mismatch')
        testify.assert_gt(len(vm_info['file_path']), 0, 'no file_path set')
        testify.assert_gt(len(vm_info['uuid']), 0, 'no uuid set')

    def test_create_vm_with_basefolder(self):
        vm_info = Manage.create_vm(name=self.vm_name, basefolder='test')
        testify.assert_equal(vm_info['name'], self.vm_name, 'name mismatch')
        testify.assert_gt(len(vm_info['file_path']), 0, 'no file_path set')
        testify.assert_gt(len(vm_info['uuid']), 0, 'no uuid set')

    def test_create_vm_with_uuid(self):
        testify.assert_raises(VirtboxManageError, Manage.create_vm,
                name=self.vm_name, uuid=self.vm_str_uuid)
        vm_info = Manage.create_vm(name=self.vm_name, uuid=self.vm_uuid)
        testify.assert_equal(vm_info['name'], self.vm_name, 'name mismatch')
        testify.assert_equal(vm_info['uuid'], str(self.vm_uuid),
                'uuid mismatch')
        testify.assert_gt(len(vm_info['file_path']), 0, 'no file_path set')


class ManageUnregisterTestCase(testify.TestCase):
    @testify.setup
    def setup_unregister_vm(self):
        self.vm_name = 'foobarz'
        self.vm_ostype = 'Linux'
        self.vm_info = Manage.create_vm(name=self.vm_name,
                ostype=self.vm_ostype)

    def test_unregister_vm_by_name(self):
        vm_info = Manage.unregister_vm(name=self.vm_name, delete=True)
        testify.assert_equal(vm_info, True, 'returned False')

    def test_unregister_vm_by_uuid(self):
        vm_info = Manage.unregister_vm(uuid=self.vm_info['uuid'], delete=True)
        testify.assert_equal(vm_info, True, 'returned False')

class ManageListVMS(testify.TestCase):
    @testify.setup
    def setup_vm(self):
        self.ostype = 'Linux'
        self.vm0_name = 'foo'
        self.vm0_info = Manage.create_vm(name=self.vm0_name,
                ostype=self.ostype)

    @testify.teardown
    def cleanup_vm(self):
        Manage.unregister_vm(name=self.vm0_name, delete=True)

    def test_list_vms(self):
        vm_info = Manage.list_vms()[0]
        testify.assert_equal(vm_info['name'], self.vm0_name, 'name mismatch')
        testify.assert_gt(len(vm_info['uuid']), 0, 'no uuid set')

class ManageListVMSMany(testify.TestCase):
    @testify.setup
    def setup_vm(self):
        self.ostype = 'Linux'
        self.vm0_name = 'foo'
        self.vm0_info = Manage.create_vm(name=self.vm0_name,
                ostype=self.ostype)
        self.vm1_name = 'bar'
        self.vm1_info = Manage.create_vm(name=self.vm1_name,
                ostype=self.ostype)
        self.vm2_name = 'foe'
        self.vm2_info = Manage.create_vm(name=self.vm2_name,
                ostype=self.ostype)

    @testify.teardown
    def cleanup_vm(self):
        Manage.unregister_vm(name=self.vm0_name, delete=True)
        Manage.unregister_vm(name=self.vm1_name, delete=True)
        Manage.unregister_vm(name=self.vm2_name, delete=True)

    def test_list_vms(self):
        vm_info0 = Manage.list_vms()[0]
        testify.assert_equal(vm_info0['name'], self.vm0_name, 'name mismatch')
        testify.assert_gt(len(vm_info0['uuid']), 0, 'no uuid set')

        vm_info1 = Manage.list_vms()[1]
        testify.assert_equal(vm_info1['name'], self.vm1_name, 'name mismatch')
        testify.assert_gt(len(vm_info1['uuid']), 0, 'no uuid set')

        vm_info2 = Manage.list_vms()[2]
        testify.assert_equal(vm_info2['name'], self.vm2_name, 'name mismatch')
        testify.assert_gt(len(vm_info2['uuid']), 0, 'no uuid set')

class ManageListOsTypes(testify.TestCase):
    """Incomplete
    """
