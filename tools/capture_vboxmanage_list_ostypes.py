#!/usr/bin/env python
import os
import envoy
import codecs

COMMAND = "VBoxManage list ostypes"


filepath = os.path.join('parser_test_data', 'vboxmanage_list_ostypes.txt')
with codecs.open(filepath, 'w', "utf-8") as fn:
    r = envoy.run(COMMAND)
    if r.status_code:
        raise Exception("could no run command")
    fn.write(r.std_out)
