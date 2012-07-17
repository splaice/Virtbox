# -*- coding: utf-8 -*-
"""
This module contains constants used.

:copyright: (c) 2012 by Sean Plaice
:license: ISC, see LICENSE for more details.
"""

VBOXMANAGE_CMD = 'VBoxManage'
BOOLEAN_OPTIONS = ('on', 'off')
HD_FORMATS = ('VDI', 'VMDK', 'VHD', 'RAW')
HD_VARIANTS = ('Standard', 'Fixed', 'Split2G', 'Stream', 'ESX')
MEDIUM_TYPES = ('disk', 'dvd', 'floppy')
STORAGECTL_TYPES = ('ide', 'sata', 'scsi', 'floppy', 'sas')
STORAGECTL_CONTROLLERS = ('LSILogic', 'LSILogicSAS', 'BusLogic', 'IntelAHCI',
    'PIIX3', 'PIIX4', 'ICH6', 'I82078')
STORAGE_TYPES = ('dvddrive', 'hdd', 'fdd')
STORAGE_MTYPES = ('normal', 'writethrough', 'immutable', 'shareable',
    'readonly', 'multiattach')
VM_FIRMWARE_OPTIONS = ('bios', 'efi', 'efi32', 'efi64')
VM_CHIPSET_OPTIONS = ('ich9', 'piix3')
VM_BIOSBOOTMENU_OPTIONS = ('disabled', 'menuonly', 'messageandmenu')
VM_BOOT_OPTIONS = ('none', 'floppy', 'dvd', 'disk', 'net')
VM_NIC_OPTIONS = ('none', 'null', 'nat', 'bridged', 'intnet', 'hostonly',
    'generic')
VM_NICTYPE_OPTIONS = ('Am79C970A', 'Am79C973', '82540EM', '82543GC', '82545EM',
    'virtio')
VM_NICPROMISC_OPTIONS = ('deny', 'allow-vms', 'allow-all')
