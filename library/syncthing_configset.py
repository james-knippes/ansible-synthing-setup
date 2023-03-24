#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# Copyright: (c) 2023, helican <james-knippes@mailbox.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: synthing_configset

short_description: Set option in syncthing

version_added: "1.0.0"

description: Change config setting for default synthing instance. Instance service has to be running.

options:
    option:
        description: name of the option
        required: true
        type: str
    value:
        description: value the option should have
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
#TODO
'''

from ansible.module_utils.basic import AnsibleModule
import subprocess

def run_module():
    module_args = dict(
        option=dict(type='str', required=True),
        value=dict(type='str', required=True),
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # check if option is already set to value
    proc = subprocess.run(
        ["syncthing", "cli", "config", "options", module.params['option'] , "get"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )
    if module.params['value'] != proc.stdout.splitlines()[0]:
        result['changed'] = True
    if module.check_mode:
        module.exit_json(**result)

    # Set option to new value
    if result['changed']:
        proc = subprocess.run(
            ["syncthing", "cli", "config", "options", module.params['option'] , "set", module.params['value']],
            check=True
        )

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
