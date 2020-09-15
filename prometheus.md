prometheus installation

    sudo useradd --no-create-home -c "Monitoring user" --shell /bin/false prometheus
    sudo mkdir /etc/prometheus
    sudo mkdir /var/lib/prometheus
    sudo chown prometheus:prometheus /etc/prometheus
    sudo chown prometheus:prometheus /var/lib/prometheus

    sudo apt install wget tar -y
    wget https://github.com/prometheus/prometheus/releases/download/v2.20.1/prometheus-2.20.1.linux-amd64.tar.gz
    tar -vxzf prometheus-2.20.1.linux-amd64.tar.gz
    mv prometheus-2.20.1.linux-amd64 prometheus-files


    sudo mv prometheus-files/prometheus /usr/local/bin/
    sudo mv prometheus-files/promtool /usr/local/bin/
    sudo mv prometheus-files/tsdb /usr/local/bin/
    sudo chown prometheus:prometheus /usr/local/bin/prometheus
    sudo chown prometheus:prometheus /usr/local/bin/promtool
    sudo chown prometheus:prometheus /usr/local/bin/tsdb


    sudo ls -la /usr/local/bin


    sudo mv prometheus-files/prometheus.yml /etc/prometheus/
    sudo mv prometheus-files/consoles /etc/prometheus
    sudo mv prometheus-files/console_libraries /etc/prometheus

    sudo chown -R prometheus:prometheus /etc/prometheus/consoles
    sudo chown -R prometheus:prometheus /etc/prometheus/console_libraries


    sudo chown -R prometheus:prometheus  /var/lib/prometheus
    sudo chown -R prometheus:prometheus  /etc/prometheus/prometheus.yml



    sudo vim /etc/systemd/system/prometheus.service 

    [Unit]
    Description=Prometheus Monitoring service
    After=network.target auditd.service

    [Service]
    Type=simple
    WorkingDirectory=/var/lib/prometheus
    User=prometheus
    ExecStart=/usr/local/bin/prometheus \
     --config.file=/etc/prometheus/prometheus.yml \
     --storage.tsdb.path=/var/lib/prometheus/data/ \
     --web.console.templates=/etc/prometheus/consoles \
     --web.console.libraries=/etc/prometheus/console_libraries \
     --storage.tsdb.retention=30d \
     --web.enable-admin-api \
     --web.external-url=http://localhost:10000 \
     --web.listen-address="0.0.0.0:10000" \
     --log.level=info \
     --web.enable-lifecycle \
     --web.page-title="Prometheus Time Series Collection and Processing Server" \
     --log.format=logfmt

    Restart=always
    StandardOutput=syslog
    StandardError=syslog

    [Install]
    WantedBy=default.target


    sudo systemctl daemon-reload
    sudo systemctl start prometheus
    sudo systemctl status prometheus
    sudo netstat -tulpn 


    # vim /etc/prometheus/prometheus.yml

    global:
      scrape_interval:     15s # default 1m
      evaluation_interval: 15s # default 1m
      scrape_timeout: 10s      # default 10s

    # Alertmanager configuration
    alerting:
      alertmanagers:
      - static_configs:
        - targets:
          # - alertmanager:9093

    # Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
    rule_files:
      # - "first_rules.yml"
      # - "second_rules.yml"

    scrape_configs:
      - job_name: 'prometheus'
        static_configs:
        - targets: ['localhost:9090']
          labels: 
            instance: Prometheus

node exporter installation

    # Create node_exporter Service [Each server]
    sudo useradd --no-create-home -c "Monitoring user" --shell /bin/false node_exporter

    wget https://github.com/prometheus/node_exporter/releases/download/v1.0.1/node_exporter-1.0.1.linux-amd64.tar.gz
    tar -vxzf node_exporter-1.0.1.linux-amd64.tar.gz
    sudo mv node_exporter-1.0.1.linux-amd64/node_exporter /usr/local/bin/
    sudo chown -R node_exporter:node_exporter  /usr/local/bin/node_exporter

    sudo vim /etc/systemd/system/node_exporter.service

    # /etc/systemd/system/node_exporter.service
    [Unit]
    Description=Prometheus node exporter
    After=network.target auditd.service

    [Service]
    User=node_exporter
    ExecStart=/usr/local/bin/node_exporter \
      --web.listen-address=0.0.0.0:9100 \
      --collector.tcpstat \
      --collector.bonding \
      --collector.systemd \
      --collector.systemd.unit-whitelist=(sshd|httpd|node_exporter|vsftpd|crond|firewalld|rsyslog).service \
      --collector.meminfo_numa \
      --collector.logind \
      --collector.filesystem.ignored-mount-points "^(/snap/|/run/|/dev/|/sys|/run).*" \
      --no-collector.wifi \
      --no-collector.nfs \
      --no-collector.zfs \
      --no-collector.nfsd \
      --no-collector.mdadm \
      --no-collector.arp \
      --no-collector.bcache \
      --no-collector.buddyinfo \
      --no-collector.edac \
      --no-collector.hwmon \
      --no-collector.qdisc \
      --no-collector.infiniband \
      --collector.ipvs 
      #--path.procfs=/proc 
    Restart=on-failure
    StandardOutput=syslog
    StandardError=syslog

    [Install]
    WantedBy=default.target


    sudo systemctl daemon-reload
    sudo systemctl start node_exporter
    sudo systemctl status node_exporter
    sudo netstat -tulpn 

switch to prometheus server

    # need to change prometheus server.
    # vim /etc/prometheus/prometheus.yml
    # add the new server with new nodeexporter
      - job_name: 'nodeexporter'
        static_configs: 
        - targets: ['localhost:9100']    # server IP address
          labels: 
            instance: Prometheus-server  # server name
        # add the new server with existing nodeexporter
        - targets: ['10.0.1.4:9100']     # server IP address
          labels: 
            instance: additional-server  # server name


        sudo systemctl restart prometheus
        
        
        

mysql exporter installtion

    # install mysql exporter MariaDB mysql [Each Server]
    sudo useradd --no-create-home -c "Monitoring user" --shell /bin/false mysqld_exporter
    wget https://github.com/prometheus/mysqld_exporter/releases/download/v0.12.1/mysqld_exporter-0.12.1.linux-amd64.tar.gz
    tar -vxzf mysqld_exporter-0.12.1.linux-amd64.tar.gz
    sudo mv mysqld_exporter-0.12.1.linux-amd64/mysqld_exporter /usr/local/bin/
    sudo chown -R mysqld_exporter:mysqld_exporter  /usr/local/bin/mysqld_exporter


    # its need mysql server (Require new installtion)
    sudo apt install mysql-server
    sudo systemctl start mysql
    sudo mysql_secure_installtion
    sudo mysql -u root -p 

    # Create Mysql user for mysqld_exporter

    CREATE USER 'mysqld_exporter'@'localhost' IDENTIFIED BY 'StrongPassword' WITH MAX_USER_CONNECTIONS 2;
    GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* TO 'mysqld_exporter'@'localhost';
    FLUSH PRIVILEGES;
    EXIT

    sudo vim /etc/.mysqld_exporter.cnf

    [client]
    user=mysqld_exporter
    password=StrongPassword


    sudo chown root:mysqld_exporter /etc/.mysqld_exporter.cnf

    sudo vim /etc/systemd/system/mysql_exporter.service

    [Unit]
    Description=Prometheus MySQL Exporter
    After=network.target

    [Service]
    Type=simple
    User=mysqld_exporter
    Restart=always
    ExecStart=/usr/local/bin/mysqld_exporter \
      --config.my-cnf /etc/.mysqld_exporter.cnf \
      --collect.global_status \
      --collect.info_schema.innodb_metrics \
      --collect.auto_increment.columns \
      --collect.info_schema.processlist \
      --collect.binlog_size \
      --collect.info_schema.tablestats \
      --collect.global_variables \
      --collect.info_schema.query_response_time \
      --collect.info_schema.userstats \
      --collect.info_schema.tables \
      --collect.perf_schema.tablelocks \
      --collect.perf_schema.file_events \
      --collect.perf_schema.eventswaits \
      --collect.perf_schema.indexiowaits \
      --collect.perf_schema.tableiowaits \
      --collect.slave_status \
      --web.listen-address=0.0.0.0:9104

    [Install]
    WantedBy=multi-user.target


    sudo systemctl daemon-reload
    sudo systemctl enable mysql_exporter
    sudo systemctl start mysql_exporter
    sudo netstat -tulpn

switch to prometheus server

    # need to change prometheus server.
    # vim /etc/prometheus/prometheus.yml
    
    # add the new server with new nodeexporter
      - job_name: 'mysqlexporter'
        static_configs: 
        - targets: ['localhost:9104']    # MySQL IP address
          labels: 
            instance: mysql-server


        sudo systemctl restart prometheus

pushgateway installation

    # PushGateway
    sudo useradd --no-create-home -c "Monitoring user" --shell /bin/false pushgateway
    wget https://github.com/prometheus/pushgateway/releases/download/v1.2.0/pushgateway-1.2.0.linux-amd64.tar.gz
    tar -xvzf pushgateway-1.2.0.linux-amd64.tar.gz
    mv pushgateway-1.2.0.linux-amd64/pushgateway /usr/local/bin/
    sudo chown -R pushgateway:pushgateway /usr/local/bin/pushgateway


    sudo vim /etc/systemd/system/pushgateway.service
    [Unit]
    Description=Pushgateway
    Wants=network-online.target
    After=network-online.target

    [Service]
    User=pushgateway
    Group=pushgateway
    Type=simple
    ExecStart=/usr/local/bin/pushgateway \
        --web.listen-address=":9091" \
        --web.telemetry-path="/metrics" \
        --persistence.file="/tmp/metric.store" \
        --persistence.interval=5m \
        --log.level="info" 

    [Install]
    WantedBy=multi-user.target

    sudo systemctl daemon-reload
    sudo systemctl enable pushgateway
    sudo systemctl start pushgateway
    sudo netstat -tulpn



switch to prometheus server

    # need to change prometheus server.
    # vim /etc/prometheus/prometheus.yml
    
    # add the new server with new nodeexporter
      - job_name: 'pushgatewayexporter'
        static_configs: 
        - targets: ['localhost:9091']    # PushGateway IP address
          labels: 
            instance: pushgateway


        sudo systemctl restart prometheus

    echo "some_metric 3.14" | curl --data-binary @- http://localhost:9091/metrics/job/cron_job/instance/127.0.0.0

    # to find the metrics
    curl -L http://localhost:9091/metrics/

    # if you want delete the request
    curl -X DELETE http://localhost:9091/metrics/job/cron_job/instance/127.0.0.0
    
    
    test cron
    
    #!/usr/bin/env bash

        # filename: cron_batchtrigger.sh

        # Environment Labels Name
        #    jobname: batchtrigger
        #    instance: 127.0.0.1

        command=$(curl -s -o /dev/null -I -w "%{http_code}" https://google.com)
        if [ $command == 200 ]; then
            echo "login_trigger 0" | curl --data-binary @- http://localhost:9091/metrics/job/batchtrigger/instance/127.0.0.0
        else
            echo "login_trigger 1" | curl --data-binary @- http://localhost:9091/metrics/job/batchtrigger/instance/127.0.0.0
        fi

        # bash cron_batchtrigger.sh
