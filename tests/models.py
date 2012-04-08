import testify
from virtbox.models import Manage


class ManageCreateTestCase(testify.TestCase):
    @testify.setup
    def setup_vm_info(self):
        self.vm_name = 'foobar'
        self.vm_ostype = 'Linux'

    @testify.teardown
    def cleanup_create_vm(self):
        Manage.unregister_vm(name=self.vm_name, delete=True)

    def test_create_vm(self):
        vm_info = Manage.create_vm(name=self.vm_name, ostype=self.vm_ostype)
        testify.assert_equal(vm_info['name'], self.vm_name, 'name mismatch')
        testify.assert_gt(len(vm_info['file_path']), 0, 'no file_path set')
        testify.assert_gt(len(vm_info['uuid']), 0, 'no uuid set')


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
