import requests
from ansible.module_utils.basic import *
DOCUMENTATION = '''
---
module: azurewebjobsdeploy
short_description: Uploads file to the azure app service
'''

EXAMPLES = '''
- name: Upload file to workspace
  azurewebjobsdeploy:
    appServiceName: "testjino"
    accessToken: "xx....xx"
    fileLocation: "/home/user/tezt.zip"
  register: result
'''

def appServiceWebJobs(appServiceName, accessToken, fileLocation):

    uploadUrl = "https://" + appServiceName + \
        ".scm.azurewebsites.net/api/zipdeploy"
    Token = "Bearer " + accessToken + ""
    # print(Token)
    data = open(fileLocation, 'rb').read()
    headers = {
        "Content-Type": "application/binary",
        "Authorization": Token
    }
    upload = requests.put(uploadUrl, data=data, headers=headers)

    if upload.status_code == 200:
        _result = "uploaded success"
        return False, {"status": _result }
    else:
        if upload.status_code == 401 or upload.status_code == 403:
            _result = "Bearer Token Error"
        return False, { "status": _result }
    
def main():
    module = AnsibleModule(
        argument_spec=dict(
            appServiceName=dict(required=True, type='str'),
            accessToken=dict(required=True, type='str'),
            fileLocation=dict(required=True, type='str')
        )
    )

    is_error, result = appServiceWebJobs(
        module.params['appServiceName'], module.params['accessToken'], module.params['fileLocation'])

    if not is_error:
        module.exit_json(changed=True, meta=result)
    else:
        module.fail_json(msg="Error upload file", meta=result)


if __name__ == '__main__':
    main()