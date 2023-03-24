#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# Copyright: (c) 2023, helican <james-knippes@mailbox.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: synthing_device

short_description: Add device a to syncthing

version_added: "1.0.0"

description: Add a device to the users default synthing instance. Instance service has to be running.

options:
    device_id:
        description: device id to add
        required: true
        type: str
    device_name:
        description: device name to assing
        required: true
        type: str

extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - helican (james-knippes@mailbox.org)
'''

EXAMPLES = r'''
#TODO
'''

RETURN = r'''
# Signals, that a device with the specified ID is already present
id_exists:
    type: bool
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
import subprocess

def run_module():
    module_args = dict(
        device_id=dict(type='str', required=True),
        device_name=dict(type='str', required=True),
    )

    result = dict(
        changed=False,
        id_exists=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # check if device with specified ID already exists
    proc = subprocess.run(
        ["syncthing", "cli", "config", "devices", "list"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )
    if module.params['device_id'] in proc.stdout.splitlines():
        result['id_exists'] = True
    if module.check_mode:
        module.exit_json(**result)

    # Add device if ID is not existent
    if not result['id_exists']:
        proc = subprocess.run(
            ["syncthing", "cli", "config", "devices", "add", "--name", module.params['device_name'] , "--device-id", module.params['device_id'], "--max-send-kbps", "10240", "--max-recv-kbps", "10240" ],
            check=True,
        )
        result['changed'] = True

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
