```yml
---
- hosts: localhost
  tasks:
  - name: update the databricks logs in existing adb cluster 
    uri:
      url: "https://{{ adbUrl }}/api/2.0/clusters/edit"
      method: POST
      headers:
        Content-Type: application/json
        Authorization: "Bearer {{ kvsecrets[secretName] }}"
      body_format: json
      body: |
        {
        "cluster_name": "{{ cvx_environment_name }}",
        "cluster_id": "{{ _details.json.clusters[0].cluster_id }}",
        "spark_version": "7.3.x-scala2.12",
        "autotermination_minutes": 120,
          "autoscale": { 
            "min_workers": 1,
            "max_workers": 4
            },
        "node_type_id": "Standard_D16_v3",
          "cluster_log_conf": {
            "dbfs": {
              "destination": "dbfs:/logs"
            }
          }
        }

```
