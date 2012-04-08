# -*- coding: utf-8 -*-
"""
This module contains the primary objects that power Bootstrap.

:copyright: (c) 2012 by Firstname Lastname.
:license: ISC, see LICENSE for more details.
"""

import envoy
from .errors import VirtboxError
from .utils import parse_list_vms, parse_list_ostypes, parse_create_vm


class Manage(object):
    cmd = 'VBoxManage'

    @classmethod
    def create_vm(cls, name=None, ostype=None, register=True, basefolder=None,
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

        r = envoy.run(_cmd)
        if r.status_code:
            raise VirtboxError()

        return parse_create_vm(r.std_out)

    @classmethod
    def unregister_vm(cls, name=None, uuid=None, delete=True):
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
