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
        parse_showvminfo, parse_createhd, parse_unregistervm, parse_showhdinfo,
        parse_closemedium)

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
