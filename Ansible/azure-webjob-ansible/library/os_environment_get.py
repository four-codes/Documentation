import os
from ansible.module_utils.basic import *

DOCUMENTATION = '''
---
module: os_environment
short_description: get the OS env variable
'''

EXAMPLES = '''
- name: get os variable
  os_environment:
    environment_name: home
  register: result
'''

def getEnv(keyname):
    keynames = keyname.upper()
    results = os.getenv(keynames)
    return False, {"vaule": results}


def main():
    module = AnsibleModule(
        argument_spec=dict(
            environment_name=dict(required=True, type='str')
        )
    )

    is_error, result = getEnv(module.params['environment_name'])

    if not is_error:
        module.exit_json(changed=False, meta=result)
    else:
        module.fail_json(msg="Error importing file", meta=result)


if __name__ == '__main__':
    main()
