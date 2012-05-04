# -*- coding: utf-8 -*-

"""
virtbox.parsers
~~~~~~~~

This module provides parsing functions that are used parse the output of
various commands.

:copyright: (c) 2012 by Sean Plaice.
:license: ISC, see LICENSE for more details.

"""

import logging

from pyparsing import (Word, alphas, dblQuotedString, alphanums, srange,
                       OneOrMore, Group, Suppress, Literal,
                       LineEnd, Combine, hexnums)

# setup module level logger
LOGGER = logging.getLogger(__name__)

# pyparsing grammars
HEX_STRING = lambda n: Word(hexnums, exact=n)
UUID_STRING = Combine(HEX_STRING(8) + "-" + HEX_STRING(4) + "-" +
    HEX_STRING(4) + "-" + HEX_STRING(4) + "-" + HEX_STRING(12))


def parse_version(stdout, stderr):
    """
    """
    version = stdout.rstrip()
    return {'version': version}


def parse_list_vms(stdout, stderr):
    """
    """
    id_vm_name = dblQuotedString(alphas).setResultsName('name')
    id_vm_uuid = Word(srange("[a-zA-Z0-9_\-]")).setResultsName('uuid')
    left_brace = Suppress("{")
    right_brace = Suppress("}")
    vm_group = Group(id_vm_name + left_brace + id_vm_uuid + right_brace)
    vm_list = OneOrMore(vm_group)

    token_lists = vm_list.parseString(stdout, parseAll=True)
    return [{'name': token_list.name.replace('\"', ''),
             'uuid': token_list.uuid} for token_list in token_lists]


def parse_list_ostypes(stdout, stderr):
    """
    """
    eol = Suppress(LineEnd())
    id_label = Suppress(Word("ID:"))
    id_os_type = Word(alphanums + "-" + "/" + "]" + "_").\
            setResultsName('os_type')
    desc_label = Suppress(Word("Description:"))
    id_os_desc = Word(alphanums + "/" + " " + "(" + ")" + ".").\
            setResultsName('os_desc')
    os_type_group = Group(id_label + id_os_type + eol + desc_label +
            id_os_desc)
    os_type_list = OneOrMore(os_type_group)
    token_lists = os_type_list.parseString(stdout, parseAll=True)
    return [{'os_type': token_list.os_type,
             'os_desc': token_list.os_desc} for token_list in token_lists]


def parse_showvminfo(stdout, stderr):
    """
    """
    data = {}
    for line in stdout.split('\n'):
        if len(line) > 0:
            (key, value) = tuple(line.split('='))
            data[key.lower()] = value.replace('\"', '')

    return data


def parse_unregistervm(stdout, stderr):
    """
    """
    return stdout


def parse_createvm(stdout, stderr):
    """
    """
    eol = Suppress(LineEnd())
    single_quote = Suppress(Literal('\''))
    name_prefix = Suppress(Word('Virtual machine'))
    id_name = Word(alphanums).setResultsName('name')
    name_postfix = Suppress(Word('is created and registered.'))
    uuid_prefix = Suppress(Word('UUID:'))
    id_vm_uuid = Word(srange("[a-zA-Z0-9_\-]")).setResultsName('uuid')
    file_prefix = Suppress(Word('Settings file:'))
    id_file_path = Word(alphanums + " /.").setResultsName('file_path')
    vm_info = Group(name_prefix + single_quote + id_name +
        single_quote + name_postfix + eol + uuid_prefix + id_vm_uuid + eol +
        file_prefix + single_quote + id_file_path + single_quote + eol)
    out = vm_info.parseString(stdout)[0]
    return {'name': out.name, 'uuid': out.uuid, 'file_path': out.file_path}


def parse_modifyvm(stdout, stderr):
    """
    """
    return stdout


def parse_closemedium(stdout, stderr):
    """
    """
    return stdout


def parse_storageattach(stdout, stderr):
    """
    """
    return stdout


def parse_storagectl_add(stdout, stderr):
    """
    """
    return stdout


def parse_storagectl_remove(stdout, stderr):
    """
    """
    return stdout


def parse_showhdinfo(stdout, stderr):
    """
    """
    eol = Suppress(LineEnd())
    uuid_prefix = Suppress(Word('UUID:'))
    id_uuid = Word(alphanums + '-').setResultsName('uuid')
    accessible_prefix = Suppress(Word('Accessible:'))
    id_accessible = Word(alphas).setResultsName('accessible')
    logical_size_prefix = Suppress(Word('Logical size:'))
    id_logical_size = Word(alphanums + ' ').setResultsName('logical_size')
    current_size_prefix = Suppress(Word('Current size on disk:'))
    id_current_size = Word(alphanums + ' ').setResultsName('current_size')
    type_prefix = Suppress(Word('Type:'))
    id_type = Word(alphas + ' ()').setResultsName('type')
    prefix_storage_format = Suppress(Word('Storage format:'))
    id_storage_format = Word(alphas).setResultsName('storage_format')
    prefix_format_variant = Suppress(Word('Format variant:'))
    id_format_variant = Word(alphanums + ' ').setResultsName('format_variant')
    prefix_location = Suppress(Word('Location:'))
    id_location = Word(alphanums + ' /.').setResultsName('location')

    hd_info = Group(uuid_prefix + id_uuid + eol + accessible_prefix +
            id_accessible + eol + logical_size_prefix + id_logical_size + eol +
            current_size_prefix + id_current_size + eol + type_prefix +
            id_type + eol + prefix_storage_format + id_storage_format + eol +
            prefix_format_variant + id_format_variant + eol + prefix_location +
            id_location + eol)
    out = hd_info.parseString(stdout)[0]

    return {'uuid': out.uuid, 'accessible': out.accessible,
            'logical_size': out.logical_size, 'current_size': out.current_size,
            'type': out.type, 'storage_format': out.storage_format,
            'format_variant': out.storage_variant, 'location': out.location}


def parse_createhd(stdout, stderr):
    """
    """
    uuid_prefix = Group(Word('Disk') + Word('image') + Word('created.') +
            Word('UUID:'))
    userdata = uuid_prefix + UUID_STRING.setResultsName('uuid')
    out = userdata.parseString(stdout)

    return {'uuid': out.uuid}
