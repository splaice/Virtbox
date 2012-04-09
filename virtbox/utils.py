# -*- coding: utf-8 -*-

"""
virtbox.utils
~~~~~~~~

This module provides utility functions that are used within Bootstrap
that are also useful for external consumption.

:copyright: (c) 2012 by Sean Plaice.
:license: ISC, see LICENSE for more details.

"""

from pyparsing import (Word, alphas, nums, dblQuotedString, alphanums, srange,
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


def parse_showvminfo(txt):
    """
    """

    eol = Suppress(LineEnd())
    eql = Suppress(Literal('='))
    label = Suppress(Word(alphanums))
    filepath_pattern = alphanums + ' /.'
    uuid_pattern = alphanums + '-'

    def pg(_id):
        return label + eql + _id + eol

    id_name = dblQuotedString(alphanums + ' ').setResultsName('name')
    id_ostype = dblQuotedString(alphanums + ' /').setResultsName('ostype')
    id_uuid = dblQuotedString(uuid_pattern).setResultsName('uuid')
    id_cfgfile = dblQuotedString(filepath_pattern).setResultsName('cfgfile')
    id_snapfldr = dblQuotedString(filepath_pattern).setResultsName('snapfldr')
    id_logfldr = dblQuotedString(filepath_pattern).setResultsName('logfldr')
    id_hardwareuuid = dblQuotedString(uuid_pattern).setResultsName(
            'hardwareuuid')
    id_memory = Word(nums).setResultsName('memory')
    id_pagefusion = dblQuotedString(alphas).setResultsName('pagefusion')
    id_vram = Word(nums).setResultsName('vram')
    id_cpuexecutioncap = Word(nums).setResultsName('cpuexecutioncap')
    id_hpet = dblQuotedString(alphas).setResultsName('hpet')
    id_chipset = dblQuotedString(alphanums).setResultsName('chipset')
    id_firmware = dblQuotedString(alphas).setResultsName('firmware')
    id_cpus = Word(nums).setResultsName('cpus')
    id_synthcpu = dblQuotedString(alphas).setResultsName('synthcpus')
    id_bootmenu = dblQuotedString(alphas).setResultsName('bootmenu')
    id_boot1 = dblQuotedString(alphas).setResultsName('boot1')
    id_boot2 = dblQuotedString(alphas).setResultsName('boot1')
    id_boot3 = dblQuotedString(alphas).setResultsName('boot1')
    id_boot4 = dblQuotedString(alphas).setResultsName('boot1')
    id_acpi = dblQuotedString(alphas).setResultsName('acpi')
    id_ioacpi = dblQuotedString(alphas).setResultsName('ioacpi')
    id_pae = dblQuotedString(alphas).setResultsName('pae')
    id_biossystemtimeoffset = Word(nums).setResultsName('biossystemtimeoffset')
    id_rtcuseutc = dblQuotedString(alphas).setResultsName('rtcuseutc')
    id_hwvirtex = dblQuotedString(alphas).setResultsName('hwvirtex')
    id_hwvirtexexcl = dblQuotedString(alphas).setResultsName('hwvirtexexcl')
    id_nestedpaging = dblQuotedString(alphas).setResultsName('nestedpaging')
    id_largepages = dblQuotedString(alphas).setResultsName('largepages')
    id_vtxvpid = dblQuotedString(alphas).setResultsName('vtxvpid')
    id_vmstate = dblQuotedString(alphas).setResultsName('vmstate')
    id_vmstatechangetime = dblQuotedString(alphanums + '-:.').setResultsName(
            'vmstatechangetime')
    id_monitorcount = Word(nums).setResultsName('monitorcount')
    id_accelerate3d = dblQuotedString(alphas).setResultsName('accelerate3d')
    id_accelerate2dvideo = dblQuotedString(alphas).setResultsName(
            'accelerate2dvideo')
    id_teleporterenabled = dblQuotedString(alphas).setResultsName(
            'teleporterenabled')
    id_teleporterport = Word(nums).setResultsName('teleporterport')
    id_teleporteraddress = dblQuotedString(alphas).setResultsName(
            'teleporteraddress')
    id_teleporterpassword = dblQuotedString(alphas).setResultsName(
            'teleporterpassword')
    id_nic1 = dblQuotedString(alphanums).setResultsName('nic1')
    id_nic2 = dblQuotedString(alphanums).setResultsName('nic2')
    id_nic3 = dblQuotedString(alphanums).setResultsName('nic3')
    id_nic4 = dblQuotedString(alphanums).setResultsName('nic4')
    id_nic5 = dblQuotedString(alphanums).setResultsName('nic5')
    id_nic6 = dblQuotedString(alphanums).setResultsName('nic6')
    id_nic7 = dblQuotedString(alphanums).setResultsName('nic7')
    id_nic8 = dblQuotedString(alphanums).setResultsName('nic8')
    id_hidpointing = dblQuotedString(alphanums).setResultsName('hidpointing')
    id_hidkeyboard = dblQuotedString(alphanums).setResultsName('hidkeyboard')
    id_uart1 = dblQuotedString(alphanums).setResultsName('uart1')
    id_uart2 = dblQuotedString(alphanums).setResultsName('uart2')
    id_audio = dblQuotedString(alphanums).setResultsName('audio')
    id_clipboard = dblQuotedString(alphanums).setResultsName('clipboard')
    id_vrde = dblQuotedString(alphanums).setResultsName('vrde')
    id_usb = dblQuotedString(alphanums).setResultsName('usb')
    id_vrdeactiveconnection = dblQuotedString(alphanums).setResultsName(
            'vrdeactiveconnection')
    id_vrdeclients = Word(nums).setResultsName(
            'vrdeclients')
    id_guestmemoryballoon = Word(nums).setResultsName('guestmemoryballoon')
    id_guestostype = dblQuotedString(alphanums).setResultsName('guestostype')
    id_guestadditionsrunlevel = Word(nums).setResultsName(
            'guestadditionsrunlevel')

    showvminfo = Group(pg(id_name) + pg(id_ostype) + pg(id_uuid) +
            pg(id_cfgfile) + pg(id_snapfldr) + pg(id_logfldr) +
            pg(id_hardwareuuid) + pg(id_memory) + pg(id_pagefusion) +
            pg(id_vram) + pg(id_cpuexecutioncap) + pg(id_hpet) +
            pg(id_chipset) + pg(id_firmware) + pg(id_cpus) + pg(id_synthcpu) +
            pg(id_bootmenu) + pg(id_boot1) + pg(id_boot2) + pg(id_boot3) +
            pg(id_boot4) + pg(id_acpi) + pg(id_ioacpi) + pg(id_pae) +
            pg(id_biossystemtimeoffset) + pg(id_rtcuseutc) + pg(id_hwvirtex) +
            pg(id_hwvirtexexcl) + pg(id_nestedpaging) + pg(id_largepages) +
            pg(id_vtxvpid) + pg(id_vmstate) + pg(id_vmstatechangetime) +
            pg(id_monitorcount) + pg(id_accelerate3d) +
            pg(id_accelerate2dvideo) + pg(id_teleporterenabled) +
            pg(id_teleporterport) + pg(id_teleporteraddress) +
            pg(id_teleporterpassword) + pg(id_nic1) + pg(id_nic2) +
            pg(id_nic3) + pg(id_nic4) + pg(id_nic5) + pg(id_nic6) +
            pg(id_nic7) + pg(id_nic8) + pg(id_hidpointing) +
            pg(id_hidkeyboard) + pg(id_uart1) + pg(id_uart2) +
            pg(id_audio) + pg(id_clipboard) + pg(id_vrde) + pg(id_usb) +
            pg(id_vrdeactiveconnection) + pg(id_vrdeclients) +
            pg(id_guestmemoryballoon) + pg(id_guestostype) +
            pg(id_guestadditionsrunlevel))

    out = showvminfo.parseString(txt)[0]
    dict_out = {'name': out.name, 'ostype': out.ostype, 'uuid': out.uuid,
            'cfgfile': out.cfgfile, 'snapfldr': out.snapfldr,
            'logfldr': out.logfldr, 'hardwareuuid': out.hardwareuuid,
            'memory': out.memory, 'pagefusion': out.pagefusion,
            'vram': out.vram, 'cpuexecutioncap': out.cpuexecutioncap,
            'hpet': out.hpet, 'chipset': out.chipset, 'firmware': out.firmware,
            'cpus': out.cpus, 'synthcpu': out.synthcpu,
            'bootmenu': out.bootmenu, 'boot1': out.boot1, 'boot2': out.boot2,
            'boot3': out.boot3, 'boot4': out.boot4, 'acpi': out.acpi,
            'ioacpi': out.acpi, 'pae': out.pae,
            'biossystemtimeoffset': out.biossystemtimeoffset,
            'rtcuseutc': out.rtcuseutc, 'hwvirtex': out.hwvirtex,
            'hwvirtexexcl': out.hwvirtexexcl, 'nestedpaging': out.nestedpaging,
            'largepages': out.largepages, 'vtxvpid': out.vtxvpid,
            'vmstate': out.vmstate, 'vmstatechangetime': out.vmstatechangetime,
            'monitorcount': out.monitorcount, 'accelerate3d': out.accelerate3d,
            'accelerate2dvideo': out.accelerate2dvideo,
            'teleporterenabled': out.teleporterenabled,
            'teleporterport': out.teleporterport,
            'teleporteraddress': out.teleporteraddress,
            'teleporterpassword': out.teleporterpassword, 'nic1': out.nic1,
            'nic2': out.nic2, 'nic3': out.nic3, 'nic4': out.nic4,
            'nic5': out.nic5, 'nic6': out.nic6, 'nic7': out.nic8,
            'hidpointing': out.hidpointing, 'hidkeyboard': out.hidkeyboard,
            'uart1': out.uart1, 'uart2': out.uart2, 'audio': out.audio,
            'clipboard': out.clipboard, 'vrde': out.vrde,
            'vrdeclients': out.vrdeclients,
            'guestmemoryballoon': out.guestmemoryballoon,
            'guestostype': out.guestostype,
            'guestadditionsrunlevel': out.guestadditionsrunlevel}

    # should probably use a better grammar but this is fine for now
    for k, v in dict_out.iteritems():
        if v.startswith('"') and v.endswith('"'):
            dict_out[k] = v.strip('"')

    return dict_out


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
    return txt
