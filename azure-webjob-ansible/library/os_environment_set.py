import os
from ansible.module_utils.basic import *

DOCUMENTATION = '''
---
module: os_environment
short_description: get the OS env variable
'''

EXAMPLES = '''
- name: get os variable
  os_environment_set:
    environment_name: home
    environment_value
  register: result
'''

def setEnv(keyname,keyvalue):
    keynames = keyname.upper()
    keyvalues = keyvalue
    os.environ[keynames] = keyvalues
    return False, { "name": keynames, "value": keyvalues  }


def main():
    module = AnsibleModule(
        argument_spec=dict(
            environment_name=dict(required=True, type='str'),
            environment_value=dict(required=True, type='str')
        )
    )

    is_error, result = setEnv(module.params['environment_name'], module.params['environment_value'])

    if not is_error:
        module.exit_json(changed=True, meta=result)
    else:
        module.fail_json(msg="Error throw", meta=result)


if __name__ == '__main__':
    main()
