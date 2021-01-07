# Documentation


  SSL certficate creation methods

    openssl req -newkey rsa:2048 -nodes -keyout domain.key -x509 -days 365 -out domain.crt
    openssl pkcs12 -export -out domain.pfx -inkey domain.key -in domain.crt 
    
