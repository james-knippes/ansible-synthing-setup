#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# Copyright: (c) 2023, helican <james-knippes@mailbox.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: synthing_share

short_description: Add device to shared folder in syncthing

version_added: "1.0.0"

description: Add a device to an existing folder in the default synthing instance. Instance service has to be running.

options:
    folder_id:
        description: folder id to use
        required: true
        type: str
    device_id:
        description: folder id to add
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
# Signals, that a device with the specified ID was already added to the specified folder
id_exists:
    type: bool
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
import subprocess

def run_module():
    module_args = dict(
        folder_id=dict(type='str', required=True),
        device_id=dict(type='str', required=True),
    )

    result = dict(
        changed=False,
        id_exists=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # check if folder ID to share already exists. exit with failure if not
    proc = subprocess.run(
        ["syncthing", "cli", "config", "folders", "list"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )
    if not module.params['folder_id'] in proc.stdout.splitlines():
        module.fail_json(msg=f"no folder with id {module.params['folder_id']} to share", **result)

    # Check if device ID is already added to folder
    proc = subprocess.run(
        ["syncthing", "cli", "config", "folders", module.params['folder_id'], "devices", "list"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )
    if module.params['device_id'] in proc.stdout.splitlines():
        result['id_exists'] = True
    if module.check_mode:
        module.exit_json(**result)

    # Add device ID to the folder if doesn't exist
    if not result['id_exists']:
        proc = subprocess.run(
            ["syncthing", "cli", "config", "folders", module.params['folder_id'], "devices", "add", "--device-id", module.params['device_id']],
            check=True,
        )
        result['changed'] = True

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
