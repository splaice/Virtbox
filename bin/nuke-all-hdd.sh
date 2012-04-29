#!/bin/bash

cd /tmp
hdds=$(ls -1 *.vdi 2>/dev/null)
if [ "$?" -ne "0" ]; then
	echo "No hdd to nuke."
	exit 0
fi
for hdd in $(ls -1 *.vdi); do
	echo -n "Nuking hdd $hdd "
	rm $hdd
	echo "done"
done
