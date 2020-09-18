import requests
from ansible.module_utils.basic import *

DOCUMENTATION = '''
---
module: azureAccessToken
short_description: get Azure resource Manager access token
'''

EXAMPLES = '''
- name: get Azure azureAccessToken
  azureAccessToken:
    tenantid: "abcdfrrew90"
    clientid: "zjsdfjdfereqwe"
    clientsecret: "JSAJjashuw"
  register: result
'''

def azureAccessToken(tenantid, clientid, clientsecret):

    response = requests.post(
        url="https://login.microsoftonline.com/" + tenantid + "/oauth2/token",
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data='grant_type=client_credentials&client_id=' + clientid +
        '&resource=https://management.core.windows.net/&client_secret=' + clientsecret
    )

    results = response.json()
    return False, {"accessToken": results['access_token'], "expireOn": results['expires_on']}


def main():
    module = AnsibleModule(
        argument_spec=dict(
            tenantid=dict(required=True, type='str'),
            clientid=dict(required=True, type='str'),
            clientsecret=dict(required=True, type='str')
        )
    )

    is_error, result = azureAccessToken(
        module.params['tenantid'], module.params['clientid'], module.params['clientsecret'])

    if not is_error:
        module.exit_json(changed=False, meta=result)
    else:
        module.fail_json(msg="Error importing file", meta=result)


if __name__ == '__main__':
    main()
