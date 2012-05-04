# -*- coding: utf-8 -*-
"""
This module contains the primary objects that power virtbox.

:copyright: (c) 2012 by Sean Plaice
:license: ISC, see LICENSE for more details.
"""

import logging

from .utils import run_cmd
from .errors import (VirtboxManageError, VirtboxCommandNotImplemented,
        VirtboxMissingArgument)
from .parsers import (parse_list_vms, parse_list_ostypes, parse_createvm,
        parse_showvminfo, parse_createhd, parse_unregistervm,
        parse_showhdinfo, parse_closemedium, parse_modifyvm,
        parse_storagectl_add, parse_storagectl_remove, parse_storageattach,
        parse_version)

VBOXMANAGE_CMD = 'VBoxManage'
HD_FORMATS = ('VDI', 'VMDK', 'VHD', 'RAW')
HD_VARIANTS = ('Standard', 'Fixed', 'Split2G', 'Stream', 'ESX')
MEDIUM_TYPES = ('disk', 'dvd', 'floppy')
STORAGECTL_TYPES = ('ide', 'sata', 'scsi', 'floppy', 'sas')
STORAGECTL_CONTROLLERS = ('LSILogic', 'LSILogicSAS', 'BusLogic', 'IntelAHCI',
    'PIIX3', 'PIIX4', 'ICH6', 'I82078')
STORAGE_TYPES = ('dvddrive', 'hdd', 'fdd')
STORAGE_MTYPES = ('normal', 'writethrough', 'immutable', 'shareable',
    'readonly', 'multiattach')


# setup module level logger
LOGGER = logging.getLogger(__name__)


class Manage(object):
    """
    """
    @classmethod
    def version(cls):
        """
        """
        cmd = '%s --version' % VBOXMANAGE_CMD

        stdout, stderr = run_cmd(cmd)
        return parse_version(stdout, stderr)

    @classmethod
    def list_vms(cls):
        """
        """
        cmd = '%s list vms' % VBOXMANAGE_CMD

        stdout, stderr = run_cmd(cmd)
        return parse_list_vms(stdout, stderr)

    @classmethod
    def list_runningvms(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def list_ostypes(cls):
        """
        """
        cmd = '%s list ostypes' % VBOXMANAGE_CMD

        stdout, stderr = run_cmd(cmd)
        return parse_list_ostypes(stdout, stderr)

    @classmethod
    def list_hostdvds(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def list_hostfloppies(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def list_bridgedifs(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def list_hostonlyifs(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def list_dhcpservers(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def list_hostinfo(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def list_hostcpuids(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def list_hddbackends(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def list_hdds(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def list_dvds(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def list_floppies(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def list_usbhost(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def list_usbfilters(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def list_systemproperties(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def list_extpacks(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def showvminfo(cls, name=None, uuid=None):
        """
        """
        cmd = '%s showvminfo --machinereadable --details' % VBOXMANAGE_CMD

        if uuid:
            cmd = '%s %s' % (cmd, uuid)
        elif name:
            cmd = '%s %s' % (cmd, name)
        else:
            raise VirtboxManageError(reason="name or uuid argument required")

        stdout, stderr = run_cmd(cmd)
        return parse_showvminfo(stdout, stderr)

    @classmethod
    def registervm(cls):
        """
        """
        raise VirtboxCommandNotImplemented(reason="not needed at this time")

    @classmethod
    def unregistervm(cls, name=None, uuid=None, delete=True):
        """
        """
        cmd = '%s unregistervm' % VBOXMANAGE_CMD

        if uuid:
            cmd = '%s %s' % (cmd, uuid)
        elif name:
            cmd = '%s %s' % (cmd, name)

        if delete:
            cmd = '%s --delete' % cmd

        stdout, stderr = run_cmd(cmd)
        return parse_unregistervm(stdout, stderr)

    @classmethod
    def createvm(cls, name=None, ostype=None, register=True, basefolder=None,
            uuid=None):
        """
        """
        cmd = '%s createvm' % VBOXMANAGE_CMD
        if name:
            cmd = '%s --name %s' % (cmd, name)

        if ostype:
            cmd = '%s --ostype %s' % (cmd, ostype)

        if basefolder:
            cmd = '%s --basefolder %s' % (cmd, basefolder)

        if uuid:
            cmd = '%s --uuid %s' % (cmd, uuid)

        if register:
            cmd = '%s --register' % cmd
        else:
            raise VirtboxManageError(
                    reason='register as False is currently unsupported.')

        stdout, stderr = run_cmd(cmd)
        return parse_createvm(stdout, stderr)

    @classmethod
    def modifyvm(cls, name=None, uuid=None, new_name=None, ostype=None,
            memory=None, pagefusion=None, vram=None, acpi=None,
            pciattach=None, pcidetach=None, ioapic=None, pae=None, hpet=None,
            hwvirtex=None, hwvirtexexcl=None, nestedpaging=None,
            largepages=None, vtxvpid=None, synthcpu=None, cpuidset=None,
            cpuidremove=None, cpuidremoveall=False, hardwareuuid=None,
            cpus=None, cpuhotplug=None, cpuexectioncap=None, rtcuseutc=None,
            monitorcount=None, acclerate3d=None, accelerate2dvideo=None,
            firmware=None, chipset=None, bioslogofadein=None,
            bioslogofadeout=None, bioslogodisplaytime=None,
            bioslogoimagepath=None, biosbootmenu=None,
            biossystemtimeoffset=None, biospxedebug=None, boot1=None,
            boot2=None, boot3=None, boot4=None, nic1=None, nic2=None,
            nic3=None, nic4=None, nic5=None, nic6=None, nic7=None,
            nictype1=None, nictype2=None, nictype3=None, nictype4=None,
            nictype5=None, nictype6=None, nictype7=None, cabelconnected1=None,
            cabelconnected2=None, cabelconnected3=None, cabelconnected4=None,
            cabelconnected5=None, cabelconnected6=None, cabelconnected7=None,
            nictrace1=None, nictrace2=None, nictrace3=None, nictrace4=None,
            nictrace5=None, nictrace6=None, nictrace7=None, nictracefile1=None,
            nictracefile2=None, nictracefile3=None, nictracefile4=None,
            nictracefile5=None, nictracefile6=None, nictracefile7=None,
            nicproperty1=None, nicproperty2=None, nicproperty3=None,
            nicproperty4=None, nicproperty5=None, nicproperty6=None,
            nicproperty7=None, nicspeed1=None, nicspeed2=None, nicspeed3=None,
            nicspeed4=None, nicspeed5=None, nicspeed6=None, nicspeed7=None,
            nicbootprio1=None, nicbootprio2=None, nicbootprio3=None,
            nicbootprio4=None, nicbootprio5=None, nicbootprio6=None,
            nicbootprio7=None, nicpromisc1=None, nicpromisc2=None,
            nicpromisc3=None, nicpromisc4=None, nicpromisc5=None,
            nicpromisc6=None, nicpromisc7=None,
            nicbandwidthgroup1=None, nicbandwidthgroup2=None,
            nicbandwidthgroup3=None, nicbandwidthgroup4=None,
            nicbandwidthgroup5=None, nicbandwidthgroup6=None,
            nicbandwidthgroup7=None, bridgeadapter1=None, bridgeadapter2=None,
            bridgeadapter3=None, bridgeadapter4=None, bridgeadapter5=None,
            bridgeadapter6=None, bridgeadapter7=None,
            hostonlyadapter1=None, hostonlyadapter2=None,
            hostonlyadapter3=None, hostonlyadapter4=None,
            hostonlyadapter5=None, hostonlyadapter6=None,
            hostonlyadapter7=None, intnet1=None, intnet2=None, intnet3=None,
            intnet4=None, intnet5=None, intnet6=None, intnet7=None,
            natnet1=None, natnet2=None, natnet3=None, natnet4=None,
            natnet5=None, natnet6=None, natnet7=None,
            nicgenericdrv1=None, nicgenericdrv2=None, nicgenericdrv3=None,
            nicgenericdrv4=None, nicgenericdrv5=None, nicgenericdrv6=None,
            nicgenericdrv7=None, netsettings1=None, netsettings2=None,
            netsettings3=None, netsettings4=None, netsettings5=None,
            netsettings6=None, netsettings7=None, natpf1=None, natpf2=None,
            natpf3=None, natpf4=None, natpf5=None, natpf6=None, natpf7=None,
            nattftpprefix1=None, nattftpprefix2=None, nattftpprefix3=None,
            nattftpprefix4=None, nattftpprefix5=None, nattftpprefix6=None,
            nattftpprefix7=None, nattftpfile1=None, nattftpfile2=None,
            nattftpfile3=None, nattftpfile4=None, nattftpfile5=None,
            nattftpfile6=None, nattftpfile7=None, nattftpserver1=None,
            nattftpserver2=None, nattftpserver3=None, nattftpserver4=None,
            nattftpserver5=None, nattftpserver6=None, nattftpserver7=None,
            natbindip1=None, natbindip2=None, natbindip3=None, natbindip4=None,
            natbindip5=None, natbindip6=None, natbindip7=None,
            natdnspassdomain1=None, natdnspassdomain2=None,
            natdnspassdomain3=None, natdnspassdomain4=None,
            natdnspassdomain5=None, natdnspassdomain6=None,
            natdnspassdomain7=None, natdnsproxy1=None, natdnsproxy2=None,
            natdnsproxy3=None, natdnsproxy4=None, natdnsproxy5=None,
            natdnsproxy6=None, natdnsproxy7=None, natdnshostresolver1=None,
            natdnshostresolver2=None, natdnshostresolver3=None,
            natdnshostresolver4=None, natdnshostresolver5=None,
            natdnshostresolver6=None, natdnshostresolver7=None,
            nataliasmode1=None, nataliasmode2=None, nataliasmode3=None,
            nataliasmode4=None, nataliasmode5=None, nataliasmode6=None,
            nataliasmode7=None, macaddress1=None, macaddress2=None,
            macaddress3=None, macaddress4=None, macaddress5=None,
            macaddress6=None, macaddress7=None, mouse=None, keyboard=None,
            uart1=None, uart2=None, uartmode1=None, uartmode2=None,
            guestmemoryballon=None, gueststatisticsinterval=None,
            audio=None, audiocontroller=None, clipboard=None, vrde=None,
            vrdeextpack=None, vrdeproperty=None, vrdeport=None,
            vrdeaddress=None, vrdeauthtype=None, vrdeauthlibrary=None,
            vrdemulticon=None, vrdereusecon=None, vrdevideochannel=None,
            vrdevideochannelquality=None, usb=None, usbehci=None,
            snapshotfolder=None, teleporter=None, teleporterport=None,
            teleporteraddress=None, teleporterpassword=None):
        """
        TODO: complete me
        """
        cmd = '%s modifyvm' % VBOXMANAGE_CMD

        if uuid:
            cmd = '%s %s' % (cmd, uuid)
        elif name:
            cmd = '%s %s' % (cmd, name)

        if new_name:
            cmd = '%s --name %s' % (cmd, new_name)

        stdout, stderr = run_cmd(cmd)
        return parse_modifyvm(stdout, stderr)

    @classmethod
    def clonevm(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def importvm(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def exportvm(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def startvm(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def controlvm(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def discardstate(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def adoptstate(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def snapshot(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def closemedium(cls, medium_type=None, uuid=None, filename=None,
            delete=False):
        """
        """
        cmd = '%s closemedium' % VBOXMANAGE_CMD

        if medium_type:
            if medium_type not in MEDIUM_TYPES:
                raise VirtboxManageError(reason='unsupported medium provided')
            cmd = '%s %s' % (cmd, medium_type)

        if uuid:
            cmd = '%s %s' % (cmd, uuid)
        elif filename:
            cmd = '%s %s' % (cmd, filename)

        if delete:
            cmd = '%s --delete' % cmd

        stdout, stderr = run_cmd(cmd)
        return parse_closemedium(stdout, stderr)

    @classmethod
    def storageattach(cls, uuid=None, vmname=None, name=None, port=None,
            device=None, storage_type=None, medium=None, mtype=None,
            comment=None, setuuid=None, setparentuuid=None, passthrough=None,
            tempeject=None, nonrotational=None, bandwidthgroup=None,
            forceunmount=False, server=None, target=None, tport=None, lun=None,
            encodedlun=None, username=None, password=None, intnet=None):
        """
        """
        cmd = '%s storageattach' % VBOXMANAGE_CMD

        if uuid:
            cmd = '%s %s' % (cmd, uuid)
        elif vmname:
            cmd = '%s %s' % (cmd, vmname)

        if name:
            cmd = '%s --storagectl %s' % (cmd, name)
        else:
            raise VirtboxMissingArgument("kwarg name is required.")

        if port:
            cmd = '%s --port %s' % (cmd, port)

        if device:
            cmd = '%s --device %s' % (cmd, device)

        if storage_type:
            if storage_type not in STORAGE_TYPES:
                raise VirtboxManageError(
                        reason='unsupported storage_type provided')

            cmd = '%s --type %s' % (cmd, storage_type)

        if medium:
            cmd = '%s --medium %s' % (cmd, medium)

        if mtype:
            if mtype not in STORAGE_MTYPES:
                raise VirtboxManageError(
                        reason='unsupported storage_type provided')

            cmd = '%s --mtype %s' % (cmd, type)

        if comment:
            cmd = '%s --comment %s' % (cmd, comment)

        if setuuid:
            cmd = '%s --setuuid %s' % (cmd, setuuid)

        if setparentuuid:
            cmd = '%s --setparentuuid %s' % (cmd, setparentuuid)

        if passthrough:
            cmd = '%s --passthrough %s' % (cmd, passthrough)

        if tempeject:
            cmd = '%s --tempeject %s' % (cmd, tempeject)

        if nonrotational:
            cmd = '%s --nonrotational %s' % (cmd, nonrotational)

        if bandwidthgroup:
            cmd = '%s --bandwidthgroup %s' % (cmd, bandwidthgroup)

        if forceunmount:
            cmd = '%s --forceunmount' % cmd

        if server:
            cmd = '%s --server %s' % (cmd, server)

        if target:
            cmd = '%s --target %s' % (cmd, target)

        if tport:
            cmd = '%s --tport %s' % (cmd, tport)

        if lun:
            cmd = '%s --lun %s' % (cmd, lun)

        if encodedlun:
            cmd = '%s --encodedlun %s' % (cmd, encodedlun)

        if username:
            cmd = '%s --username %s' % (cmd, username)

        if password:
            cmd = '%s --password %s' % (cmd, password)

        if intnet:
            cmd = '%s --intnet' % cmd

        stdout, stderr = run_cmd(cmd)
        return parse_storageattach(stdout, stderr)

    @classmethod
    def storagectl_add(cls, uuid=None, vmname=None, name=None, ctl_type=None,
            controller=None, sataideemulation1=None, sataideemulation2=None,
            sataideemulation3=None, sataideemulation4=None,  hostiocache=None,
            bootable=False):
        """
        """
        cmd = '%s storagectl' % VBOXMANAGE_CMD

        if uuid:
            cmd = '%s %s' % (cmd, uuid)
        elif vmname:
            cmd = '%s %s' % (cmd, vmname)

        if name:
            cmd = '%s --name %s' % (cmd, name)
        else:
            raise VirtboxMissingArgument("kwarg name is required.")

        if ctl_type:
            if ctl_type not in STORAGECTL_TYPES:
                raise VirtboxManageError(
                        reason='unsupported ctl_type provided')
            else:
                cmd = '%s --add %s' % (cmd, ctl_type)

        if controller:
            if controller not in STORAGECTL_CONTROLLERS:
                raise VirtboxManageError(
                        reason='unsupported controller ctl_type provided')
            else:
                cmd = '%s --controller %s' % (cmd, controller)

        if sataideemulation1:
            cmd = '%s --sataideemulation1 %d' % (cmd, sataideemulation1)

        if sataideemulation2:
            cmd = '%s --sataideemulation2 %d' % (cmd, sataideemulation2)

        if sataideemulation3:
            cmd = '%s --sataideemulation3 %d' % (cmd, sataideemulation3)

        if sataideemulation4:
            cmd = '%s --sataideemulation4 %d' % (cmd, sataideemulation4)

        if hostiocache:
            cmd = '%s --hostiocache %s' % (cmd, hostiocache)

        if bootable:
            cmd = '%s --bootable %s' % (cmd, bootable)

        stdout, stderr = run_cmd(cmd)
        return parse_storagectl_add(stdout, stderr)

    @classmethod
    def storagectl_remove(cls, uuid=None, vmname=None, name=None):
        """
        """
        cmd = '%s storagectl' % VBOXMANAGE_CMD

        if uuid:
            cmd = '%s %s' % (cmd, uuid)
        elif vmname:
            cmd = '%s %s' % (cmd, vmname)

        if name:
            cmd = '%s --name %s --remove' % (cmd, name)
        else:
            raise VirtboxMissingArgument("kwarg name is required.")

        stdout, stderr = run_cmd(cmd)
        return parse_storagectl_remove(stdout, stderr)

    @classmethod
    def bandwidthctl(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def showhdinfo(cls, uuid=None, filename=None):
        """
        """
        cmd = '%s showhdinfo' % VBOXMANAGE_CMD

        if uuid:
            cmd = '%s %s' % (cmd, uuid)
        elif filename:
            cmd = '%s %s' % (cmd, filename)

        stdout, stderr = run_cmd(cmd)
        return parse_showhdinfo(stdout, stderr)

    @classmethod
    def createhd(cls, filename=None, size=None, sizebytes=None, hd_format=None,
            variant=None):
        """
        """
        cmd = '%s createhd' % VBOXMANAGE_CMD

        if filename:
            cmd = '%s --filename %s' % (cmd, filename)

        if sizebytes:
            cmd = '%s --sizebytes %s' % (cmd, sizebytes)
        elif size:
            cmd = '%s --size %s' % (cmd, size)

        if hd_format:
            if hd_format not in HD_FORMATS:
                raise VirtboxManageError(reason='unsupported format provided')
            cmd = '%s --format %s' % (cmd, hd_format)

        if variant:
            if variant not in HD_VARIANTS:
                raise VirtboxManageError(reason='unsupported variant provided')
            cmd = '%s --variant %s' % (cmd, variant)

        stdout, stderr = run_cmd(cmd)
        return parse_createhd(stdout, stderr)

    @classmethod
    def modifyhd(cls):
        """
        """
        raise VirtboxCommandNotImplemented(reason="not needed at this time")

    @classmethod
    def clonehd(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def convertfromraw(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def getextradata(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def setextradata(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def setproperty(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def usbfilter(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def sharedfolder(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def guestproperty(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def guestcontrol(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def debugvm(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def metrics(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def hostonlyif(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def dhcpserver(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")

    @classmethod
    def extpack(cls):
        """
        TODO: implement me
        """
        raise VirtboxCommandNotImplemented(reason="not yet implemented")
