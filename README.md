# Documentation


  SSL certficate creation 

    openssl req -newkey rsa:2048 -nodes -keyout domain.key -x509 -days 365 -out domain.crt
    openssl pkcs12 -export -out domain.pfx -inkey domain.key -in domain.crt 
    
  MySQL USER CREATION
  
    CREATE USER 'user'@'localhost' IDENTIFIED BY '.';
    GRANT ALL PRIVILEGES ON *.* TO 'user'@'localhost';
