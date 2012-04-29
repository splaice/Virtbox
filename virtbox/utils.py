# -*- coding: utf-8 -*-

"""
virtbox.utils
~~~~~~~~

This module provides utility functions that are used within Bootstrap
that are also useful for external consumption.

:copyright: (c) 2012 by Sean Plaice.
:license: ISC, see LICENSE for more details.

"""

from pyparsing import (Word, alphas, dblQuotedString, alphanums, srange,
                       OneOrMore, Group, Suppress, Literal,
                       LineEnd)


def parse_list_vms(txt):
    id_vm_name = dblQuotedString(alphas).setResultsName('name')
    id_vm_uuid = Word(srange("[a-zA-Z0-9_\-]")).setResultsName('uuid')
    left_brace = Suppress("{")
    right_brace = Suppress("}")
    vm_group = Group(id_vm_name + left_brace + id_vm_uuid + right_brace)
    vm_list = OneOrMore(vm_group)

    token_lists = vm_list.parseString(txt, parseAll=True)
    return [{'name': token_list.name.replace('\"', ''),
             'uuid': token_list.uuid} for token_list in token_lists]


def parse_list_ostypes(txt):
    """ Incomplete
    """
    eol = Suppress(LineEnd())
    id_label = Suppress(Word("ID:"))
    id_os_type = Word(srange("[a-zA-Z0-9_\-/]")).setResultsName('os_type')
    id_os_desc = Word(srange("[a-zA-Z0-9_\-/]")).setResultsName('os_desc')
    desc_label = Suppress(Word("Description:"))
    os_type_group = Group(id_label + id_os_type + eol + desc_label + id_os_desc
            + eol)
    os_type_list = OneOrMore(os_type_group)
    return os_type_list.parseString(txt)


def parse_createvm(txt):
    """
    Virtual machine 'foobar' is created and registered.
    UUID: 65749ad3-a77d-4f82-9dac-6d9176bf5d23
    Settings file: '/Users/virtbox/VirtualBox VMs/foobar/foobar.vbox'
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
    out = vm_info.parseString(txt)[0]
    return {'name': out.name, 'uuid': out.uuid, 'file_path': out.file_path}


def parse_showvminfo(txt):
    data = {}
    for line in txt.split('\n'):
        if len(line) > 0:
            (key, value) = tuple(line.split('='))
            data[key.lower()] = value.replace('\"', '')

    return data


def parse_createhd(txt):
    """
    Disk image created. UUID: 0ab4081c-f383-4ba0-96df-ed7b4ed2d791
    """

    uuid_prefix = Suppress(Word('Disk image created. UUID:'))
    id_uuid = Word(alphanums + '-').setResultsName('uuid')
    hd_info = Group(uuid_prefix + id_uuid)
    out = hd_info.parseString(txt)[0]
    dict_out = {'uuid': out.uuid}

    return dict_out


def parse_unregistervm(txt):
    return txt


def parse_closemedium(txt):
    return txt


def parse_showhdinfo(txt):
    """
    UUID:                 1e489961-954b-455a-80e6-873c2bef681b
    Accessible:           yes
    Logical size:         128 MBytes
    Current size on disk: 0 MBytes
    Type:                 normal (base)
    Storage format:       VDI
    Format variant:       dynamic default
    Location:             /tmp/test.vdi
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
    out = hd_info.parseString(txt)[0]

    dict_out = {'uuid': out.uuid, 'accessible': out.accessible,
            'logical_size': out.logical_size, 'current_size': out.current_size,
            'type': out.type, 'storage_format': out.storage_format,
            'format_variant': out.storage_variant, 'location': out.location}
    return dict_out


def parse_modifyvm(txt):
    return txt


def parse_storagectl_add(txt):
    return txt


def parse_storagectl_remove(txt):
    return txt


def parse_storageattach(txt):
    return txt
