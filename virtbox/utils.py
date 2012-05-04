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
logger = logging.getLogger(__name__)


def run_cmd(cmd):
    r = envoy.run(cmd)
    if r.status_code:
        logger.error('cmd: %s status_code: %d stdout: %s stderr: %s' %
            (cmd, r.status_code, r.std_out.replace('\n', ' '),
                r.std_err.replace('\n', ' ')))
        raise CommandError(status_code=r.status_code, cmd=cmd,
            stdout=r.std_out, stderr=r.std_err)

    logger.debug('cmd: %s status_code: %d stdout: %s stderr: %s' % (cmd,
        r.status_code, r.std_out.replace('\n', ' '),
        r.std_err.replace('\n', ' ')))
    return (r.std_out, r.std_err)


def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def generate_vm(**kwargs):
    from .models import Manage
    data = {'name': id_generator(7),
            'ostype': 'Linux'}
    data.update(kwargs)
    return Manage.createvm(**data)


def delete_vm(**kwargs):
    from .models import Manage
    data = {'delete': True}
    data.update(kwargs)
    # prune unneeded / unexpected kwargs
    if data.get('file_path'):
        del data['file_path']
    return Manage.unregistervm(**data)


def generate_hd(**kwargs):
    from .models import Manage
    filename = '%s.vdi' % id_generator()
    data = {'size': '128',
            'format': 'VDI',
            'variant': 'Standard',
            'filename': os.path.join('/tmp', filename)}
    data.update(kwargs)
    Manage.createhd(**data)
    return data


def delete_hd(**kwargs):
    data = {}
    data.update(kwargs)
    os.remove(data['filename'])


def generate_ctl(**kwargs):
    from .models import Manage
    data = {'name': 'primary',
            'ctl_type': 'scsi',
            'controller': 'LSILogic'}
    data.update(kwargs)
    Manage.storagectl_add(**data)
    return data


def delete_ctl(**kwargs):
    from .models import Manage
    data = {'name': 'primary'}
    data.update(kwargs)
    # prune unneeded / unexpected kwargs
    if data.get('controller'):
        del data['controller']
    if data.get('ctl_type'):
        del data['ctl_type']
    return Manage.storagectl_remove(**data)
