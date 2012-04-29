# -*- coding: utf-8 -*-
"""
This module contains utility functions used in our tests.

:copyright: (c) 2012 by Sean Plaice
:license: ISC, see LICENSE for more details.
"""

import string
import random
import os

from virtbox.models import Manage


def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def generate_vm(**kwargs):
    data = {'name': id_generator(7),
            'ostype': 'Linux'}
    data.update(kwargs)
    return Manage.createvm(**data)


def delete_vm(**kwargs):
    data = {'delete': True}
    data.update(kwargs)
    # prune unneeded / unexpected kwargs
    if data.get('file_path'):
        del data['file_path']
    return Manage.unregistervm(**data)


def generate_hd(**kwargs):
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
    data = {'name': 'primary',
            'ctl_type': 'scsi',
            'controller': 'LSILogic'}
    data.update(kwargs)
    Manage.storagectl_add(**data)
    return data


def delete_ctl(**kwargs):
    data = {'name': 'primary'}
    data.update(kwargs)
    # prune unneeded / unexpected kwargs
    if data.get('controller'):
        del data['controller']
    if data.get('ctl_type'):
        del data['ctl_type']
    return Manage.storagectl_remove(**data)
