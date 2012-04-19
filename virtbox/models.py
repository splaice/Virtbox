# -*- coding: utf-8 -*-
"""
This module contains the primary objects that power virtbox.

:copyright: (c) 2012 by Sean Plaice
:license: ISC, see LICENSE for more details.
"""

import envoy
from .errors import (VirtboxError, VirtboxManageError, VirtboxCommandError,
    VirtboxCommandNotImplemented)
from .utils import (parse_list_vms, parse_list_ostypes, parse_createvm,
        parse_showvminfo, parse_createhd, parse_unregistervm,
        parse_showhdinfo, parse_closemedium, parse_modifyvm)

HD_FORMATS = ('VDI', 'VMDK', 'VHD', 'RAW')
HD_VARIANTS = ('Standard', 'Fixed', 'Split2G', 'Stream', 'ESX')
MEDIUM_TYPES = ('disk', 'dvd', 'floppy')


class Manage(object):
    cmd = 'VBoxManage'

    @classmethod
    def _run_cmd(cls, cmd):
        r = envoy.run(cmd)
        if r.status_code:
            raise VirtboxCommandError(status_code=r.status_code, cmd=cmd,
                    stdout=r.std_out, stderr=r.std_err)

        return (r.std_out, r.std_err)

    @classmethod
    def createvm(cls, name=None, ostype=None, register=True, basefolder=None,
            uuid=None):
        _cmd = '%s createvm' % cls.cmd
        if name:
            _cmd = '%s --name %s' % (_cmd, name)

        if ostype:
            _cmd = '%s --ostype %s' % (_cmd, ostype)

        if basefolder:
            _cmd = '%s --basefolder %s' % (_cmd, basefolder)

        if uuid:
            _cmd = '%s --uuid %s' % (_cmd, uuid)

        if register:
            _cmd = '%s --register' % _cmd
        else:
            raise VirtboxManageError(
                    reason='register as False is currently unsupported.')

        stdout, stderr = cls._run_cmd(_cmd)
        return parse_createvm(stdout)

    @classmethod
    def registervm(cls, filename=None):
        raise VirtboxCommandNotImplemented(reason="not needed at this time")

    @classmethod
    def unregistervm(cls, name=None, uuid=None, delete=True):
        _cmd = '%s unregistervm' % cls.cmd

        if uuid:
            _cmd = '%s %s' % (_cmd, uuid)
        elif name:
            _cmd = '%s %s' % (_cmd, name)

        if delete:
            _cmd = '%s --delete' % _cmd

        stdout, stderr = cls._run_cmd(_cmd)
        return parse_unregistervm(stdout)

    @classmethod
    def showvminfo(cls, name=None, uuid=None, log=False):
        _cmd = '%s showvminfo --machinereadable --details' % cls.cmd

        if uuid:
            _cmd = '%s %s' % (_cmd, uuid)
        elif name:
            _cmd = '%s %s' % (_cmd, name)
        else:
            raise VirtboxManageError(reason="name or uuid argument required")

        stdout, stderr = cls._run_cmd(_cmd)
        return parse_showvminfo(stdout)

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
        _cmd = '%s modifyvm' % cls.cmd

        if uuid:
            _cmd = '%s %s' % (_cmd, uuid)
        elif name:
            _cmd = '%s %s' % (_cmd, name)

        if new_name:
            _cmd = '%s --name %s' % (_cmd, new_name)

        stdout, stderr = cls._run_cmd(_cmd)
        return parse_modifyvm(stdout)

    @classmethod
    def createhd(cls, filename=None, size=None, sizebytes=None, format=None,
            variant=None):
        _cmd = '%s createhd' % cls.cmd

        if filename:
            _cmd = '%s --filename %s' % (_cmd, filename)

        if sizebytes:
            _cmd = '%s --sizebytes %s' % (_cmd, sizebytes)
        elif size:
            _cmd = '%s --size %s' % (_cmd, size)

        if format:
            if format not in HD_FORMATS:
                raise VirtboxManageError(reason='unsupported format provided')
            _cmd = '%s --format %s' % (_cmd, format)

        if variant:
            if variant not in HD_VARIANTS:
                raise VirtboxManageError(reason='unsupported variant provided')
            _cmd = '%s --variant %s' % (_cmd, variant)

        stdout, stderr = cls._run_cmd(_cmd)
        return parse_createhd(stdout)

    @classmethod
    def showhdinfo(cls, uuid=None, filename=None):
        _cmd = '%s showhdinfo' % cls.cmd

        if uuid:
            _cmd = '%s %s' % (_cmd, uuid)
        elif filename:
            _cmd = '%s %s' % (_cmd, filename)

        stdout, stderr = cls._run_cmd(_cmd)
        return parse_showhdinfo(stdout)

    @classmethod
    def closemedium(cls, medium_type=None, uuid=None, filename=None,
            delete=False):
        _cmd = '%s closemedium' % cls.cmd

        if medium_type:
            if medium_type not in MEDIUM_TYPES:
                raise VirtboxManageError(reason='unsupported medium provided')
            _cmd = '%s %s' % (_cmd, medium_type)

        if uuid:
            _cmd = '%s %s' % (_cmd, uuid)
        elif filename:
            _cmd = '%s %s' % (_cmd, filename)

        if delete:
            _cmd = '%s --delete' % _cmd

        stdout, stderr = cls._run_cmd(_cmd)
        return parse_closemedium(stdout)

    @classmethod
    def _list(cls, arg):
        _cmd = '%s list %s' % (cls.cmd, arg)
        r = envoy.run(_cmd)
        if r.status_code:
            raise VirtboxError()
        else:
            return r.std_out

    @classmethod
    def list_vms(cls):
        return(parse_list_vms(cls._list('vms')))

    @classmethod
    def list_ostypes(cls):
        return(parse_list_ostypes(cls._list('ostypes')))
