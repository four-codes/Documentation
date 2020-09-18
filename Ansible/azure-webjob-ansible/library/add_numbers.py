from ansible.module_utils.basic import *

DOCUMENTATION = '''
---
module: add_numbers
short_description: get the OS env variable
'''

EXAMPLES = '''
- name: Add three numbers
  add_numbers:
    a: 1
    b: 2
    c: 3
  register: result
'''

def Add(a,b,c):
    d = a + b + c
    print(d)
    return False, {"value": d}

def main():
    module = AnsibleModule(
    argument_spec=dict(
        a=dict(required=True, type='int'),
        b=dict(required=True, type='int'),
        c=dict(required=True, type='int')
    )
)

    is_error, result = Add(module.params['a'], module.params['b'], module.params['c'])
    
    if not is_error:
        module.exit_json(changed=False, meta=result)
    else:
        module.fail_json(msg="Error importing file", meta=result)

if __name__ == '__main__':
    main()
