# Documentation


  SSL certficate creation methods

    openssl req -key server.key -new -out server.csr
    openssl x509 -in certificate.crt -text -noout
    openssl pkcs12 -export -out domain.pfx -inkey domain.key -in domain.crt -certfile more.crt
