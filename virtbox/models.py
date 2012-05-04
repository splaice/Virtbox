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
            cpus=None, plugcpu=None, unplugcpu=None, cpuhotplug=None,
            cpuexecutioncap=None, rtcuseutc=None, monitorcount=None,
            accelerate3d=None, accelerate2dvideo=None, firmware=None,
            chipset=None, bioslogofadein=None, bioslogofadeout=None,
            bioslogodisplaytime=None, bioslogoimagepath=None,
            biosbootmenu=None, biossystemtimeoffset=None, biospxedebug=None,
            boot1=None, boot2=None, boot3=None, boot4=None, nic1=None,
            nic2=None, nic3=None, nic4=None, nic5=None, nic6=None, nic7=None,
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
            nicgenericdrv7=None, natsettings1=None, natsettings2=None,
            natsettings3=None, natsettings4=None, natsettings5=None,
            natsettings6=None, natsettings7=None, natpf1=None, natpf2=None,
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

        if ostype:
            cmd = '%s --ostype %s' % (cmd, ostype)

        if memory:
            cmd = '%s --memory %s' % (cmd, memory)

        if pagefusion:
            cmd = '%s --pagefusion %s' % (cmd, pagefusion)

        if vram:
            cmd = '%s --vram %s' % (cmd, vram)

        if acpi:
            cmd = '%s --acpi %s' % (cmd, acpi)

        if pciattach:
            cmd = '%s --pciattach %s' % (cmd, pciattach)

        if pcidetach:
            cmd = '%s --pcidetach %s' % (cmd, pcidetach)

        if ioapic:
            cmd = '%s --ioapic' % (cmd, ioapic)

        if pae:
            cmd = '%s --pae %s' % (cmd, pae)

        if hpet:
            cmd = '%s --hpet %s' % (cmd, hpet)

        if hwvirtex:
            cmd = '%s --hwvirtex %s' % (cmd, hwvirtex)

        if hwvirtexexcl:
            cmd = '%s --hwvirtexexcl %s' % (cmd, hwvirtexexcl)

        if nestedpaging:
            cmd = '%s --nestedpaging %s' % (cmd, nestedpaging)

        if largepages:
            cmd = '%s --largepages %s' % (cmd, largepages)

        if vtxvpid:
            cmd = '%s --vtxvpid %s' % (cmd, vtxvpid)

        if synthcpu:
            cmd = '%s --synthcpu %s' % (cmd, synthcpu)

        if cpuidset:
            cmd = '%s --cpuidset %s' % (cmd, cpuidset)

        if cpuidremove:
            cmd = '%s --cpuidremove %s' % (cmd, cpuidremove)

        if cpuidremoveall:
            cmd = '%s --cpuidremoveall %s' % (cmd, cpuidremoveall)

        if hardwareuuid:
            cmd = '%s --hardwareuuid %s' % (cmd, hardwareuuid)

        if cpus:
            cmd = '%s --cpus %s' % (cmd, cpus)

        if cpuhotplug:
            cmd = '%s --cpuhotplug %s' % (cmd, cpuhotplug)

        if plugcpu:
            cmd = '%s --plugcpu %s' % (cmd, plugcpu)

        if unplugcpu:
            cmd = '%s --unplugcpu %s' % (cmd, unplugcpu)

        if cpuexecutioncap:
            cmd = '%s --cpuexecutioncap %s' % (cmd, cpuexecutioncap)

        if rtcuseutc:
            cmd = '%s --rtcuseutc %s' % (cmd, rtcuseutc)

        if monitorcount:
            cmd = '%s --monitorcount %s' % (cmd, monitorcount)

        if accelerate3d:
            cmd = '%s --accelerate3d %s' % (cmd, accelerate3d)

        if accelerate2dvideo:
            cmd = '%s --accelerate2dvideo %s' % (cmd, accelerate2dvideo)

        if firmware:
            cmd = '%s --firmware %s' % (cmd, firmware)

        if chipset:
            cmd = '%s --chipset %s' % (cmd, chipset)

        if bioslogofadein:
            cmd = '%s --bioslogofadein %s' % (cmd, bioslogofadein)

        if bioslogofadeout:
            cmd = '%s --bioslogofadeout %s' % (cmd, bioslogofadeout)

        if bioslogodisplaytime:
            cmd = '%s --bioslogodisplaytime %s' % (cmd, bioslogodisplaytime)

        if bioslogoimagepath:
            cmd = '%s --bioslogoimagepath %s' % (cmd, bioslogoimagepath)

        if biosbootmenu:
            cmd = '%s --biosbootmenu %s' % (cmd, biosbootmenu)

        if biossystemtimeoffset:
            cmd = '%s --biossystemtimeoffset %s' % (cmd, biossystemtimeoffset)

        if biospxedebug:
            cmd = '%s --biospxedebug %s' % (cmd, biospxedebug)

        if boot1:
            cmd = '%s --boot1 %s' (cmd, boot1)

        if boot2:
            cmd = '%s --boot2 %s' (cmd, boot2)

        if boot3:
            cmd = '%s --boot3 %s' (cmd, boot3)

        if boot4:
            cmd = '%s --boot4 %s' (cmd, boot4)

        if nic1:
            cmd = '%s --nic1 %s' (cmd, nic1)

        if nic2:
            cmd = '%s --nic2 %s' (cmd, nic2)

        if nic3:
            cmd = '%s --nic3 %s' (cmd, nic3)

        if nic4:
            cmd = '%s --nic4 %s' (cmd, nic4)

        if nic5:
            cmd = '%s --nic5 %s' (cmd, nic5)

        if nic6:
            cmd = '%s --nic6 %s' (cmd, nic6)

        if nic7:
            cmd = '%s --nic7 %s' (cmd, nic7)

        if nictype1:
            cmd = '%s --nictype1 %s' (cmd, nictype1)

        if nictype2:
            cmd = '%s --nictype2 %s' (cmd, nictype2)

        if nictype3:
            cmd = '%s --nictype3 %s' (cmd, nictype3)

        if nictype4:
            cmd = '%s --nictype4 %s' (cmd, nictype4)

        if nictype5:
            cmd = '%s --nictype5 %s' (cmd, nictype5)

        if nictype6:
            cmd = '%s --nictype6 %s' (cmd, nictype6)

        if nictype7:
            cmd = '%s --nictype7 %s' (cmd, nictype7)

        if cabelconnected1:
            cmd = '%s --cabelconnected1 %s' (cmd, cabelconnected1)

        if cabelconnected2:
            cmd = '%s --cabelconnected2 %s' (cmd, cabelconnected2)

        if cabelconnected3:
            cmd = '%s --cabelconnected3 %s' (cmd, cabelconnected3)

        if cabelconnected4:
            cmd = '%s --cabelconnected4 %s' (cmd, cabelconnected4)

        if cabelconnected5:
            cmd = '%s --cabelconnected5 %s' (cmd, cabelconnected5)

        if cabelconnected6:
            cmd = '%s --cabelconnected6 %s' (cmd, cabelconnected6)

        if cabelconnected7:
            cmd = '%s --cabelconnected7 %s' (cmd, cabelconnected7)

        if nictrace1:
            cmd = '%s --nictrace1 %s' (cmd, nictrace1)

        if nictrace2:
            cmd = '%s --nictrace2 %s' (cmd, nictrace2)

        if nictrace3:
            cmd = '%s --nictrace3 %s' (cmd, nictrace3)

        if nictrace4:
            cmd = '%s --nictrace4 %s' (cmd, nictrace4)

        if nictrace5:
            cmd = '%s --nictrace5 %s' (cmd, nictrace5)

        if nictrace6:
            cmd = '%s --nictrace6 %s' (cmd, nictrace6)

        if nictrace7:
            cmd = '%s --nictrace7 %s' (cmd, nictrace7)

        if nictracefile1:
            cmd = '%s --nictracefile1 %s' (cmd, nictracefile1)

        if nictracefile2:
            cmd = '%s --nictracefile2 %s' (cmd, nictracefile2)

        if nictracefile3:
            cmd = '%s --nictracefile3 %s' (cmd, nictracefile3)

        if nictracefile4:
            cmd = '%s --nictracefile4 %s' (cmd, nictracefile4)

        if nictracefile5:
            cmd = '%s --nictracefile5 %s' (cmd, nictracefile5)

        if nictracefile6:
            cmd = '%s --nictracefile6 %s' (cmd, nictracefile6)

        if nictracefile7:
            cmd = '%s --nictracefile7 %s' (cmd, nictracefile7)

        if nicproperty1:
            cmd = '%s --nicproperty1 %s' (cmd, nicproperty1)

        if nicproperty2:
            cmd = '%s --nicproperty2 %s' (cmd, nicproperty2)

        if nicproperty3:
            cmd = '%s --nicproperty3 %s' (cmd, nicproperty3)

        if nicproperty4:
            cmd = '%s --nicproperty4 %s' (cmd, nicproperty4)

        if nicproperty5:
            cmd = '%s --nicproperty5 %s' (cmd, nicproperty5)

        if nicproperty6:
            cmd = '%s --nicproperty6 %s' (cmd, nicproperty6)

        if nicproperty7:
            cmd = '%s --nicproperty7 %s' (cmd, nicproperty7)

        if nicspeed1:
            cmd = '%s --nicspeed1 %s' (cmd, nicspeed1)

        if nicspeed2:
            cmd = '%s --nicspeed2 %s' (cmd, nicspeed2)

        if nicspeed3:
            cmd = '%s --nicspeed3 %s' (cmd, nicspeed3)

        if nicspeed4:
            cmd = '%s --nicspeed4 %s' (cmd, nicspeed4)

        if nicspeed5:
            cmd = '%s --nicspeed5 %s' (cmd, nicspeed5)

        if nicspeed6:
            cmd = '%s --nicspeed6 %s' (cmd, nicspeed6)

        if nicspeed7:
            cmd = '%s --nicspeed7 %s' (cmd, nicspeed7)

        if nicbootprio1:
            cmd = '%s --nicbootprio1 %s' (cmd, nicbootprio1)

        if nicbootprio2:
            cmd = '%s --nicbootprio2 %s' (cmd, nicbootprio2)

        if nicbootprio3:
            cmd = '%s --nicbootprio3 %s' (cmd, nicbootprio3)

        if nicbootprio4:
            cmd = '%s --nicbootprio4 %s' (cmd, nicbootprio4)

        if nicbootprio5:
            cmd = '%s --nicbootprio5 %s' (cmd, nicbootprio5)

        if nicbootprio6:
            cmd = '%s --nicbootprio6 %s' (cmd, nicbootprio6)

        if nicbootprio7:
            cmd = '%s --nicbootprio7 %s' (cmd, nicbootprio7)

        if nicpromisc1:
            cmd = '%s --nicpromisc1 %s' (cmd, nicpromisc1)

        if nicpromisc2:
            cmd = '%s --nicpromisc2 %s' (cmd, nicpromisc2)

        if nicpromisc3:
            cmd = '%s --nicpromisc3 %s' (cmd, nicpromisc3)

        if nicpromisc4:
            cmd = '%s --nicpromisc4 %s' (cmd, nicpromisc4)

        if nicpromisc5:
            cmd = '%s --nicpromisc5 %s' (cmd, nicpromisc5)

        if nicpromisc6:
            cmd = '%s --nicpromisc6 %s' (cmd, nicpromisc6)

        if nicpromisc7:
            cmd = '%s --nicpromisc7 %s' (cmd, nicpromisc7)

        if nicbandwidthgroup1:
            cmd = '%s --nicbandwidthgroup1 %s' (cmd, nicbandwidthgroup1)

        if nicbandwidthgroup2:
            cmd = '%s --nicbandwidthgroup2 %s' (cmd, nicbandwidthgroup2)

        if nicbandwidthgroup3:
            cmd = '%s --nicbandwidthgroup3 %s' (cmd, nicbandwidthgroup3)

        if nicbandwidthgroup4:
            cmd = '%s --nicbandwidthgroup4 %s' (cmd, nicbandwidthgroup4)

        if nicbandwidthgroup5:
            cmd = '%s --nicbandwidthgroup5 %s' (cmd, nicbandwidthgroup5)

        if nicbandwidthgroup6:
            cmd = '%s --nicbandwidthgroup6 %s' (cmd, nicbandwidthgroup6)

        if nicbandwidthgroup7:
            cmd = '%s --nicbandwidthgroup7 %s' (cmd, nicbandwidthgroup7)

        if bridgeadapter1:
            cmd = '%s --bridgeadapter1 %s' (cmd, bridgeadapter1)

        if bridgeadapter2:
            cmd = '%s --bridgeadapter2 %s' (cmd, bridgeadapter2)

        if bridgeadapter3:
            cmd = '%s --bridgeadapter3 %s' (cmd, bridgeadapter3)

        if bridgeadapter4:
            cmd = '%s --bridgeadapter4 %s' (cmd, bridgeadapter4)

        if bridgeadapter5:
            cmd = '%s --bridgeadapter5 %s' (cmd, bridgeadapter5)

        if bridgeadapter6:
            cmd = '%s --bridgeadapter6 %s' (cmd, bridgeadapter6)

        if bridgeadapter7:
            cmd = '%s --bridgeadapter7 %s' (cmd, bridgeadapter7)

        if hostonlyadapter1:
            cmd = '%s --hostonlyadapter1 %s' (cmd, hostonlyadapter1)

        if hostonlyadapter2:
            cmd = '%s --hostonlyadapter2 %s' (cmd, hostonlyadapter2)

        if hostonlyadapter3:
            cmd = '%s --hostonlyadapter3 %s' (cmd, hostonlyadapter3)

        if hostonlyadapter4:
            cmd = '%s --hostonlyadapter4 %s' (cmd, hostonlyadapter4)

        if hostonlyadapter5:
            cmd = '%s --hostonlyadapter5 %s' (cmd, hostonlyadapter5)

        if hostonlyadapter6:
            cmd = '%s --hostonlyadapter6 %s' (cmd, hostonlyadapter6)

        if hostonlyadapter7:
            cmd = '%s --hostonlyadapter7 %s' (cmd, hostonlyadapter7)

        if intnet1:
            cmd = '%s --intnet1 %s' (cmd, intnet1)

        if intnet2:
            cmd = '%s --intnet2 %s' (cmd, intnet2)

        if intnet3:
            cmd = '%s --intnet3 %s' (cmd, intnet3)

        if intnet4:
            cmd = '%s --intnet4 %s' (cmd, intnet4)

        if intnet5:
            cmd = '%s --intnet5 %s' (cmd, intnet5)

        if intnet6:
            cmd = '%s --intnet6 %s' (cmd, intnet6)

        if intnet7:
            cmd = '%s --intnet7 %s' (cmd, intnet7)

        if natnet1:
            cmd = '%s --natnet1 %s' (cmd, natnet1)

        if natnet2:
            cmd = '%s --natnet2 %s' (cmd, natnet2)

        if natnet3:
            cmd = '%s --natnet3 %s' (cmd, natnet3)

        if natnet4:
            cmd = '%s --natnet4 %s' (cmd, natnet4)

        if natnet5:
            cmd = '%s --natnet5 %s' (cmd, natnet5)

        if natnet6:
            cmd = '%s --natnet6 %s' (cmd, natnet6)

        if natnet7:
            cmd = '%s --natnet7 %s' (cmd, natnet7)

        if nicgenericdrv1:
            cmd = '%s --nicgenericdrv1 %s' (cmd, nicgenericdrv1)

        if nicgenericdrv2:
            cmd = '%s --nicgenericdrv2 %s' (cmd, nicgenericdrv2)

        if nicgenericdrv3:
            cmd = '%s --nicgenericdrv3 %s' (cmd, nicgenericdrv3)

        if nicgenericdrv4:
            cmd = '%s --nicgenericdrv4 %s' (cmd, nicgenericdrv4)

        if nicgenericdrv5:
            cmd = '%s --nicgenericdrv5 %s' (cmd, nicgenericdrv5)

        if nicgenericdrv6:
            cmd = '%s --nicgenericdrv6 %s' (cmd, nicgenericdrv6)

        if nicgenericdrv7:
            cmd = '%s --nicgenericdrv7 %s' (cmd, nicgenericdrv7)

        if natsettings1:
            cmd = '%s --natsettings1 %s' (cmd, natsettings1)

        if natsettings2:
            cmd = '%s --natsettings2 %s' (cmd, natsettings2)

        if natsettings3:
            cmd = '%s --natsettings3 %s' (cmd, natsettings3)

        if natsettings4:
            cmd = '%s --natsettings4 %s' (cmd, natsettings4)

        if natsettings5:
            cmd = '%s --natsettings5 %s' (cmd, natsettings5)

        if natsettings6:
            cmd = '%s --natsettings6 %s' (cmd, natsettings6)

        if natsettings7:
            cmd = '%s --natsettings7 %s' (cmd, natsettings7)

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
