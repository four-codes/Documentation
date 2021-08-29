```sh

  sudo apt install openssh-server
  sudo apt install ssh
  sudo adduser sftp_user
  sudo mkdir -p /var/sftp/folder/data/
  sudo chown root:root /var/sftp/folder
  sudo chmod 755 /var/sftp/folder
  sudo chown sftp_user:sftp_user /var/sftp/folder/data/
  
```

```sh

sudo vim /etc/ssh/sshd_config

  Match User sftp_user
  ForceCommand internal-sftp
  PasswordAuthentication yes # Existing value no. Please change the line
  ChrootDirectory /var/sftp/folder
  PermitTunnel no
  AllowAgentForwarding no
  AllowTcpForwarding no
  X11Forwarding no  # Existing value yes. Please change the line
  
```

```bash

  sudo sshd -t 
  sudo systemctl restart sshd
  
```
```bash

# verification

  ssh sftp_user@localhost
  # This means that sftp_user can no longer can access the server shell using SSH

  sftp sftp_user@localhost
  sftp> ls
  
```

