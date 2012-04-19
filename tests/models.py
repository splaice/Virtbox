# -*- coding: utf-8 -*-
"""
This module contains the unit tests for the models module.

:copyright: (c) 2012 by Sean Plaice
:license: ISC, see LICENSE for more details.
"""

import testify
import os
from virtbox.models import Manage


class ManageCreateTestCase(testify.TestCase):
    @testify.setup
    def setup_vm_info(self):
        self.vm_name = 'foobar'
        self.vm_ostype = 'Linux'
        self.vm_uuid = 'cd9ceb52-3852-40c0-8937-2c782b48b6ed'

    @testify.teardown
    def cleanup_createvm(self):
        Manage.unregistervm(name=self.vm_name, delete=True)

    def test_createvm(self):
        vm_info = Manage.createvm(name=self.vm_name, ostype=self.vm_ostype)
        testify.assert_equal(vm_info['name'], self.vm_name, 'name mismatch')
        testify.assert_gt(len(vm_info['file_path']), 0, 'no file_path set')
        testify.assert_gt(len(vm_info['uuid']), 0, 'no uuid set')

    def test_createvm_no_ostype(self):
        vm_info = Manage.createvm(name=self.vm_name)
        testify.assert_equal(vm_info['name'], self.vm_name, 'name mismatch')
        testify.assert_gt(len(vm_info['file_path']), 0, 'no file_path set')
        testify.assert_gt(len(vm_info['uuid']), 0, 'no uuid set')

    def test_createvm_with_basefolder(self):
        vm_info = Manage.createvm(name=self.vm_name, basefolder='test')
        testify.assert_equal(vm_info['name'], self.vm_name, 'name mismatch')
        testify.assert_gt(len(vm_info['file_path']), 0, 'no file_path set')
        testify.assert_gt(len(vm_info['uuid']), 0, 'no uuid set')

    def test_createvm_with_uuid(self):
        vm_info = Manage.createvm(name=self.vm_name, uuid=self.vm_uuid)
        testify.assert_equal(vm_info['name'], self.vm_name, 'name mismatch')
        testify.assert_equal(vm_info['uuid'], self.vm_uuid, 'uuid mismatch')
        testify.assert_gt(len(vm_info['file_path']), 0, 'no file_path set')


class ManageUnregisterTestCase(testify.TestCase):
    @testify.setup
    def setup_unregistervm(self):
        self.vm_name = 'foobarz'
        self.vm_ostype = 'Linux'
        self.vm_info = Manage.createvm(name=self.vm_name,
                ostype=self.vm_ostype)

    def test_unregistervm_by_name(self):
        vm_info = Manage.unregistervm(name=self.vm_name, delete=True)
        testify.assert_equal(vm_info, '', 'returned non-empty string')

    def test_unregistervm_by_uuid(self):
        vm_info = Manage.unregistervm(uuid=self.vm_info['uuid'], delete=True)
        testify.assert_equal(vm_info, '', 'returned non-empty string')


class ManageListVMSTestCase(testify.TestCase):
    @testify.setup
    def setup_vm(self):
        self.ostype = 'Linux'
        self.vm0_name = 'foo'
        self.vm0_info = Manage.createvm(name=self.vm0_name,
                ostype=self.ostype)

    @testify.teardown
    def cleanup_vm(self):
        Manage.unregistervm(name=self.vm0_name, delete=True)

    def test_list_vms(self):
        vm_info = Manage.list_vms()[0]
        testify.assert_equal(vm_info['name'], self.vm0_name, 'name mismatch')
        testify.assert_gt(len(vm_info['uuid']), 0, 'no uuid set')


class ManageListVMSManyTestCase(testify.TestCase):
    @testify.setup
    def setup_vm(self):
        self.ostype = 'Linux'
        self.vm0_name = 'foo'
        self.vm0_info = Manage.createvm(name=self.vm0_name,
                ostype=self.ostype)
        self.vm1_name = 'bar'
        self.vm1_info = Manage.createvm(name=self.vm1_name,
                ostype=self.ostype)
        self.vm2_name = 'foe'
        self.vm2_info = Manage.createvm(name=self.vm2_name,
                ostype=self.ostype)

    @testify.teardown
    def cleanup_vm(self):
        Manage.unregistervm(name=self.vm0_name, delete=True)
        Manage.unregistervm(name=self.vm1_name, delete=True)
        Manage.unregistervm(name=self.vm2_name, delete=True)

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


class ManageShowVMInfoTestCase(testify.TestCase):
    @testify.setup
    def create_vm(self):
        self.vm_info = Manage.createvm(name='taco')

    @testify.teardown
    def destroy_vm(self):
        Manage.unregistervm(name=self.vm_info['name'], delete=True)

    def test_showvminfo_by_name(self):
        vm_details = Manage.showvminfo(name=self.vm_info['name'])
        testify.assert_equal(vm_details['name'], self.vm_info['name'])
        testify.assert_equal(vm_details['uuid'], self.vm_info['uuid'])

    def test_showvminfo_by_uuid(self):
        vm_details = Manage.showvminfo(name=self.vm_info['uuid'])
        testify.assert_equal(vm_details['name'], self.vm_info['name'])
        testify.assert_equal(vm_details['uuid'], self.vm_info['uuid'])


class ManageCreateStorageCTLTestCase(testify.TestCase):
    @testify.setup
    def create_vm(self):
        self.vm_info = Manage.createvm(name='taco')

    @testify.teardown
    def destroy_vm(self):
        Manage.unregistervm(name=self.vm_info['name'], delete=True)

    def test_create_storagectl_by_name(self):
        out = Manage.storagectl_add(vmname=self.vm_info['name'],
                name='primary', ctl_type='scsi', controller='LSILogic')
        testify.assert_equal(out, '')
        out = Manage.storagectl_remove(vmname=self.vm_info['name'],
                name='primary')
        testify.assert_equal(out, '')

    def test_create_storagectl_by_uuid(self):
        out = Manage.storagectl_add(vmname=self.vm_info['uuid'],
                name='primary', ctl_type='scsi', controller='LSILogic')
        testify.assert_equal(out, '')
        out = Manage.storagectl_remove(vmname=self.vm_info['uuid'],
                name='primary')
        testify.assert_equal(out, '')


class ManageCreateHDTestCase(testify.TestCase):
    @testify.setup
    def setup_hd_info(self):
        self.hd_size = '128'
        self.hd_format = 'VDI'
        self.hd_variant = 'Standard'
        self.hd_filename = '/tmp/test.vdi'

    @testify.teardown
    def destory_hdd(self):
        os.remove(self.hd_filename)

    def test_createhd(self):
        hd_info = Manage.createhd(filename=self.hd_filename, size=self.hd_size,
                format=self.hd_format, variant=self.hd_variant)
        testify.assert_equal(len(hd_info['uuid']), 36, 'uuid len is off')
        testify.assert_equal(os.path.exists(self.hd_filename), True,
                'created file does not exist')


class ManageShowHDInfoTestCase(testify.TestCase):
    @testify.setup
    def create_hd(self):
        self.hd_size = '128'
        self.hd_format = 'VDI'
        self.hd_variant = 'Standard'
        self.hd_filename = '/tmp/test.vdi'
        self.hd_info = Manage.createhd(filename=self.hd_filename,
                size=self.hd_size, format=self.hd_format,
                variant=self.hd_variant)

    @testify.teardown
    def destory_hdd(self):
        os.remove(self.hd_filename)

    def test_showhdinfo_by_filename(self):
        hd_info = Manage.showhdinfo(uuid=self.hd_filename)
        logical_size = '%s MBytes' % self.hd_size
        testify.assert_equal(hd_info['logical_size'], logical_size,
                'logical size mismatch')
        testify.assert_equal(hd_info['location'], self.hd_filename,
                'filename/location mismatch')
        testify.assert_equal(hd_info['storage_format'], self.hd_format,
                'storage format mismatch')


#class ManageCloseMediumTestCase(testify.TestCase):
#    @testify.setup
#    def create_hd(self):
#        self.hd_size = '128'
#        self.hd_format = 'VDI'
#        self.hd_variant = 'Standard'
#        self.hd_filename = '/tmp/test.vdi'
#        self.hd_info = Manage.createhd(filename=self.hd_filename,
#                size=self.hd_size, format=self.hd_format,
#                variant=self.hd_variant)
#
#    def test_closemedium_disk_by_uuid_with_delete(self):
#       out = Manage.closemedium(medium_type='disk', uuid=self.hd_info['uuid'],
#                delete=True)
#        print out


class ManageListOsTypes(testify.TestCase):
    """Incomplete
    """


class ManageModifyVMTestCase(testify.TestCase):
    """ Incomplete in the sense that I don't want to write tests for every
        option at this point.
    """
    @testify.setup
    def setup_createvm(self):
        self.vm_name = 'foobarz'
        self.vm_new_name = 'foobart'
        self.vm_ostype = 'Linux'
        self.vm_info = Manage.createvm(name=self.vm_name,
                ostype=self.vm_ostype)

    def test_modifyvm_new_name_by_name(self):
        testify.assert_equal(self.vm_name, self.vm_info['name'])

        Manage.modifyvm(name=self.vm_name, new_name=self.vm_new_name)
        vm_info = Manage.showvminfo(uuid=self.vm_info['uuid'])

        testify.assert_equal(self.vm_new_name, vm_info['name'])

    def test_modifyvm_new_name_by_uuid(self):
        testify.assert_equal(self.vm_name, self.vm_info['name'])

        Manage.modifyvm(uuid=self.vm_info['uuid'], new_name=self.vm_new_name)
        vm_info = Manage.showvminfo(uuid=self.vm_info['uuid'])

        testify.assert_equal(self.vm_new_name, vm_info['name'])

    @testify.teardown
    def destroy_vm(self):
        Manage.unregistervm(name=self.vm_info['uuid'], delete=True)
