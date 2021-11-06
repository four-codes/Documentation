#### postfix relay with gmail

```bah

sudo vi /etc/postfix/sasl_passwd
[smtp.gmail.com]:587 mailid@gmail.com:PASSWORD

```

#### configuration changes

```bash
sudo postmap /etc/postfix/sasl_passwd
sudo vi /etc/postfix/main.cf

inet_protocols = ipv4
# Gmail SMTP relay
relayhost = [smtp.gmail.com]:587
 
# Enable SASL authentication in the Postfix SMTP client.
smtpd_sasl_auth_enable = yes
smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_sasl_security_options =
smtp_sasl_mechanism_filter = AUTH LOGIN
 
# Enable Transport Layer Security (TLS), i.e. SSL.
smtp_use_tls = yes
smtp_tls_security_level = encrypt
tls_random_source = dev:/dev/urandom

```
#### Restart the postfix

```bash
sudo postfix stop && sudo postfix start
```
#### test mail

```bash
date | mail -s "Test Email" mail@gmail.com
```

