# -*- coding: utf-8 -*-

"""
This module contains the set of bootstrap's exceptions

:copyright: (c) 2012 by Sean Plaice.
:license: ISC, see LICENSE for more details.

"""

import logging


# setup module level logger
logger = logging.getLogger(__name__)


class VirtboxError(Exception):
    """ This is an ambiguous error that occured.
    """
    pass


class VirtboxMissingArgument(VirtboxError):
    """ This is an error when a method is called missing a required parameter.
    """


class VirtboxManageError(VirtboxError):
    """ This is an error specific to the use of the Manage class.
    """
    def __init__(self, reason=None):
        self.reason = reason

    def as_dict(self):
        return {'reason': self.reason}

    def __str__(self):
        return '%s' % str(self.as_dict())


class VirtboxCommandError(VirtboxError):
    """ This is an error specific to running a VBoxManage command.
    """
    def __init__(self, status_code=None, cmd=None, stdout=None, stderr=None):
        self.status_code = status_code
        self.cmd = cmd
        self.stdout = stdout
        self.stderr = stderr

    def as_dict(self):
        return {'status_code': self.status_code, 'cmd': self.cmd, 'stdout':
                self.stdout, 'stderr': self.stderr}

    def __str__(self):
        return '%s' % str(self.as_dict())


class VirtboxCommandNotImplemented(VirtboxError):
    """ This is an error specific top methods that map to commands that are
        not yet implemented.
    """

    def __init__(self, reason=None):
        self.reason = reason

    def as_dict(self):
        return {'reason': self.reason}

    def __str__(self):
        return '%s' % str(self.as_dict())
