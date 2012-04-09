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
    id_name = Word(alphas).setResultsName('name')
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
