# Documentation

  windows request checker


    Invoke-WebRequest -Headers @{Host='ntwo.dodonotdo.in'} http://3.67.199.67  -UseBasicParsing | Select-Object StatusCode

  SSL certficate creation 

    openssl req -newkey rsa:2048 -nodes -keyout domain.key -x509 -days 365 -out domain.crt
    openssl pkcs12 -export -out domain.pfx -inkey domain.key -in domain.crt 
    
  MySQL USER CREATION
  
    CREATE USER 'user'@'localhost' IDENTIFIED BY '.';
    GRANT ALL PRIVILEGES ON *.* TO 'user'@'localhost';

![docs:- pfx key convert](https://www.ibm.com/docs/en/arl/9.7?topic=certification-extracting-certificate-keys-from-pfx-file)

   .pfx convert into pem
   
       openssl pkcs12 -in client_ssl.pfx -out client_ssl.pem -clcerts
       or
       openssl pkcs12 -in filename.pfx -out client_ssl.pem -nodes
       
   ![verify command](https://docs.apigee.com/how-to-guides/validating-certificate-chain)
       
       openssl x509 -startdate -enddate -noout -in client_ssl.pem
       

   Run the following command to extract the private key:

      openssl pkcs12 -in [yourfile.pfx] -nocerts -out [drlive.key]

   Note: You will be prompted to type the import password. Type the password that you used to protect your keypair when you created the .pfx file. You will be prompted again to provide a new password to protect the .key file that you are creating. Store the password to your key file in a secure place to avoid misuse.

    
   Run the following command to extract the certificate:

      openssl pkcs12 -in [yourfile.pfx] -clcerts -nokeys -out [drlive.crt]

   Run the following command to decrypt the private key:

    openssl rsa -in [drlive.key] -out [drlive-decrypted.key]

