# -*- coding: utf-8 -*-
"""
This module contains the primary objects that power virtbox.

:copyright: (c) 2012 by Sean Plaice
:license: ISC, see LICENSE for more details.
"""

import envoy
from .errors import (VirtboxError, VirtboxManageError, VirtboxCommandError,
    VirtboxCommandNotImplemented)
from .utils import parse_list_vms, parse_list_ostypes, parse_createvm


class Manage(object):
    cmd = 'VBoxManage'

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

        r = envoy.run(_cmd)
        if r.status_code:
            raise VirtboxCommandError(status_code=r.status_code, cmd=_cmd,
                    stdout=r.std_out, stderr=r.std_err)

        return parse_createvm(r.std_out)

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

        r = envoy.run(_cmd)
        if r.status_code:
            raise VirtboxError()

        return True

    @classmethod
    def showvminfo(cls, name=None, uuid=None, log=False):
        pass

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
