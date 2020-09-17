 webjobs deployment via ansible
 
    ---
    - name: all
      hosts: localhost
      vars:
        appname: "testjino"
        tenant: "xxx"
        clientid: "xxx"
        secretid: "xxx"
        file_location: /home/sepoy/Documents/ansible/App_Data.zip
        body: 'grant_type=client_credentials&client_id={{clientid}}&resource=https://management.core.windows.net/&client_secret={{secretid}}'
      tasks:
      - name: Create a JIRA issue
        uri:
          url: "https://login.microsoftonline.com/{{ tenant }}/oauth2/token"
          return_content: yes
          method: GET
          headers:
            Content-Type: application/x-www-form-urlencoded
          body: "{{ body }}"
        register: test

      - shell: 'curl -X POST -H  "Authorization: Bearer {{ test.json.access_token  }}" --data-binary @"{{ file_location }}" "https://{{ appname }}.scm.azurewebsites.net/api/zipdeploy"'
        register: test
