#!/bin/bash

vms=$(VBoxManage list vms | cut -d' ' -f 1 | sed -e 's/"//g')
if [ -z "$vms" ] ; then
	echo "No vms to nuke."
	exit 0
fi
for v in $vms; do
	echo -n "Nuking VM $v "
	VBoxManage unregistervm $v --delete
	echo "done."
done
