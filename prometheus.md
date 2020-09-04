  Prometheus Installation
   
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
    --web.external-url=http://localhost:9090 \
    --web.listen-address="0.0.0.0:9090" \
    --log.level=info \
    --web.enable-lifecycle \
    --web.page-title="Prometheus Time Series Collection and Processing Server" \
    --log.format=logfmt

    Restart=always
    StandardOutput=syslog
    StandardError=syslog

    [Install]
    WantedBy=default.target

    :wq!


    sudo systemctl daemon-reload
    sudo systemctl start prometheus
    sudo systemctl status prometheus


    sudo netstat -tulpn 
    
    
    open browser IP:9090
