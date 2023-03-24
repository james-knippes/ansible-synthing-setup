#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# Copyright: (c) 2023, helican <james-knippes@mailbox.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: synthing_folder

short_description: Add folder to syncthing

version_added: "1.0.0"

description: Add a folder to the users default synthing instance. Instance service has to be running.

options:
    folder_id:
        description: folder id to add
        required: true
        type: str
    folder_label:
        description: folder label to assing
        required: false
        type: str
    folder_path:
        description: folder path to use
        required: false
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
# Signals, that a folder with the specified ID is already present
id_exists:
    type: bool
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
import subprocess

def run_module():
    module_args = dict(
        folder_id=dict(type='str', required=True),
        folder_label=dict(type='str', required=False, default='sync'),
        folder_path=dict(type='str', required=False, default='/home/default/sync'),
    )

    result = dict(
        changed=False,
        id_exists=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # check if a folder with specified ID already exists
    proc = subprocess.run(
        ["syncthing", "cli", "config", "folders", "list"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )
    if module.params['folder_id'] in proc.stdout.splitlines():
        result['id_exists'] = True
    if module.check_mode:
        module.exit_json(**result)

    # Add folder if ID is not existent
    if not result['id_exists']:
        proc = subprocess.run(
            ["syncthing", "cli", "config", "folders", "add", "--id", module.params['folder_id'], "--label", module.params['folder_label'], "--path", module.params['folder_path'], "--type", "sendreceive", "--filesystem-type", "basic" ],
            check=True,
        )
        result['changed'] = True

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
