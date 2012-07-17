# -*- coding: utf-8 -*-

"""
virtbox.utils
~~~~~~~~

This module provides utility functions that are used within Bootstrap
that are also useful for external consumption.

:copyright: (c) 2012 by Sean Plaice.
:license: ISC, see LICENSE for more details.

"""

import os
import logging
import string
import random
import envoy

from .errors import CommandError


# setup module level logger
LOGGER = logging.getLogger(__name__)


def run_cmd(cmd):
    """
    """
    res = envoy.run(cmd)
    if res.status_code:
        LOGGER.error('cmd: %s status_code: %d stdout: %s stderr: %s' %
            (cmd, res.status_code, res.std_out.replace('\n', ' '),
                res.std_err.replace('\n', ' ')))
        raise CommandError(status_code=res.status_code, cmd=cmd,
            stdout=res.std_out, stderr=res.std_err)

    LOGGER.debug('cmd: %s status_code: %d stdout: %s stderr: %s' % (cmd,
        res.status_code, res.std_out.replace('\n', ' '),
        res.std_err.replace('\n', ' ')))
    return (res.std_out, res.std_err)


def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    """
    """
    return ''.join(random.choice(chars) for x in range(size))


def generate_vm(**kwargs):
    """
    """
    from .manage import createvm
    data = {'name': id_generator(7),
            'ostype': 'Linux'}
    data.update(kwargs)
    return createvm(**data)


def delete_vm(**kwargs):
    """
    """
    from .manage import unregistervm
    data = {'delete': True}
    data.update(kwargs)
    # prune unneeded / unexpected kwargs
    if data.get('file_path'):
        del data['file_path']
    return unregistervm(**data)


def generate_hd(**kwargs):
    """
    """
    from .manage import createhd
    filename = '%s.vdi' % id_generator()
    data = {'size': '128',
            'hd_format': 'VDI',
            'variant': 'Standard',
            'filename': os.path.join('/tmp', filename)}
    data.update(kwargs)
    createhd(**data)
    return data


def delete_hd(**kwargs):
    """
    """
    data = {}
    data.update(kwargs)
    os.remove(data['filename'])


def generate_ctl(**kwargs):
    """
    """
    from .manage import storagectl_add
    data = {'name': 'primary',
            'ctl_type': 'sata',
            'sataportcount': 2,
            'bootable': 'on'}
    data.update(kwargs)
    storagectl_add(**data)
    return data


def delete_ctl(**kwargs):
    """
    """
    from .manage import storagectl_remove
    data = {'name': 'primary'}
    data.update(kwargs)
    # prune unneeded / unexpected kwargs
    if data.get('controller'):
        del data['controller']
    if data.get('ctl_type'):
        del data['ctl_type']
    if data.get('sataportcount'):
        del data['sataportcount']
    if data.get('bootable'):
        del data['bootable']
    return storagectl_remove(**data)
