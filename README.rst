Virtbox: Simple VirtualBox management
=========================

Build, configure, manage virtualbox virtual machines.


::

    >>> v = virtbox.create(name='jangofett', memory=128, hdds=[{'name': 'main', 'size': 2048}])
    >>> v.status_code
    0
    >>> v.name
    'jangofett'
    >>> v.status
    'off'
    >>> v.memory
    128
    >>> v.hdds
    [
        {
            'size': 2048,
            'format': 'VDI',
            'variant': 'Standard',
            'filename': '/Users/homie/VirtualBox\ VMs/dev/main.vdi'
         }
    ]
    >>> v.start()
    >>> v.status_code
    0
    >>> v.status
    'booting'
    >>> v.status
    'running'
    >>> v.run('shutdown -h now')
    >>> v.status_code
    0
    >>> v.status
    'off'
    >>> v.export(image='/tmp/myclone.virtbox')
    v.status_code
    0
    >>> v2 = virtbox.create(name='bobafett', image='/tmp/mylcone.virtbox')
    >>> v2.status_code
    0
    >>> v2.name
    'bobafett'
    >>> v2.start()
    >>> v2.status_code
    0
    >>> v2.status
    'running'

::

    >>> virtbox.machines
    [
        {
            'name': 'jangofett',
            'uuid': 'xyz'
        },
        {
            'name': 'bobafett',
            'uuid': 'xyz'
        },
    ]
    >>> v = virtbox.machine(name='jangofett')
    >>> v.status_code
    0
    >>> v.status
    'off'
    >>> v2 = virtbox.machine(name='bobafett')
    >>> v2.status_code
    0
    >>> v2.status
    'running'


Features
--------

- Example ...


Contribute
----------

#. Fork the project on github to start making your changes
#. Send pull requests with your bug fixes or features
#. Submit and create issues on github
