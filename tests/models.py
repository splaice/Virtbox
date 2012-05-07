# -*- coding: utf-8 -*-
"""
This module contains the unit tests for the models module.

:copyright: (c) 2012 by Sean Plaice
:license: ISC, see LICENSE for more details.
"""

import os
import logging
import testify
import uuid
import time

from virtbox.models import Manage
from virtbox.utils import (id_generator, generate_vm, delete_vm, generate_hd,
        delete_hd, generate_ctl, delete_ctl)


# setup module level logger
logger = logging.getLogger(__name__)


class ManageVersionTestCase(testify.TestCase):
    def test_version(self):
        out = Manage.version()
        testify.assert_equal(bool(out['version']), True)


class ManageListVMSTestCase(testify.TestCase):
    @testify.setup
    def setup_vm(self):
        self.vms = []
        self.vms.append(generate_vm())

    @testify.teardown
    def cleanup_vm(self):
        Manage.unregistervm(name=self.vms[0]['name'], delete=True)

    def test_list_vms(self):
        vms = Manage.list_vms()
        testify.assert_equal(vms[0]['name'], self.vms[0]['name'],
                'name mismatch')
        vm_uuid = uuid.UUID('{%s}' % vms[0]['uuid'])
        testify.assert_equal(type(vm_uuid), type(uuid.uuid4()), 'no uuid set')


class ManageListVMSManyTestCase(testify.TestCase):
    @testify.setup
    def setup_vm(self):
        self.vm0 = generate_vm()
        self.vm1 = generate_vm()
        self.vm2 = generate_vm()

    @testify.teardown
    def cleanup_vm(self):
        delete_vm(**self.vm0)
        delete_vm(**self.vm1)
        delete_vm(**self.vm2)

    def test_list_vms(self):
        vms = Manage.list_vms()
        testify.assert_equal(vms[0]['name'], self.vm0['name'],
                'name mismatch')
        testify.assert_equal(vms[1]['name'], self.vm1['name'],
                'name mismatch')
        testify.assert_equal(vms[2]['name'], self.vm2['name'],
                'name mismatch')


class ManageListRunningVMSTestCase(testify.TestCase):
    @testify.setup
    def setup(self):
        self.vm0 = generate_vm()
        self.running_uuid0 = Manage.startvm(vm_uuid=self.vm0['uuid'],
                start_type='headless')
        time.sleep(5)

    @testify.teardown
    def cleanup_vm(self):
        Manage.controlvm(vm_uuid=self.vm0['uuid'], action='poweroff')
        time.sleep(5)
        delete_vm(**self.vm0)

    def test_list_runningvms(self):
        vms = Manage.list_runningvms()
        testify.assert_equal(vms[0]['name'], self.vm0['name'],
                'name mismatch')


class ManageListManyRunningVMSTestCase(testify.TestCase):
    @testify.setup
    def setup(self):
        self.vm0 = generate_vm()
        self.running_uuid0 = Manage.startvm(vm_uuid=self.vm0['uuid'],
                start_type='headless')
        self.vm1 = generate_vm()
        self.running_uuid1 = Manage.startvm(vm_uuid=self.vm1['uuid'],
                start_type='headless')
        self.vm2 = generate_vm()
        self.running_uuid2 = Manage.startvm(vm_uuid=self.vm2['uuid'],
                start_type='headless')
        time.sleep(5)

    @testify.teardown
    def cleanup_vm(self):
        Manage.controlvm(vm_uuid=self.vm0['uuid'], action='poweroff')
        Manage.controlvm(vm_uuid=self.vm1['uuid'], action='poweroff')
        Manage.controlvm(vm_uuid=self.vm2['uuid'], action='poweroff')
        time.sleep(5)
        delete_vm(**self.vm0)
        delete_vm(**self.vm1)
        delete_vm(**self.vm2)

    def test_list_runningvms(self):
        vms = Manage.list_runningvms()
        testify.assert_equal(vms[0]['name'], self.vm0['name'],
                'name mismatch')
        testify.assert_equal(vms[1]['name'], self.vm1['name'],
                'name mismatch')
        testify.assert_equal(vms[2]['name'], self.vm2['name'],
                'name mismatch')


class ManageListOSTypesTestCase(testify.TestCase):
    def test_list_ostypes(self):
        ostypes = Manage.list_ostypes()
        testify.assert_equal(ostypes[0]['os_desc'], 'Other/Unknown')
        testify.assert_equal(ostypes[0]['os_type'], 'Other')


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


class ManageUnregisterTestCase(testify.TestCase):
    @testify.setup
    def setup_unregistervm(self):
        self.vm = generate_vm()

    def test_unregistervm_by_name(self):
        out = Manage.unregistervm(name=self.vm['name'], delete=True)
        testify.assert_equal(out, '', 'returned non-empty string')

    def test_unregistervm_by_uuid(self):
        out = Manage.unregistervm(uuid=self.vm['uuid'], delete=True)
        testify.assert_equal(out, '', 'returned non-empty string')


class ManageCreateVMTestCase(testify.TestCase):
    @testify.setup
    def setup_vm_info(self):
        self.vm_name = id_generator()
        self.vm_ostype = 'Linux'
        self.vm_uuid = str(uuid.uuid4())

    @testify.teardown
    def cleanup_createvm(self):
        delete_vm(name=self.vm_name)

    def test_createvm(self):
        vm_info = Manage.createvm(name=self.vm_name, ostype=self.vm_ostype)
        testify.assert_equal(vm_info['name'], self.vm_name, 'name mismatch')
        testify.assert_equal(bool(vm_info['file_path']), True,
                'no file_path set')
        vm_uuid = uuid.UUID('{%s}' % vm_info['uuid'])
        testify.assert_equal(type(vm_uuid), type(uuid.uuid4()), 'no uuid set')

    def test_createvm_no_ostype(self):
        vm_info = Manage.createvm(name=self.vm_name)
        testify.assert_equal(vm_info['name'], self.vm_name, 'name mismatch')
        testify.assert_equal(bool(vm_info['file_path']), True,
                'no file_path set')
        vm_uuid = uuid.UUID('{%s}' % vm_info['uuid'])
        testify.assert_equal(type(vm_uuid), type(uuid.uuid4()), 'no uuid set')

    def test_createvm_with_basefolder(self):
        vm_info = Manage.createvm(name=self.vm_name, basefolder='test')
        testify.assert_equal(vm_info['name'], self.vm_name, 'name mismatch')
        testify.assert_equal(bool(vm_info['file_path']), True,
                'no file_path set')
        vm_uuid = uuid.UUID('{%s}' % vm_info['uuid'])
        testify.assert_equal(type(vm_uuid), type(uuid.uuid4()), 'no uuid set')

    def test_createvm_with_uuid(self):
        vm_info = Manage.createvm(name=self.vm_name, uuid=self.vm_uuid)
        testify.assert_equal(vm_info['name'], self.vm_name, 'name mismatch')
        testify.assert_equal(vm_info['uuid'], self.vm_uuid, 'uuid mismatch')
        vm_uuid = uuid.UUID('{%s}' % vm_info['uuid'])
        testify.assert_equal(type(vm_uuid), type(uuid.uuid4()), 'no uuid set')


class ManageModifyVMTestCase(testify.TestCase):
    """ Incomplete in the sense that I don't want to write tests for every
        option at this point.
    """
    @testify.setup
    def setup_createvm(self):
        self.vm_name = 'foo'
        self.new_name = 'bar'
        self.vm = generate_vm(name=self.vm_name)

    @testify.teardown
    def destroy_vm(self):
        delete_vm(**self.vm)

    def test_modifyvm_new_name_by_name(self):
        testify.assert_equal(self.vm_name, self.vm['name'])

        Manage.modifyvm(vm_name=self.vm['name'], name=self.new_name)
        vm_info = Manage.showvminfo(uuid=self.vm['uuid'])

        testify.assert_equal(self.new_name, vm_info['name'])

    def test_modifyvm_new_name_by_uuid(self):
        testify.assert_equal(self.vm_name, self.vm['name'])

        Manage.modifyvm(vm_uuid=self.vm['uuid'], name=self.new_name)
        vm_info = Manage.showvminfo(uuid=self.vm['uuid'])

        testify.assert_equal(self.new_name, vm_info['name'])

    def test_modifyvm_adjust_memory_by_uuid(self):
        memory = "128"
        testify.assert_equal(self.vm_name, self.vm['name'])

        Manage.modifyvm(vm_uuid=self.vm['uuid'], memory=memory)
        vm_info = Manage.showvminfo(uuid=self.vm['uuid'])

        testify.assert_equal(memory, vm_info['memory'])

    def test_modifyvm_basic_configuration(self):
        memory = "256"
        rtcuseutc = "on"
        nic1 = "hostonly"
        nictype1 = "Am79C973"
        hostonlyadapter1 = "vboxnet0"

        testify.assert_equal(self.vm_name, self.vm['name'])
        Manage.modifyvm(vm_uuid=self.vm['uuid'], memory=memory,
                rtcuseutc=rtcuseutc, nic1=nic1, nictype1=nictype1,
                hostonlyadapter1=hostonlyadapter1)
        vm_info = Manage.showvminfo(uuid=self.vm['uuid'])

        testify.assert_equal(memory, vm_info['memory'])
        testify.assert_equal(rtcuseutc, vm_info['rtcuseutc'])
        testify.assert_equal(nic1, vm_info['nic1'])
        testify.assert_equal(hostonlyadapter1, vm_info['hostonlyadapter1'])


class ManageStartVMTestCase(testify.TestCase):
    @testify.setup
    def setup(self):
        self.vm = generate_vm()
        self.hdd = generate_hd()
        self.memory = "256"
        self.rtcuseutc = "on"
        Manage.modifyvm(vm_uuid=self.vm['uuid'], memory=self.memory,
                rtcuseutc=self.rtcuseutc)

    def test_start_and_stop_vm(self):
        result = Manage.startvm(vm_name=self.vm['uuid'], start_type='headless')
        testify.assert_equal(self.vm['uuid'], result['uuid'])
        # this looks hacky but waiting on these operations finishing will
        # be handled in the biz logic at a higher level
        time.sleep(5)
        Manage.controlvm(vm_uuid=self.vm['uuid'], action='poweroff')
        time.sleep(5)

    @testify.teardown
    def teardown(self):
        delete_hd(**self.hdd)
        delete_vm(**self.vm)
        #Manage.controlvm(vm_uuid=self.vm['uuid'], action='poweroff')


class ManageCloseMediumTestCase(testify.TestCase):
    @testify.setup
    def setup(self):
        self.vm = generate_vm()
        self.hdd = generate_hd()

    @testify.teardown
    def teardown(self):
        delete_hd(**self.hdd)
        delete_vm(**self.vm)

#    def test_closemedium_disk_by_filename(self):
#        out = Manage.closemedium(medium_type='disk',
#                filename=self.hdd['filename'], delete=True)
#        print out


class ManageStorageAttachTestCase(testify.TestCase):
    @testify.setup
    def create_vm(self):
        self.vm = generate_vm()
        self.hdd = generate_hd()
        self.ctl = generate_ctl(vmname=self.vm['name'])

    @testify.teardown
    def cleanup_createvm(self):
        delete_ctl(**self.ctl)
        delete_hd(**self.hdd)
        delete_vm(**self.vm)

    def test_storage_attach_by_name(self):
        out = Manage.storageattach(vmname=self.vm['name'],
                name=self.ctl['name'], port='0', device='0',
                storage_type='hdd', medium=self.hdd['filename'])
        testify.assert_equal(out, '')

    def test_storage_attach_by_uuid(self):
        out = Manage.storageattach(uuid=self.vm['uuid'],
                name=self.ctl['name'], port='0', device='0',
                storage_type='hdd', medium=self.hdd['filename'])
        testify.assert_equal(out, '')


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


class ManageShowHDInfoTestCase(testify.TestCase):
    @testify.setup
    def create_hd(self):
        self.hdd = generate_hd()

    @testify.teardown
    def destory_hdd(self):
        delete_hd(**self.hdd)

    def test_showhdinfo_by_filename(self):
        hd_info = Manage.showhdinfo(filename=self.hdd['filename'])
        logical_size = '%s MBytes' % self.hdd['size']
        testify.assert_equal(hd_info['logical_size'], logical_size,
                'logical size mismatch')
        testify.assert_equal(hd_info['location'], self.hdd['filename'],
                'filename/location mismatch')
        testify.assert_equal(hd_info['storage_format'], self.hdd['hd_format'],
                'storage format mismatch')


class ManageCreateHDTestCase(testify.TestCase):
    @testify.setup
    def setup_hd_info(self):
        self.hd_size = '128'
        self.hd_format = 'VDI'
        self.hd_variant = 'Standard'
        self.hd_filename = '/tmp/test.vdi'

    @testify.teardown
    def destory_hdd(self):
        delete_hd(filename=self.hd_filename)

    def test_createhd(self):
        hd_info = Manage.createhd(filename=self.hd_filename, size=self.hd_size,
                hd_format=self.hd_format, variant=self.hd_variant)
        # TODO: remove once we figure out why we get a bad uuid returned
        try:
            hd_uuid = uuid.UUID('{%s}' % hd_info['uuid'])
        except:
            logger.error('fucked up uuid? %r' % hd_info)
            raise
        testify.assert_equal(type(hd_uuid), type(uuid.uuid4()), 'no uuid set')
        testify.assert_equal(os.path.exists(self.hd_filename), True,
                'created file does not exist')
